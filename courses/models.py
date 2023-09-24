from django.db import models
from memberships.models import Membership
from django.urls import reverse


class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    allowed_membership = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    def get_membership(self):
        return ",".join([str(m) for m in self.allowed_membership.all()])

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug':self.slug})

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')



class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to='lesson/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:lesson_detail', kwargs={'course_slug':self.course.slug, 'lesson_slug':self.slug})



