from django import forms

from .models import WorkSheet

from apps.qapp.models import Questions
from apps.members.models import Topic, SubTopic


# class WorkSheetForm(forms.ModelForm):

# 	def __init__(self, *args, **kwargs):
# 		super(WorkSheetForm, self).__init__(*args, **kwargs)
# 		self.fields['question'] = forms.ModelMultipleChoiceField(queryset=Questions.objects.all(),
# 															required=True,
# 															widget=forms.CheckboxSelectMultiple
# 														)
# 		self.fields['topic'] = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(),
# 															widget=forms.CheckboxSelectMultiple,
# 															required=True,
# 														)
# 		self.fields['subtopic'] = forms.ModelMultipleChoiceField(queryset=SubTopic.objects.all(),
# 															widget=forms.CheckboxSelectMultiple,
# 															required=False
# 														)
# 		if 'topic' in self.data:
# 			try:
# 				topic_id = int(self.data.get('topic'))
# 				self.fields['subtopic'].queryset = SubTopic.objects.filter(topic_id=topic_id)
# 			except (ValueError, TypeError):
# 				pass
# 		elif self.instance.pk:
# 			self.fields['subtopic'].queryset = SubTopic.objects.all()


# 	class Meta:
# 		model = WorkSheet
# 		exclude = ('school', 'questionNumber')
