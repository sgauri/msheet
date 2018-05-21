from django.db import models


class TimeStampWS(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class WorkSheet(TimeStampWS):
	question = models.ManyToManyField('qapp.Questions', related_name='wsheets')
	
	CLASSROOM = (('1','I'), ('2','II'), ('3','III'), ('4','IV'), ('5','V'))
	classroom = models.CharField(max_length=2, choices=CLASSROOM)	

	CATEGORY = (
		('testing', 'Test'),
		('practice', 'Practice'),
		('homework', 'Home Work'),
		('quiz', 'Quiz'),
		('classwork', 'Class-Work')
	)
	category = models.CharField(max_length=10, choices=CATEGORY)
	school = models.ForeignKey('members.School', on_delete=models.SET_NULL, null=True)
	topic = models.ManyToManyField('members.Topic')
	subtopic = models.ManyToManyField('members.SubTopic', blank=True)
	duration = models.PositiveIntegerField()
	due_date = models.DateTimeField()

	def __str__(self):
		return '{}-{}'.format(self.category, self.classroom)


class Assessment(TimeStampWS):
	answer = models.TextField()
	school = models.ForeignKey('members.School', on_delete=models.SET_NULL, null=True)
	topic = models.ForeignKey('members.Topic', on_delete=models.CASCADE)
	subtopic = models.ForeignKey('members.SubTopic', on_delete=models.CASCADE)
	worksheet = models.ForeignKey('WorkSheet', on_delete=models.CASCADE)
	question = models.ForeignKey('qapp.Questions', on_delete=models.CASCADE)

	def __str__(self):
		return self.question + ' ; ' + self.answer


class SharingWS(TimeStampWS):
	shared_by = models.ForeignKey('members.Profile', on_delete=models.CASCADE, related_name='shared_by')
	shared_with = models.ForeignKey('members.Profile', on_delete=models.CASCADE, related_name='shared_with')
	worksheet = models.ForeignKey('WorkSheet', on_delete=models.SET_NULL, null=True)
	flag = models.BooleanField()
	reason = models.TextField(blank=True)

	def __str__(self):
		return "{}-{}-{}-{}".format(self.shared_by, self.shared_with, self.worksheet, self.flag)