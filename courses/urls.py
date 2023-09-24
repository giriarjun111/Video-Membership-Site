from django.urls import path
from .views import IndexView, CourseListView, CourseDetailView, LessonDetailView


app_name =  'courses'

urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('courses/', CourseListView.as_view(), name='course'),
    path('course/<slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<course_slug>/<lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail')
]
