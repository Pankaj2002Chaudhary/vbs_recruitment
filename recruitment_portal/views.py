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

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def landing_page(request):
    active_url = None
    
    if request.user.is_authenticated:
        if request.user.groups.filter(name='TA_member').exists():
            active_url = reverse('ta_members')  # URL name for TAMembers
        elif request.user.groups.filter(name='TA_Manager').exists():
            active_url = reverse('ta_managers')  # URL name for Managers
        elif request.user.groups.filter(name='Team_leads_managers').exists():
            active_url = reverse('leads_managers')  # URL name for Interviewers
        # Add other conditions as needed for Employee, POC, etc.
    if isinstance(active_url, HttpResponseRedirect):
        active_url = active_url.url
    return render(request, 'recruit/landing_page.html', {'active_url': active_url})

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
                return redirect('common_page')
            
            elif user.groups.filter(name='Team_poc').exists():
                return redirect('common_page')
            
            else:
                return redirect('login')  # Default redirect if no group matches
        else:
            messages.error(request, "Invalid username or password")  # Display error message

    # Render the login page for GET request or failed login attempt
    return render(request, 'recruit/login.html')


def leads_managers(request):
    return render(request, 'recruit/team_manager_leads.html')
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def add_ta_member(request):
    teams = TATeam.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        team_id = request.POST['ta_team']
        team = TATeam.objects.get(ta_team_id=team_id)
        TAMember.objects.create(name=name,
                                ta_team=team)
        return redirect('ta_managers')  # Redirect to a success page

    return render(request, 'recruit/add_ta_member.html', {'teams': teams})

@login_required
def ta_managers(request):
    try:
        # Get the TA Manager linked to the logged-in user
        ta_manager = TAManager.objects.get(name=request.user.username)

        # Get the TA team of this manager
        ta_team = ta_manager.ta_team

        # Get all members belonging to this TA team
        ta_members = TAMember.objects.filter(ta_team=ta_team)

        # Get candidates added by members of this TA team
        candidates = Candidate.objects.filter(ta_member__in=ta_members)

    except TAManager.DoesNotExist:
        # If the logged-in user is not a TA Manager, redirect them
        return redirect('no_access')

    return render(request, 'recruit/ta_manager.html', {'candidates': candidates})


@login_required
def ta_members(request):
    # Get the TA member associated with the logged-in user
    try:
        ta_member = TAMember.objects.get(name=request.user.username)
    except TAMember.DoesNotExist:
        return redirect('no_access')  # Redirect if user is not a TA member

    # Fetch candidates added by the logged-in TA member
    candidates = Candidate.objects.filter(ta_member=ta_member)
    
    return render(request, 'recruit/ta_members.html', {'candidates': candidates})



def logout_page(request):
    logout(request)
    return redirect('landing_page')



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
            return redirect('common_page')
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

# def add_candidate(request):
#     if request.method == 'POST':
#         form = CandidateForm(request.POST, request.FILES)  # Use the form for validation
#         if form.is_valid():
#             form.save()  # Save the candidate instance directly using the form
#             messages.success(request, "Candidate added successfully!")  # Optional success message
#             return redirect('ta_members')
#         else:
#             # Print form errors to debug
#             print(form.errors)  
#             return HttpResponse(f"Form errors: {form.errors}")
#     else:
#         form = CandidateForm()  # Create a new form instance for GET request

#     return render(request, 'recruit/add_candidate.html', {'form': form})

from django.contrib.auth.decorators import login_required
@login_required
def add_candidate(request):
    try:
        # Check if the user is a TA member
        ta_member = TAMember.objects.filter(name=request.user.username).first()
    except Exception as e:
        print(e)
        return redirect('common_page')

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.ta_member = ta_member
            candidate.save()
            messages.success(request, "Candidate added successfully!")
            return redirect('ta_members' if ta_member else 'ta_managers')
        else:
            # Print form errors to debug
            print(form.errors)
            return HttpResponse(f"Form errors: {form.errors}")
    else:
        form = CandidateForm()

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
        return redirect('common_page')

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
    return redirect('ta_members')

def common_page(request):
    queryset = Candidate.objects.prefetch_related('feedbacks').all()
    user = request.user

    # # Assuming user is related to an Interviewer object, and we need to use interviewer_name
    # try:
    #     interview = Interviewer.objects.get(interviewer_name=request.user.username)
    # except Interviewer.DoesNotExist:
    #     return redirect('no_access')  # Redirect if user is not an Interviewer

    # Fetch candidates associated with the logged-in Interviewer
    # candidates = Candidate.objects.filter(interviewer=interview)

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
        'queryset': queryset,
    }
    return render(request, 'recruit/common_page.html', context)




class CandidateFormListCreate(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateFormSerializer


























