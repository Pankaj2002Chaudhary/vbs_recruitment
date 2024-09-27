from rest_framework import serializers
from .models import *

class CandidateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model=Candidate
        fields=['name', 'age', 'email', 'phone','interviewer', 'experience', 'address', 'tech_stack']