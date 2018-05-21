from django.contrib import admin

from .models import School, ClassRoom, ClassSection, Topic, SubTopic, Profile


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'city')


class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'school')


class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'class_section', 'school')
    list_display_links = ('classroom', 'class_section')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_name', 'school', 'get_classrooms')

    def get_classrooms(self, obj):
        return "; ".join([c.classroom for c in obj.classrooms.all()])


class SubTopicAdmin(admin.ModelAdmin):
    list_display = ('subtopic_name', 'topic', 'get_classrooms')

    def get_classrooms(self, obj):
        return "; ".join([c.classroom for c in obj.classrooms.all()])


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'school', 'name', 'class_section')


admin.site.register(School, SchoolAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(ClassSection, ClassSectionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(SubTopic, SubTopicAdmin)
admin.site.register(Profile, ProfileAdmin)