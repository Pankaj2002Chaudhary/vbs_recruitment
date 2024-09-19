from django.db import models

# Create your models here.
class Candidate(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField()
    phone=models.IntegerField()
    inteviewer=models.CharField(max_length=100)
    resume=models.FileField()
    experience=models.TextField()
    address=models.TextField()
    tech_stack=models.TextField()