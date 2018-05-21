from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse

from apps.members.views import members_login
from apps.members.models import Profile


class TestMembersLogin(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser1', email='user@test.com', password='testuser1')
		self.user2 = User.objects.create_user(username='testuser2', email='user@test2.com', password='testuser2')

	def test_get_request_loads_correct_template(self):
		response = self.client.get(reverse('members:login'))
		self.assertTemplateUsed(response, 'apps/members/login.html')

	def test_post_request_is_accepted_correctly(self):
		user1 = Profile.objects.create(user=self.user)
		response = self.client.post(reverse('members:login'), {'username':'testuse', 'password':'testuser1'})
		self.assertEqual(response.status_code, 200)

	def test_authenticated_users_are_allowed_to_log_in(self):
		user1 = Profile.objects.create(user=self.user)
		response = self.client.post(reverse('members:login'), {'username':'testuse', 'password':'testuser1'})
		m = list(response.wsgi_request._messages)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(str(m[0]), 'Error! wrong username/password')

	def test_teacher_is_redirected_to_teacher_detail_page(self):
		user1 = Profile.objects.create(user=self.user)
		user1.role = 'teacher'
		user1.save()
		self.client.force_login(self.user)
		response = self.client.post(reverse('members:login'), {'username':'testuser1', 'password':'testuser1'})
		self.assertEqual(response.status_code, 302)
