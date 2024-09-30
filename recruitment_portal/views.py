from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from rest_framework import generics
from .serializers import CandidateFormSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .templates import *
# Create your views here.


def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "User not found")
        else:
            login(request,user)
            return redirect('home')

    return render(request, 'recruit/login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')


def candidate_details(request,id):
    queryset=Candidate.objects.filter(id=id)

    return render(request, "recruit/candidate_details.html", {'queryset':queryset})


@login_required(login_url="/login/")
def add_candidate(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        registerdate=request.POST.get('registerdate')
        firstround=request.POST.get('firstround')
        secondround=request.POST.get('secondround')
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
            registerdate=registerdate,
            secondround=secondround,
            firstround=firstround,
        )
        return redirect('home')
    queryset=Candidate.objects.all()
    context={'queryset':queryset}
    return render(request, 'recruit/add_candidate.html',context )


def home(request):
    queryset=Candidate.objects.all()

    if request.GET.get('search'):
        search=request.GET.get('search')

        queryset=queryset.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(id__icontains=search) |
            Q(interviewer__icontains=search)
        )
    context={'queryset':queryset}
    return render(request , 'recruit/home.html', context)


class CandidateFormListCreate(generics.ListCreateAPIView):
    queryset=Candidate.objects.all()
    serializer_class=CandidateFormSerializer