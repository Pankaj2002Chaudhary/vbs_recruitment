from rest_framework import serializers
from .models import *

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = '__all__'  # or list all the fields explicitly
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_id', 'team_name', 'program']  # Adjust fields based on your model
        
class EmployeeSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Employee
        fields = "__all__"