from django.conf.urls import re_path
from django.urls import path
from . import views

app_name = 'worksheet'

urlpatterns = [
	re_path(r'^worksheet/success/$', views.success, name='worksheet_success'),
	re_path(r'^worksheets/$', views.WorkSheetListView.as_view(), name='worksheet_list'),
	re_path(r'^worksheet/(?P<id_name>\d+)/$', views.worksheet_detail, name='worksheet_detail'),

	re_path(r'^worksheet/(?P<id_w>\d+)/answers/fill/$', views.worksheet_answers_fill, name='worksheet_answers_fill'),
	re_path(r'^worksheet/(?P<id_ans>\d+)/answers/$', views.worksheet_answers, name='worksheet_answers'),
	
	re_path(r'^worksheet/(?P<id_r>\d+)/review/$', views.worksheet_review, name='worksheet_review'),
	re_path(r'^worksheet/review/once/$', views.worksheet_review_once, name='worksheet_review_once'),
	re_path(r'^worksheet/review/success/$', views.worksheet_review_success, name='worksheet_review_success'),
	re_path(r'^worksheet/(?P<id_review>\d+)/reviews/all/$', views.worksheet_reviews_all, name='worksheet_reviews_all'),
]