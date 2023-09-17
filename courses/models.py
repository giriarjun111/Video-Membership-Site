from django.db import models
from memberships.models import Membership


class Course(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=100)
	description = models.TextField()
	allowed_membership = models.ManyToManyField(Membership)

	def __str__(self):
		return self.title


class Lesson(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=150)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
	position = models.IntegerField()
	video = models.CharField(max_length=250)
	thumbnail = models.ImageField(upload_to='lesson/')

	def __str__(self):
		return self.title


