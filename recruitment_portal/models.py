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




class POC(models.Model):
    poc_id = models.AutoField(primary_key=True)  # Auto-increment primary key
    poc_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # FK to Team

    def __str__(self):
        return self.poc_name




class Timesheet(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    ldap = models.CharField(max_length=255)
    lead = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    process = models.CharField(max_length=50)
    activity=models.CharField(max_length=20)
    time_in_mins = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Timesheet for {self.name} ({self.process}) - {self.time_in_mins} min"