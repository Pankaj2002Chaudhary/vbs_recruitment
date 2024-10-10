from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Candidate(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')   
    name = models.CharField(max_length=100, default="None")
    age = models.BigIntegerField()
    email = models.EmailField()
    phone = models.BigIntegerField()
    registerdate = models.DateField(default='2024-01-01')
    interviewer = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    experience = models.TextField()
    address = models.TextField()
    tech_stack = models.TextField()

    def __str__(self):
        return self.name

class Feedback(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="feedbacks")
    interviewer = models.CharField(max_length=100)
    status = models.CharField(max_length=50)  # e.g. "Passed", "Failed", "Pending"
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.candidate.name} by {self.interviewer}"









# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
# class Candidate(models.Model):
#     id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')   
#     name=models.CharField(max_length=100,default="None")
#     age=models.BigIntegerField()
#     email=models.EmailField()
#     phone=models.BigIntegerField()
#     registerdate=models.DateField(default='2024-01-01')
#     interviewer=models.CharField(max_length=100)
#     # resume=models.FileField(default='none')
#     resume = models.FileField(upload_to='resumes/', blank=True, null=True)
#     experience=models.TextField()
#     address=models.TextField()
#     tech_stack=models.TextField()

#     def __str__(self):
#         return self.name
    

