from django.db import models


class TimeStampQApp(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Questions(TimeStampQApp):
	question = models.TextField()
	question_img = models.ImageField(upload_to='question_images', blank=True, null=True)
	school = models.ForeignKey('members.School', on_delete=models.SET_NULL, null=True, related_name='schoolquestion')

	CLASSROOM = (('1','I'), ('2','II'), ('3','III'), ('4','IV'), ('5','V'))
	classroom = models.CharField(max_length=2, choices=CLASSROOM)

	topic = models.ForeignKey('members.Topic', on_delete=models.SET_NULL, null=True)
	subtopic = models.ForeignKey('members.SubTopic', on_delete=models.SET_NULL, null=True)

	DIFFICULTY = (('l', 'Low'), ('m', 'Medium'), ('h', 'High'))
	difficulty = models.CharField(max_length=1, choices=DIFFICULTY)

	TYPE = (
		('value', 'Short Answer'),
		('fill_blank', "Fill in the blanks"),
		('mcq', "Multiple Choice"),
		('lhs_rhs', "Left Right Matching"),
	)
	question_type = models.CharField(max_length=10, choices=TYPE)
	options = models.TextField(blank=True)
	answer = models.TextField()
	solution = models.TextField(blank=True)

	def __str__(self):
		return self.question