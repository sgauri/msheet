from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from .models import Profile

def is_student(user):
	return Profile.objects.filter(user__username=user, role='student')

def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='members:login'):
	'''
	Decorator for views that checks that the logged in user is student,
	redirects to login page if necessary.
	'''
	actual_decorator = user_passes_test(
		is_student,
		login_url=login_url,
		redirect_field_name=redirect_field_name			
	)
	if function:
		return actual_decorator(function)
	
	return actual_decorator


def is_teacher(user):
	return Profile.objects.filter(user__username=user, role='teacher')

def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='members:login'):
	'''
	Decorator for views that checks that the logged in user is a teacher,
	redirects to log-in page if necessary.
	'''
	actual_decorator = user_passes_test(
		is_teacher,
		login_url=login_url,
		redirect_field_name=redirect_field_name			
	)
	if function:
		return actual_decorator(function)

	return actual_decorator