# forms.py

from django import forms
from .models import Candidate
from .models import Feedback

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'age', 'email', 'phone', 'interviewer', 'resume', 'experience', 'address', 'tech_stack', 'registerdate']



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
    
    INTERVIEWER_CHOICES = [
        ('Akhil Bhatnagar', 'Akhil Bhatnagar'),
        ('Prasenjith Jana', 'Prasenjith Jana'),
        ('Parag Kayat', 'Parag Kayat'),
        ('Trapti Kapkoti', 'Trapti Kapkoti')
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    interviewer = forms.ChoiceField(choices=INTERVIEWER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Feedback
        fields = ['feedback', 'status', 'interviewer']

# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['interviewer', 'status', 'feedback']
