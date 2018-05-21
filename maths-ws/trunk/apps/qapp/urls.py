from django.conf.urls import re_path
from . import views

app_name = 'qapp'

urlpatterns = [
	re_path(r'^question/add/$', views.question_add, name='question_add'),
	re_path(r'^ajax/load_html_classroom_topics/$', views.ajax_load_html_classroom_topics, name='ajax_load_html_classroom_topics'),
	re_path(r'^ajax/load_stopics/$', views.ajax_load_subtopics, name='ajax_load_subtopics'),

	re_path(r'^question/success/$', views.success, name='success'),

	re_path(r'^pagination/(?P<clsroom>\d{1})/(?P<pages>\d{1})/$', views.question_pagination, name='question_pagination'),

	re_path(r'^question/filter/$', views.question_filter, name='question_filter'),
	re_path(r'^ajax/load_classroom_topics/$', views.ajax_load_classroom_topics, name='ajax_load_classroom_topics'),
	re_path(r'^ajax/load_topics_subtopics/$', views.ajax_load_topics_subtopics, name='ajax_load_topics_subtopics'),
	re_path(r'^ajax/load_questions/$', views.ajax_load_questions, name='ajax_load_questions'),
	re_path(r'^ajax/edit/topic/subtopic/$', views.ajax_edit_topic_subtopic, name='ajax_edit_topic_subtopic'),
	re_path(r'^ajax/edit/questions/$', views.ajax_edit_questions, name='ajax_edit_questions'),

	re_path(r'^question/preview/$', views.question_preview_and_save_worksheet, name='question_preview'),
	re_path(r'^ajax/load_teachers/$', views.ajax_load_teachers, name='ajax_load_teachers')
]