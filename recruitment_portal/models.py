from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    program_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    program_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.program_name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    team_name = models.CharField(max_length=255, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)  # FK to Program

    def __str__(self):
        return self.team_name


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    manager_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # FK to Team

    def __str__(self):
        return self.manager_name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    employee_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # FK to Team

    def __str__(self):
        return self.employee_name


class Interviewer(models.Model):
    interviewer_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    interviewer_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # FK to Team

    def __str__(self):
        return self.interviewer_name


class POC(models.Model):
    poc_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    poc_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # FK to Team

    def __str__(self):
        return self.poc_name

    

class TATeam(models.Model):
    ta_team_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    ta_team_name = models.CharField(max_length=255, unique=True)  # TA team name

    def __str__(self):
        return self.ta_team_name
    
class TAManager(models.Model):
    ta_manager_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    name = models.CharField(max_length=255)  # TA Manager's name
    ta_team = models.ForeignKey(TATeam, on_delete=models.CASCADE)  # FK to TA team

    def __str__(self):
        return self.name

# TA Members model
class TAMember(models.Model):
    ta_member = models.AutoField(primary_key=True)  # Auto-increment primary key
    name = models.CharField(max_length=255)  # TA Member's name
    ta_team = models.ForeignKey(TATeam, on_delete=models.CASCADE)  # FK to TA team

    def __str__(self):
        return self.name

class Candidate(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')   
    name = models.CharField(max_length=255,default='none')  # Candidate's name
    ta_member=models.ForeignKey('TAMember', on_delete=models.CASCADE,null=True,blank=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True,blank=True)  # FK to Team
    interviewer = models.ForeignKey('Interviewer', on_delete=models.SET_NULL, null=True,blank=True)  # FK to Interviewer, nullable
    poc = models.ForeignKey('POC', on_delete=models.SET_NULL, null=True,blank=True)  # FK to POC, nullable
    age = models.BigIntegerField()  # Candidate's age
    phone = models.BigIntegerField()  # Phone number
    email = models.EmailField()  # Email address
    registerdate = models.DateField(default='2024-01-01')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    experience = models.TextField()
    address = models.TextField()  # Candidate's address
    tech_stack = models.TextField()  # Technology stack
    team=models.ForeignKey('Team', on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="feedbacks")
    status = models.CharField(max_length=50)  # e.g. "Passed", "Failed", "Pending"
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.candidate.name} by {self.interviewer}"
