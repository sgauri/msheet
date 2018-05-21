from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from django.utils import timezone

from apps.worksheet.views import worksheet_review
from apps.worksheet.models import *
from apps.qapp.models import Questions
from apps.members.models import Profile, School, Topic, SubTopic, ClassRoom

import datetime


class TestWorkSheetReview(TestCase):


	def setUp(self):
		self.client = Client()
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
		# teacher1 = Profile.objects.create(user=self.user)
		q1 = Questions.objects.create(question='question1',school=school1,classroom='1',topic=topic1,
									subtopic=stopic1,difficulty='l',question_type='value',answer='ans1')
		q2 = Questions.objects.create(question='question2',school=school1,classroom='1',topic=topic2,
									subtopic=stopic2,difficulty='l',question_type='value',answer='ans2')
		self.wsheet1 = WorkSheet.objects.create(classroom='1',category='practice',school=school1,
											duration=10,due_date=date1)
		self.wsheet1.question.add(q1)
		self.wsheet1.topic.add(topic1)
		self.wsheet1.subtopic.add(stopic1)
		
	def test_worksheet_review_get_request_renders_correct_template(self):
		response = self.client.get(reverse('worksheet:worksheet_review', args=[self.wsheet1.id]))
		self.assertTemplateUsed(response, 'apps/worksheet/worksheet_review.html')

	def test_worksheet_detail_renders_correct_template(self):
		response = self.client.get(reverse('worksheet:worksheet_detail', args=[self.wsheet1.id]))
		self.assertTemplateUsed(response, 'apps/worksheet/worksheet_detail.html')

	def test_worksheet_list_view_renders_correct_template(self):
		response = self.client.get(reverse('worksheet:worksheet_list'))
		self.assertTemplateUsed(response, 'apps/worksheet/worksheet_list.html')

	def test_worksheet_review_once_renders_correct_template(self):
		response = self.client.get(reverse('worksheet:worksheet_review_once'))
		self.assertTemplateUsed(response, 'apps/worksheet/worksheet_review_once.html')

	def test_worksheet_reviews_all_renders_correct_template(self):
		user1 = Profile.objects.create(user=self.user)
		response = self.client.get(reverse('worksheet:worksheet_reviews_all', args=[self.wsheet1.id]))
		self.assertTemplateUsed(response, 'apps/worksheet/worksheet_reviews_all.html')