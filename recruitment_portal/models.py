from django.db import models

# Create your models here.
class Candidate(models.Model):
    name=models.CharField(max_length=100)
    age=models.BigIntegerField()
    email=models.EmailField()
    phone=models.BigIntegerField()
    interviewer=models.CharField(max_length=100)
    resume=models.FileField(default='none',upload_to='resumes/')
    experience=models.TextField()
    address=models.TextField()
    tech_stack=models.TextField()

    def __str__(self):
        return self.name
    