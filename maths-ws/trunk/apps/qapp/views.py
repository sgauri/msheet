from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Questions
from .forms import QuestionsForm, QuestionFilterForm

from apps.members.models import Topic, SubTopic, Profile, School
from apps.worksheet.models import WorkSheet, SharingWS

import datetime
import random


@login_required
def question_add(request):
	current_user = Profile.objects.get(user=request.user)

	if request.method == 'POST':
		form = QuestionsForm(request.POST, request.FILES)

		try:
			topic_name = Topic.objects.get(id=request.POST.get('topic'))
			subtopic_name = SubTopic.objects.get(id=request.POST.get('subtopic'))
			if form.is_valid():
				form_instance = form.save(commit=False)
				form_instance.school = current_user.school
				form_instance.topic = topic_name
				form_instance.subtopic = subtopic_name
				form_instance.save()
				return HttpResponseRedirect(reverse('qapp:success'))
		except Exception:
			messages.error(request, 'Please fill all the required values.')

	else:
		form = QuestionsForm()
	return render(request, 'apps/qapp/question_add.html', {'form': form})


def success(request):
	return render(request, 'apps/qapp/question_success.html')


def question_pagination(request, clsroom, pages):
	class_questions = Questions.objects.filter(classroom=clsroom)
	page = request.GET.get('page', 1)
	paginator = Paginator(class_questions, pages)
	try:
		all_questions = paginator.page(page)
	except PageNotAnInteger:
		all_questions = paginator.page(1)
	except EmptyPage:
		all_questions = paginator.page(paginator.num_pages)

	return render(request, 'apps/qapp/question_pagination.html', {'all_questions': all_questions})


@login_required
def question_filter(request):
	'''
	This function accepts post requests and redirects to 
	another view for showing Preview before submission.
	'''

	if request.method == 'POST':

		request.session['topics_all'] = request.POST.getlist('topic')
		request.session['classroom'] = request.POST.get('classroom')
		request.session['subtopics_all'] = request.POST.getlist('subtopic')
		request.session['wsheet_id'] = request.POST.get('edit')

		if 'manual_filter' in request.POST:
			request.session['question_pk'] = request.POST.getlist('question_pk')
			request.session.modified = True

		elif 'auto_filter' in request.POST:
			question_ids = Questions.objects.filter(
				classroom=request.POST.get('classroom'),
				topic__id__in=request.POST.getlist('topic'),
				subtopic__id__in=request.POST.getlist('subtopic'),
				difficulty__in=request.POST.getlist('difficulty')
			).values_list('id', flat=True)

			try:
				num_questions = int(request.POST.get('auto_select'))
			except ValueError:
				raise ValueError('Please enter numeric value.')
			else:
				questions_available = min(len(question_ids), num_questions)
				random_ids = random.sample(list(question_ids), questions_available)
				request.session['question_pk'] = random_ids
				request.session.modified = True

		return HttpResponseRedirect(reverse('qapp:question_preview'))

	elif request.method == 'GET' and request.GET.get('edit'):
		wsheet_id = request.GET.get('edit')
		wsheet_object = WorkSheet.objects.get(id=wsheet_id)
		classroom = wsheet_object.classroom
		questions = wsheet_object.question.all()
		difficulty = list(set([i.difficulty for i in questions]))
		form = QuestionFilterForm(initial={'classroom': classroom, 'difficulty': difficulty})

		return render(request, 'apps/qapp/question_filter.html', {'form': form, 'wsheet_id': wsheet_id})

	else:
		form = QuestionFilterForm(initial={'difficulty': ['l', 'm', 'h']})
		return render(request, 'apps/qapp/question_filter.html', {'form': form, 'wsheet_id': None})


@login_required
def question_preview_and_save_worksheet(request):
	'''
	Shows preview of questions, gets redirected from
	'question_filter view' with post data.
	'''
	question_pk_list = request.session['question_pk']
	topics_list = request.session['topics_all']
	classroom = request.session['classroom']
	subtopics_list = request.session['subtopics_all']
	wsheet_id = request.session['wsheet_id']

	current_user = Profile.objects.get(user=request.user)

	current_date = timezone.now().date()

	if request.method == 'GET':
		all_questions = Questions.objects.all()
		preview_questions = all_questions.filter(id__in=question_pk_list, school=current_user.school)
		topics = Topic.objects.filter(id__in=topics_list, school=current_user.school)
		context = {'preview_questions': preview_questions, 'topics': topics, 'classroom': classroom,
				   'wsheet_id': wsheet_id}
		return render(request, 'apps/qapp/question_preview.html', context)

	elif request.method == 'POST':

		worksheet_data = {}
		worksheet_data['classroom'] = classroom
		worksheet_data['category'] = request.POST.get('category')
		worksheet_data['duration'] = request.POST.get('duration')
		worksheet_data['school'] = current_user.school

		temp_date = datetime.datetime.strptime(request.POST.get('due_date'), "%Y-%m-%d")
		date_aware = timezone.make_aware(temp_date, timezone.get_current_timezone())
		if date_aware.date() < current_date:
			messages.error(request, 'Due Date can not be in past.')
			return HttpResponseRedirect(reverse('qapp:question_preview'))
		else:
			worksheet_data['due_date'] = date_aware

		if wsheet_id == 'None':
			worksheet_object = WorkSheet(**worksheet_data)
			worksheet_object.save()
			worksheet_object.question.add(*question_pk_list)
			worksheet_object.topic.add(*topics_list)
			worksheet_object.subtopic.add(*subtopics_list)

			current_user.worksheets.add(worksheet_object.id)
			SharingWS.objects.create(shared_by=current_user,
									 shared_with=current_user,
									 worksheet=worksheet_object,
									 flag=True
									)

			all_teachers = request.POST.getlist('all_teachers')
			for i in all_teachers:
				u = Profile.objects.get(pk=i)
				u.worksheets.add(worksheet_object.id)
				sharing_object = SharingWS(shared_by=current_user, shared_with=u, worksheet=worksheet_object, flag=True)
				sharing_object.save()
		else:
			worksheet_update = WorkSheet.objects.filter(pk=int(wsheet_id)).update(
				classroom=worksheet_data['classroom'],
				category=worksheet_data['category'],
				duration=worksheet_data['duration'],
				due_date=worksheet_data['due_date'],
			)
			wsheet_object_new = WorkSheet.objects.get(pk=int(wsheet_id))
			wsheet_object_new.question.set(Questions.objects.filter(id__in=question_pk_list), clear=True)
			wsheet_object_new.topic.set(Topic.objects.filter(id__in=topics_list), clear=True)
			wsheet_object_new.subtopic.set(SubTopic.objects.filter(id__in=subtopics_list), clear=True)

		return HttpResponseRedirect(reverse('worksheet:worksheet_success'))


