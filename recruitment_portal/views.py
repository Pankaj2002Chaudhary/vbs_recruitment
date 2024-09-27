from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from .models import *
from rest_framework import generics
from .serializers import CandidateFormSerializer
# Create your views here.
def home(request):
    queryset=Candidate.objects.all()
    context={'queryset':queryset}
    return render(request , 'recruit/home.html', context)

def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)

        if user is None:
            messages.error("User not found")
        else:
            login(request,user)
            return redirect('home')

    return render(request, 'recruit/login.html')

def candidate_details(request):
    # queryset=Candidate.objects.filter(Candidate__id=id)
    return render(request, "recruit/candidate_details.html")


def add_candidate(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        interviewer=request.POST.get('interviewer')
        resume=request.FILES.get('resume')
        experience=request.POST.get('experience')
        address=request.POST.get('address')
        tech_stack=request.POST.get('tech_stack')

        Candidate.objects.create(
            name=name,
            age=age,
            email=email,
            phone=phone,
            interviewer=interviewer,
            resume=resume,
            experience=experience,
            address=address,
            tech_stack=tech_stack,
        )
        return redirect('home')
    queryset=Candidate.objects.all()
    context={'queryset':queryset}
    return render(request, 'recruit/add_candidate.html',context )


class CandidateFormListCreate(generics.ListCreateAPIView):
    queryset=Candidate.objects.all()
    serializer_class=CandidateFormSerializer