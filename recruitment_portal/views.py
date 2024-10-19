from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import CandidateForm, FeedbackForm  # Ensure you're importing your form
from rest_framework import generics
from .serializers import CandidateFormSerializer
from django.http import HttpResponse  # For debugging purposes


# Create your views here.

# def login_page(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is None:
#             messages.error(request, "User not found")
#         else:
#             login(request, user)
#             login(request, user)
#             return redirect('home')

#     return render(request, 'recruit/login.html')
from django.contrib.auth import login

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Check if authentication is successful
            login(request, user)  # Log the user in
            if user.is_superuser:
                return redirect('/admin/')
            # Redirect based on the user's group
            if user.groups.filter(name='Team_leads_managers').exists():
                return redirect('leads_managers')
            
            elif user.groups.filter(name='TA_Manager').exists():
                return redirect('ta_managers')
            
            elif user.groups.filter(name='TA_member').exists():
                return redirect('ta_members')
            
            elif user.groups.filter(name='Team_interviewer').exists():
                return redirect('home')
            
            elif user.groups.filter(name='Team_poc').exists():
                return redirect('home')
            
            else:
                return redirect('login')  # Default redirect if no group matches
        else:
            messages.error(request, "Invalid username or password")  # Display error message

    # Render the login page for GET request or failed login attempt
    return render(request, 'recruit/login.html')


def leads_managers(request):
    return render(request, 'recruit/team_manager_leads.html')

def ta_managers(request):
    return render(request, 'recruit/ta_manager.html')

def ta_members(request):
    return render(request, 'recruit/ta_members.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')



# def candidate_details(request, id):
#     candidate = get_object_or_404(Candidate, id=id)  # Fetch the candidate by ID
#     context = {
#         'queryset': [candidate]  # Pass the candidate as a list
#     }
#     return render(request, "recruit/candidate_details.html", context)

def add_feedback(request,id):
    candidate = get_object_or_404(Candidate, id=id)
    feedbacks = candidate.feedbacks.all()  # Fetch all feedback related to this candidate

    # Handle feedback form submission
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.candidate = candidate  # Associate the feedback with the candidate
            feedback.save()
            messages.success(request, "Feedback added successfully!")
            return redirect('home')
    else:
        feedback_form = FeedbackForm()

    context = {
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
    }
    return render(request, "recruit/add_feedback.html", context)

def candidate_details(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    feedbacks = candidate.feedbacks.all()  # Fetch all feedback related to this candidate

    # Handle feedback form submission
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.candidate = candidate  # Associate the feedback with the candidate
            feedback.save()
            messages.success(request, "Feedback added successfully!")
            return redirect('details', id=id)
    else:
        feedback_form = FeedbackForm()

    context = {
        'candidate': candidate,
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
    }
    return render(request, "recruit/candidate_details.html", context)


@login_required(login_url="/login/")
def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)  # Use the form for validation
        if form.is_valid():
            form.save()  # Save the candidate instance directly using the form
            messages.success(request, "Candidate added successfully!")  # Optional success message
            return redirect('home')
        else:
            # Print form errors to debug
            print(form.errors)  
            return HttpResponse(f"Form errors: {form.errors}")
    else:
        form = CandidateForm()  # Create a new form instance for GET request

    return render(request, 'recruit/add_candidate.html', {'form': form})


@login_required(login_url="/login/")
def editCandidate(request, id):
    d = get_object_or_404(Candidate, id=id)  # Fetch the candidate object by ID
    feedback = Feedback.objects.filter(candidate=d).last()  # Get the latest feedback for the candidate (or adjust to get the required feedback)

    if request.method == "POST":
        # Retrieve the form data for candidate
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        registerdate = request.POST.get('registerdate')
        interviewer = request.POST.get('interviewer')
        resume = request.FILES.get('resume')  # None if no file is uploaded
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        tech_stack = request.POST.get('tech_stack')

        # Update the candidate object
        d.name = name
        d.age = age
        d.email = email
        d.phone = phone
        d.registerdate = registerdate
        d.interviewer = interviewer
        d.experience = experience
        d.address = address
        d.tech_stack = tech_stack

        # Update the resume only if a new one is uploaded
        if resume:
            d.resume = resume

        # Save the updated candidate object
        d.save()

        messages.success(request, "Candidate details updated successfully!")
        return redirect('home')

    # Render the form with existing candidate and feedback data
    context = {
        "d": d,
        "feedback": feedback  # Pass the feedback to the template
    }
    return render(request, "recruit/edit.html", context)



def delete(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.delete()
    messages.error(request, "Data Deleted Successfully")
    return redirect('home')


def home(request):
    queryset = Candidate.objects.prefetch_related('feedbacks').all()
    user = request.user
    if user.groups.filter(name='Team_poc').exists():
        # Assuming user is related to a POC object, and POC is linked to a team
        poc = POC.objects.filter(poc_name=user.username).first()
        if poc:
            team_id = poc.team.team_id
            queryset = queryset.filter(team_id=team_id)


    if request.GET.get('search'):
        search = request.GET.get('search')
        if search.lower() == 'none':
            queryset = queryset.filter(interviewer__isnull=True)        
        else:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(id__icontains=search) |
                Q(interviewer__interviewer_name__icontains=search)
            )
    context = {
        'is_interviewer': user.groups.filter(name='Team_interviewer').exists() if user.is_authenticated else False,
        'is_poc': user.groups.filter(name='Team_poc').exists() if user.is_authenticated else False,
        'is_employee': user.groups.filter(name='Employee').exists() if user.is_authenticated else False,
        # 'is_team_manager' : user.groups.filter(name="Team_leads_managers").exists() if user.is_authenticated else False,
        'queryset':queryset,
    }
    return render(request, 'recruit/home.html', context)


class CandidateFormListCreate(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateFormSerializer


























