from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Candidate
from .forms import CandidateForm  # Ensure you're importing your form
from rest_framework import generics
from .serializers import CandidateFormSerializer

# Create your views here.

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "User not found")
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'recruit/login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')


# def candidate_details(request, id):
#     candidate = get_object_or_404(Candidate, id=id)
#     return render(request, "recruit/candidate_details.html", {'candidate': candidate})

def candidate_details(request, id):
    candidate = get_object_or_404(Candidate, id=id)  # Fetch the candidate by ID
    context = {
        'queryset': [candidate]  # Pass the candidate as a list
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
        form = CandidateForm()  # Create a new form instance for GET request

    return render(request, 'recruit/add_candidate.html', {'form': form})


@login_required(login_url="/login/")
def editCandidate(request, id):
    d = get_object_or_404(Candidate, id=id)  # Fetch the candidate object by ID

    if request.method == "POST":
        # Retrieve the form data
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

    # Render the form with existing candidate data
    context = {"d": d}
    return render(request, "recruit/edit.html", context)


def delete(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.delete()
    messages.error(request, "Data Deleted Successfully")
    return redirect('home')


def home(request):
    queryset = Candidate.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(id__icontains=search) |
            Q(interviewer__icontains=search)
        )
        
    return render(request, 'recruit/home.html', {'queryset': queryset})


class CandidateFormListCreate(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateFormSerializer


