@login_required
def ajax_load_html_classroom_topics(request):
	classroom = request.GET.get('classroom')
	topics = Topic.objects.filter(classrooms__classroom=classroom)
	return render(request, 'apps/qapp/ajax_load_html_classroom_topics.html', {'topics': topics})


@login_required
def ajax_load_subtopics(request):
	topic_id = request.GET.get('topic')
	classroom = request.GET.get('classroom')
	stopics = SubTopic.objects.filter(classrooms__classroom=classroom).filter(topic_id=topic_id)
	return render(request, 'apps/qapp/ajax_load_subtopics.html', {'stopics': stopics})


@login_required
def ajax_load_classroom_topics(request):
	'''
	Ajax Function to load topics based on the value of class selected.
	Returns JsonResponse to be used in template.
	'''
	classroom = request.GET.get('classroom')
	temp_topics = Topic.objects.filter(classrooms__classroom=classroom).order_by('topic_name')
	topics = temp_topics.values('topic_name', 'id')
	response_data = {}
	try:
		response_data['topics'] = list(topics)
	except:
		response_data['error'] = "No Topics listed for this class."

	return JsonResponse(response_data)


@login_required
def ajax_load_topics_subtopics(request):
	'''
	Ajax Function to load subtopics based on the topics and 
	classroom selected.	Returns JsonResponse of subtopics data.
	'''
	classroom = request.GET.get('classroom')
	topics = request.GET.getlist('topics_all[]')

	temp_subtopics = SubTopic.objects.filter(classrooms__classroom=classroom).filter(topic__id__in=topics)
	subtopics = temp_subtopics.order_by('subtopic_name').values('subtopic_name', 'id')

	response_stopics = {}
	try:
		response_stopics['subtopics'] = list(subtopics)
	except:
		response_stopics['error'] = "No Subtopics available in this class and Topics"

	return JsonResponse(response_stopics)


@login_required
def ajax_load_questions(request):
	'''
	Ajax function for dynamically showing questions based 
	on the values of selected classroom, topics, difficulty and subtopics.
	'''
	all_questions = Questions.objects.all()

	classroom = request.GET.get('classroom')
	topics = request.GET.getlist('topics_all[]')
	difficulty = request.GET.getlist('difficulty[]')
	subtopics = request.GET.getlist('subtopics_all[]')

	filter1 = all_questions.filter(classroom=classroom).filter(topic__id__in=topics)
	questions_list = filter1.filter(subtopic__id__in=subtopics).filter(difficulty__in=difficulty)

	return render(request, 'apps/qapp/ajax_load_questions.html', {'questions_list': questions_list})


@login_required
def ajax_load_teachers(request):
	all_teachers = Profile.objects.filter(role='teacher').exclude(user=request.user).order_by('name')
	return render(request, 'apps/qapp/ajax_load_teachers.html', {'all_teachers': all_teachers})


@login_required
def ajax_edit_topic_subtopic(request):
	wsheet_id = request.GET['wsheet']
	wsheet_object = WorkSheet.objects.get(id=wsheet_id)

	topics_pk = [i.pk for i in wsheet_object.topic.all()]
	subtopics_pk = [i.pk for i in wsheet_object.subtopic.all()]
	topics = Topic.objects.filter(id__in=topics_pk).values('topic_name', 'id')
	subtopics = SubTopic.objects.filter(id__in=subtopics_pk).values('subtopic_name', 'id')

	worksheet_data = {}
	worksheet_data['topics'] = list(topics)
	worksheet_data['subtopics'] = list(subtopics)

	return JsonResponse(worksheet_data)


@login_required
def ajax_edit_questions(request):
	wsheet_object = WorkSheet.objects.get(id=request.GET['wsheet'])
	questions_list = wsheet_object.question.all()
	return render(request, 'apps/qapp/ajax_edit_questions.html', {'questions_list': questions_list})
