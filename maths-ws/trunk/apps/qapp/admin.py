from django.contrib import admin

from .models import Questions


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_img', 'classroom', 'topic', 'subtopic')


admin.site.register(Questions, QuestionsAdmin)