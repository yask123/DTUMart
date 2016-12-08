from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Year(models.Model):
    year_choice = [
		('I','I'),
		('II','II'),
		('III','III'),
		('IV','IV'),
	]
    year = models.CharField(choices = year_choice, max_length=5)

    def __str__(self):
        return self.year

class Branch(models.Model):
    branch = models.CharField(max_length=5)

    def __str__(self):
        return self.branch

class Ad(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)
    by = models.ForeignKey(User)
    yr = models.ManyToManyField(Year)
    br = models.ManyToManyField(Branch)
    price = models.IntegerField(default=0)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.title
