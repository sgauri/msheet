from django.contrib import admin

from .models import WorkSheet, Assessment, SharingWS


class WorkSheetAdmin(admin.ModelAdmin):
    list_display = ('category', 'classroom', 'school')


class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


class SharingWSAdmin(admin.ModelAdmin):
    list_display = ('shared_by', 'shared_with', 'worksheet', 'flag', 'reason')

admin.site.register(WorkSheet, WorkSheetAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(SharingWS, SharingWSAdmin)