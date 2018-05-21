from django.db import models
from django.contrib.auth.models import User

from mathsws import settings


class TimeStampMembers(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class School(TimeStampMembers):
	school_name = models.CharField(max_length=100)
	address = models.TextField()
	city = models.CharField(max_length=60, blank=True)
	state = models.CharField(max_length=30)
	pin = models.CharField(max_length=6)
	description = models.TextField(blank=True)
	email = models.EmailField()
	logo = models.ImageField(upload_to='logo', blank=True, null=True)

	def __str__(self):
		return self.school_name


class ClassRoom(TimeStampMembers):
	CLASSROOM = (('1','I'), ('2','II'), ('3','III'), ('4','IV'), ('5','V'))
	classroom = models.CharField(max_length=2, choices=CLASSROOM)

	school = models.ForeignKey('School', on_delete=models.CASCADE)

	def __str__(self):
		return self.classroom


class ClassSection(TimeStampMembers):
	class_section = models.CharField(max_length=2)
	classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)
	school = models.ForeignKey('School', on_delete=models.CASCADE)

	def __str__(self):
		return "{}-{}".format(self.classroom, self.class_section)


class Topic(TimeStampMembers):
	topic_name = models.CharField(max_length=50)
	classrooms = models.ManyToManyField('ClassRoom', blank=True)
	school = models.ForeignKey('School', on_delete=models.CASCADE)

	def __str__(self):
		return self.topic_name


class SubTopic(TimeStampMembers):
	subtopic_name = models.CharField(max_length=100)
	topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
	classrooms = models.ManyToManyField('ClassRoom', blank=True)
	school = models.ForeignKey('School', on_delete=models.CASCADE)

	def __str__(self):
		return self.subtopic_name


class BaseProfile(TimeStampMembers):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

	ROLE = (
		# ('student', 'student'),
		('teacher', 'teacher'),
	)
	role = models.CharField(max_length=15, choices=ROLE, null=True)
	school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=100, null=True)
	email = models.EmailField(null=True)
	image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/default.png')
	worksheets = models.ManyToManyField('worksheet.WorkSheet', blank=True)

	class Meta:
		abstract = True

	def __str__(self):
		return "{}-{}-{}".format(self.user, self.role, self.name)


class Student(models.Model):
	roll_number = models.CharField(max_length=10, null=True, blank=True)
	classroom = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL, null=True, blank=True)
	class_section = models.ForeignKey('ClassSection', models.SET_NULL, null=True, blank=True)

	class Meta:
		abstract = True


class Teacher(models.Model):
	teacher_id = models.CharField(max_length=15, null=True, blank=True)

	class Meta:
		abstract = True


class Profile(Student, Teacher, BaseProfile):
	'''
	Contains all the fields of inherited models and display them in admin.
	'''