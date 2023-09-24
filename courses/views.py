from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Lesson
from memberships.models import UserMembership

# Create your views here.

class IndexView(TemplateView):
	template_name = 'index.html'

class CourseListView(ListView):
	model = Course

class CourseDetailView(DetailView):
	model = Course

class LessonDetailView(LoginRequiredMixin, View):

	def get(self, request, course_slug, lesson_slug, *args, **kwargs):

		course = get_object_or_404(Course, slug=course_slug)


		# course_qs = Course.objects.filter(slug=course_slug)
		# if course_qs.exists():
		# 	course = course_qs.first()

		lesson_qs = course.lessons.filter(slug=lesson_slug)
		if lesson_qs.exists():
			lesson = lesson_qs.first()
		else:
			return render(request, '404.html')

		user_membership = UserMembership.objects.filter(user=request.user).first()
		user_membership_type = user_membership.membership.membership_type

		course_allowed_mem_types = course.allowed_membership.all()

		context = {
			'object': None
		}

		if course_allowed_mem_types.filter(membership_type = user_membership_type).exists():
			context = {'object': lesson}

		return render(request, 'courses/lesson_detail.html', context)

