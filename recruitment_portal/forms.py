from django import forms
from .models import Candidate
from .models import Feedback

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields=['name', 'age','email','phone','registerdate','interviewer','experience','address','tech_stack', 'resume']
        

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

