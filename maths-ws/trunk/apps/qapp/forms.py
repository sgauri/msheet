from django import forms

from .models import Questions

from apps.members.models import Topic, SubTopic

from collections import OrderedDict


class QuestionsForm(forms.ModelForm):
	required_css_class = 'required'

	ORDER = ['question', 'question_img', 'classroom', 'topic', 'subtopic', 'difficulty', 'question_type', 'options', 'answer', 'solution']

	def __init__(self, *args, **kwargs):
		super(QuestionsForm, self).__init__(*args, **kwargs)
		fields = OrderedDict()
		self.fields['question'] = forms.CharField(widget=forms.Textarea, required=True)
		self.fields['topic'] = forms.CharField(max_length=50, widget=forms.Select(), required=True)
		self.fields['subtopic'] = forms.CharField(max_length=50, widget=forms.Select(), required=True)
		for key in self.ORDER:
			fields[key] = self.fields.pop(key)
		self.fields = fields

	class Meta:
		model = Questions
		exclude = ('school', 'topic', 'subtopic')


class QuestionFilterForm(forms.ModelForm):

	DIFFICULTY = (('l', 'Low'), ('m', 'Medium'), ('h', 'High'))
	CLASSROOM = (('1','I'), ('2','II'), ('3','III'), ('4','IV'), ('5','V'))

	def __init__(self, *args, **kwargs):
		super(QuestionFilterForm, self).__init__(*args, **kwargs)
		self.fields['classroom'] = forms.ChoiceField(choices=self.CLASSROOM, required=True)
		self.fields['topic'] = forms.ModelMultipleChoiceField(queryset=Topic.objects.filter(classrooms__classroom=1),
															widget=forms.CheckboxSelectMultiple,
															required=True
														)
		self.fields['subtopic'] = forms.ModelMultipleChoiceField(queryset=SubTopic.objects.filter(classrooms__classroom=1),
															widget=forms.CheckboxSelectMultiple,
															required=True
														)
		self.fields['difficulty'] = forms.MultipleChoiceField(choices=self.DIFFICULTY,
															widget=forms.CheckboxSelectMultiple,
															required=True
														)


	class Meta:
		model = Questions
		fields = ['classroom', 'topic', 'subtopic', 'difficulty']
