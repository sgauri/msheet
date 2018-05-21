from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from apps.members.decorators import student_required, teacher_required
from apps.members.models import Profile

from .models import WorkSheet, SharingWS

import datetime


def success(request):
	return render(request, 'apps/worksheet/worksheet_success.html')


@login_required
def worksheet_review_success(request):
	return render(request, 'apps/worksheet/worksheet_review_success.html')


class WorkSheetListView(generic.ListView):
	model = WorkSheet
	queryset = WorkSheet.objects.all()[:10]
	context_object_name = 'worksheet_list'
	template_name = 'apps/worksheet/worksheet_list.html'


@login_required
def worksheet_detail(request, id_name):
	if request.method=="GET":
		full_wsheet = WorkSheet.objects.get(id=id_name)
		return render(request,
                        'apps/worksheet/worksheet_detail.html',
                        {'full_wsheet':full_wsheet})


@login_required
def worksheet_answers(request, id_ans):
	if request.method == 'GET':
		full_wsheet = WorkSheet.objects.get(id=id_ans)
		return render(request,
                              'apps/worksheet/worksheet_answers.html',
                              {'full_wsheet':full_wsheet})


@login_required
def worksheet_review(request, id_r):
	full_wsheet = WorkSheet.objects.get(id=id_r)
	shared_by_list = SharingWS.objects.filter(worksheet=id_r).values_list('shared_by',flat=True)
	current_time = timezone.now().replace(second=0, microsecond=0)
	
	if len(shared_by_list)==0:
		shared_by = 1
	else:
		shared_by = shared_by_list[0]

	if request.method == 'GET':
		return render(request, 'apps/worksheet/worksheet_review.html', {'full_wsheet':full_wsheet})

	elif request.method=='POST':
		review_data = {}
		review_data['worksheet'] = full_wsheet
		review_data['shared_with'] = Profile.objects.get(pk=request.user)
		review_data['shared_by'] = Profile.objects.get(pk=shared_by)
		share_instance = SharingWS.objects.filter(**review_data)[0]
		creation_time = share_instance.created_at.replace(second=0,microsecond=0)

		if creation_time==share_instance.last_updated.replace(second=0,microsecond=0):
			share_instance.reason = request.POST.get('reason')
			share_instance.flag = request.POST.get('flag', '') == 'on'
			share_instance.save()
			return HttpResponseRedirect(reverse('worksheet:worksheet_review_success'))

		elif current_time - creation_time > datetime.timedelta(days=2):
			return HttpResponseRedirect(reverse('worksheet:worksheet_review_once'))

		else:
			return HttpResponseRedirect(reverse('worksheet:worksheet_review_once'))


@login_required
def worksheet_review_once(request):
	return render(request, 'apps/worksheet/worksheet_review_once.html')


@login_required
def worksheet_reviews_all(request, id_review):
	current_user = Profile.objects.get(user=request.user)
	reviews = SharingWS.objects.filter(worksheet=id_review).exclude(shared_with=current_user)
	return render(request, 'apps/worksheet/worksheet_reviews_all.html', {'reviews':reviews})


#-----------#-----------#-----------#-----------#-----------#-----------#-----------#-----------#
#-----------#-----------#-----------# Student Dashboard View #-----------#-----------#----------#
#-----------#-----------#-----------#-----------#-----------#-----------#-----------#-----------#


@login_required
@student_required
def worksheet_answers_fill(request, id_w):
	if request.method=='GET':
		wsheet = WorkSheet.objects.get(id=id_w)
		return render(request, 'apps/worksheet/worksheet_answers_fill.html', {'wsheet':wsheet})


def submit_answers(request):
	pass


