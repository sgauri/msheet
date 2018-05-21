from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone

from apps.qapp.models import Questions
from apps.qapp.views import *
from apps.qapp.forms import QuestionsForm, QuestionFilterForm
from apps.members.models import ClassRoom

import datetime


class TestAddQuestion(TestCase):

	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='testuser1', email='user@test.com', password='testuser1')
		self.client.force_login(self.user)
		teacher1 = Profile.objects.create(user=self.user)

	def test_question_add_loads_correct_template(self):
		response = self.client.get(reverse('qapp:question_add'))
		self.assertTemplateUsed(response, 'apps/qapp/question_add.html')

	def test_login_question_add(self):
		request = self.factory.get(reverse('qapp:question_add'))
		request.user = self.user
		response = question_add(request)
		self.assertEqual(response.status_code, 200)

	def test_question_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'question':''})
		self.assertFormError(response, 'form', 'question', 'This field is required.')

	def test_classroom_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'classroom':''})
		self.assertFormError(response, 'form', 'classroom', 'This field is required.')

	def test_topic_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'topic':''})
		self.assertFormError(response, 'form', 'topic', 'This field is required.')

	def test_subtopic_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'subtopic':''})
		self.assertFormError(response, 'form', 'subtopic', 'This field is required.')

	def test_difficulty_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'difficulty':''})
		self.assertFormError(response, 'form', 'difficulty', 'This field is required.')

	def test_question_type_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'question_type':''})
		self.assertFormError(response, 'form', 'question_type', 'This field is required.')

	def test_answer_is_not_empty(self):
		response = self.client.post(reverse('qapp:question_add'), {'answer':''})
		self.assertFormError(response, 'form', 'answer', 'This field is required.')



class TestQuestionFilter(TestCase):

	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='testuser1', email='user@test.com', password='testuser1')
		self.client.force_login(self.user)
		date1 = timezone.make_aware(datetime.datetime.strptime('2022-12-31', "%Y-%m-%d"), timezone.get_current_timezone())
		school1 = School.objects.create(school_name='Fr. Agnel',address='address1',city='Delhi',
										state='Delhi',pin='110001',email='school@example.com')

		classroom1 = ClassRoom.objects.create(classroom='1', school=school1)
		topic1 = Topic.objects.create(topic_name='Algebra',school=school1)
		topic1.classrooms.add(classroom1)
		topic2 = Topic.objects.create(topic_name='Geometry',school=school1)
		topic2.classrooms.add(classroom1)
		stopic1 = SubTopic.objects.create(subtopic_name='Addition',topic=topic1,school=school1)
		stopic1.classrooms.add(classroom1)
		stopic2 = SubTopic.objects.create(subtopic_name='2D Objects',topic=topic2,school=school1)
		stopic2.classrooms.add(classroom1)
		teacher1 = Profile.objects.create(user=self.user)
		q1 = Questions.objects.create(question='question1',school=school1,classroom='1',topic=topic1,
									subtopic=stopic1,difficulty='l',question_type='value',answer='ans1')
		q2 = Questions.objects.create(question='question2',school=school1,classroom='1',topic=topic2,
									subtopic=stopic2,difficulty='l',question_type='value',answer='ans2')
		self.wsheet1 = WorkSheet.objects.create(classroom='1',category='practice',school=school1,
											duration=10,due_date=date1)
		self.wsheet1.question.add(q1)
		self.wsheet1.topic.add(topic1)
		self.wsheet1.subtopic.add(stopic1)

	def test_login_question_filter(self):
		resp = self.client.get(reverse('qapp:question_filter'))
		self.assertEqual(resp.status_code, 200)

	def test_get_request_loads_correct_template(self):
		response = self.client.get(reverse('qapp:question_filter'))
		self.assertTemplateUsed(response, 'apps/qapp/question_filter.html')

	def test_get_request_with_data_loads_correct_template(self):
		wsheet_id = WorkSheet.objects.get(id=self.wsheet1.id)
		response = self.client.get(reverse('qapp:question_filter'), {'edit':wsheet_id.id})
		self.assertTemplateUsed(response, 'apps/qapp/question_filter.html')

	def test_manual_filter_has_questions_with_post_request(self):
		response = self.client.post(reverse('qapp:question_filter'), {'manual_filter':1})
		self.assertEqual(response.status_code, 302)

	def test_post_request_redirects_to_question_preview_page(self):
		data = {'topics_all':[1], 'subtopics_all':[1], 'wsheet_id':1, 'classroom':1}
		response = self.client.post(reverse('qapp:question_filter'), data)
		self.assertEqual(response.status_code, 302)

	def test_invalid_numeral_raises_value_error_exception(self):
		data = {'auto_filter':1, 'auto_select':'a'}
		with self.assertRaises(ValueError) as d1:
			self.client.post(reverse('qapp:question_filter'), data)
		self.assertEqual(str(d1.exception), 'Please enter numeric value.')



