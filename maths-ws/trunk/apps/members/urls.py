from django.conf.urls import re_path
from django.urls import include

from . import views


app_name = 'members'

urlpatterns = [
	re_path(r'^$', views.home, name='home'),
	re_path(r'^students/all/$', views.students_all, name='students_all'),
	re_path(r'^student/$', views.student_detail, name='student_detail'),
	re_path(r'^teacher/$', views.teacher_detail, name='teacher_detail'),
	re_path(r'^login/$', views.members_login , name='login'),
	re_path(r'^logout/$', views.members_logout, name='logout'),
]