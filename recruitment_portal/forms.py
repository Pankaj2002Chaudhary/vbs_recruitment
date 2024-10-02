# forms.py

from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'age', 'email', 'phone', 'interviewer', 'resume', 'experience', 'address', 'tech_stack', 'registerdate']