class TestQuestionPreviewAndSaveWorkSheet(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser1', email='user@test.com', password='testuser1')
		self.client.force_login(self.user)
		school1 = School.objects.create(school_name='Fr. Agnel',address='address1',city='Delhi',
										state='Delhi',pin='110001',email='school@example.com')

		classroom1 = ClassRoom.objects.create(classroom='1', school=school1)
		topic1 = Topic.objects.create(topic_name='Algebra',school=school1)
		topic1.classrooms.add(classroom1)
		topic2 = Topic.objects.create(topic_name='Geometry',school=school1)
		topic2.classrooms.add(classroom1)
		stopic1 = SubTopic.objects.create(subtopic_name='Addition',topic=topic1,school=school1)
		stopic1.classrooms.add(classroom1)
		stopic2 = SubTopic.objects.create(subtopic_name='2D Objects',topic=topic2,school=school1)
		stopic2.classrooms.add(classroom1)
		# teacher1 = Profile.objects.create(user=self.user)
		q1 = Questions.objects.create(question='question1',school=school1,classroom='1',topic=topic1,
									subtopic=stopic1,difficulty='l',question_type='value',answer='ans1')
		q2 = Questions.objects.create(question='question2',school=school1,classroom='1',topic=topic2,
									subtopic=stopic2,difficulty='l',question_type='value',answer='ans2')
	
		session = self.client.session
		session['question_pk'] = [q1.id,q2.id]
		session['topics_all'] = [topic1.id,topic2.id]
		session['classroom'] = 3
		session['subtopics_all'] = [stopic1.id,stopic2.id]
		session['wsheet_id'] = 4
		session.save()
		self.profile_object = Profile.objects.create(user=self.user)

	def test_current_user_is_same_as_logged_in_user(self):
		user = User.objects.get(username='testuser1')
		self.assertEqual(user, self.user)

	def test_get_request_renders_correct_template(self):
		response = self.client.get(reverse('qapp:question_preview'))
		self.assertTemplateUsed(response, 'apps/qapp/question_preview.html')

	def test_due_date_should_be_later_than_current_date(self):
		date3 = timezone.make_aware(datetime.datetime.strptime('2016-12-31', "%Y-%m-%d"), timezone.get_current_timezone()).date()
		data = {'category':'Test', 'due_date':date3, 'duration':1}
		response = self.client.post(reverse('qapp:question_preview'), data)
		m = list(response.wsgi_request._messages)
		self.assertEqual(str(m[0]), 'Due Date can not be in past.')

	def test_object_is_saved_in_ShareWS_table_also(self):
		date3 = timezone.make_aware(datetime.datetime.strptime('2022-12-31', "%Y-%m-%d"), timezone.get_current_timezone()).date()
		data = {'category':'Test', 'due_date':date3, 'duration':1, 'classroom':3}
		session = self.client.session
		session['wsheet_id'] = 'None'
		session.save()
		response = self.client.post(reverse('qapp:question_preview'), data)
		wsheet = WorkSheet(**data)
		wsheet.save()
		wsheet.question.add(*session['question_pk'])
		wsheet.topic.add(*session['topics_all'])
		wsheet.subtopic.add(*session['subtopics_all'])
		user1 = User.objects.get(username='testuser1')
		user2 = User.objects.create_user(username='testuser2', email='user2@test.com', password='testuser2')
		profile2 = Profile.objects.create(user=user2)
		share1 = SharingWS.objects.create(shared_by=self.profile_object, shared_with=profile2, worksheet=wsheet, flag=True)
		self.assertEqual(share1.id, 2)

	def test_worksheet_is_getting_saved_in_database(self):
		date3 = timezone.make_aware(datetime.datetime.strptime('2022-12-31', "%Y-%m-%d"), timezone.get_current_timezone()).date()
		data = {'category':'Test', 'due_date':date3, 'duration':1, 'classroom':3}
		session = self.client.session
		session['wsheet_id'] = 'None'
		session.save()
		response = self.client.post(reverse('qapp:question_preview'), data)
		wsheet = WorkSheet(**data)
		wsheet.save()
		wsheet.question.add(*session['question_pk'])
		wsheet.topic.add(*session['topics_all'])
		wsheet.subtopic.add(*session['subtopics_all'])
		self.assertEqual(wsheet.id, 10)