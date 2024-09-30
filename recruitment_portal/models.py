from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Candidate(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')   
    name=models.CharField(max_length=100,default="None")
    age=models.BigIntegerField()
    email=models.EmailField()
    phone=models.BigIntegerField()
    registerdate=models.DateField(default='2024-01-01')
    firstround=models.DateField(default='2024-01-01')
    secondround=models.DateField(default='2024-01-01')
    interviewer=models.CharField(max_length=100)
    resume=models.FileField(default='none')
    experience=models.TextField()
    address=models.TextField()
    tech_stack=models.TextField()

    def __str__(self):
        return self.name
    

