from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse

from apps.worksheet.models import SharingWS

from .models import Profile
from .decorators import student_required, teacher_required


def home(request):
	'''
	Renders home page view which has urls to internal links.
	'''
	return render(request, 'apps/members/home.html')


def students_all(request):
	'''
	Displays the list of all students registered.
	'''
	if request.method=="GET":
		students = Profile.objects.filter(role='student')
		return render(request, 'apps/members/students_all.html', {'students':students})


@login_required
@student_required
def student_detail(request):
	
	'''
	This functions uses the session data saved during the login.
	Only logged in students can access this view. Teacher can not access this.
	'''

	login_data = request.session.get('login_data')
	student = Profile.objects.get(user__username=login_data['username'])
	return render(request, 'apps/members/student_detail.html', {'student':student})


@login_required
@teacher_required
def teacher_detail(request):
	'''
	This functions uses the session data saved during the login.
	Only logged in teachers can access this view. Other teachers and
	students can not access this.
	'''

	login_data = request.session.get('login_data')
	teacher = Profile.objects.get(user__username=login_data['username'])
	
	shared_worksheets_all = SharingWS.objects.all()
	self_created = shared_worksheets_all.filter(shared_with=teacher, shared_by=teacher)
	shared_by_others = shared_worksheets_all.filter(shared_with=teacher).exclude(shared_by=teacher)

	context = {'self_created':self_created, 'shared_by_others':shared_by_others, 'teacher':teacher}

	return render(request, 'apps/members/teacher_detail.html', context)


def members_login(request):
	'''
	Single login page for both Teachers and Students.
	This function checks automatically for either of them and
	redirects them to their respective profile view.
	'''

	if request.method == "GET":
		return render(request, 'apps/members/login.html')

	elif request.method == "POST":
		username1 = request.POST['username']
		password1 = request.POST['password']
		user1 = auth.authenticate(username=username1, password=password1)

		if user1 is not None and user1.is_active:
			auth.login(request, user1)
			request.session['login_data'] = request.POST

			u = Profile.objects.get(user__username=username1)
			if u.role == 'student':
				return HttpResponseRedirect(reverse('members:student_detail'))
			elif u.role == 'teacher':
				return HttpResponseRedirect(reverse('members:teacher_detail'))

		else:
			messages.error(request, 'Error! wrong username/password')
	
	return render(request, 'apps/members/login.html')


def members_logout(request):
	'''
	Log out a user
	'''
	auth.logout(request)
	return render(request, 'apps/members/logout.html')
