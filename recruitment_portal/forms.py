from django import forms
from .models import Candidate
from .models import *

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields=['name', 'age','email','phone','registerdate','experience','address','tech_stack', 'resume']


class InterviewerForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name']  # Only include the 'interviewer' field
        

class FeedbackForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('yet to start', 'Yet to Start'),
        ('1st round', '1st Round'),
        ('2nd round', '2nd Round'),
        ('3rd round', '3rd Round'),
        ('HR round', 'HR Round'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('on-hold', 'On Hold')
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Feedback
        fields = ['feedback', 'status']

class RegistrationForm(forms.Form):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('poc', 'POC'),
        ('interviewer', 'Interviewer'),
    ]

    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    name = forms.CharField(max_length=255, required=True)

class TARegistrationForm(forms.Form):
    TA_ROLE_CHOICES = [
        ('ta_member', 'ta_member'),
                ('poc', 'POC'),

    ]

    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(choices=TA_ROLE_CHOICES, required=True)
    name = forms.CharField(max_length=255, required=True)