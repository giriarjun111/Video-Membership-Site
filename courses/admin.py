from django.contrib import admin
from .models import Course, Lesson

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ['title', 'get_membership']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
	list_display = ['title', 'course']
