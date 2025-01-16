from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from rest_framework import generics
from django.http import HttpResponse  # For debugging purposes
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from .forms import *
def custom_password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Here you send the email to the entered email address
            send_mail(
                'Password Reset Request',
                'Here is the link to reset your password: [URL]',
                'sandysaluja7@gmail.com',  # Sender email
                [email],  # Recipient email
                fail_silently=False,
            )
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


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
                return redirect('poc')
            
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









def logout_page(request):
    logout(request)
    return redirect('landing_page')



# def candidate_details(request, id):
#     candidate = get_object_or_404(Candidate, id=id)  # Fetch the candidate by ID
#     context = {
#         'queryset': [candidate]  # Pass the candidate as a list
#     }
#     return render(request, "recruit/candidate_details.html", context)





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








def common_page(request):
    queryset = Employee.objects.prefetch_related('feedbacks').all()
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
                Q(id__icontains=search) 
                # Q(interviewer__interviewer_name__icontains=search)
            )

    context = {
        'is_poc': user.groups.filter(name='Team_poc').exists() if user.is_authenticated else False,
        'is_employee': user.groups.filter(name='Employee').exists() if user.is_authenticated else False,
        'queryset': queryset,
    }
    return render(request, 'recruit/common_page.html', context)






from django.contrib.auth.models import User
from django.contrib import messages
from .models import Team, Employee, POC, Manager
from .forms import RegistrationForm
from django.contrib.auth.models import Group

def register_member(request):
    # Retrieve the manager's team based on the logged-in user's name or identifier
        # Assuming the manager's name matches the logged-in user's username
    manager = Manager.objects.get(manager_name=request.user.username)
    print(manager)
    team = manager.team
    print(team)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            name = form.cleaned_data['name']

            # Create the User object
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Assign the user to a group based on their role
            group_name = None
            if role == 'employee':
                Employee.objects.create(employee_name=name, team=team)
                group_name = 'Team_employee'
            elif role == 'poc':
                POC.objects.create(poc_name=name, team=team)
                group_name = 'Team_poc'
            elif role == 'interviewer':
                Interviewer.objects.create(interviewer_name=name, team=team)
                group_name = 'Team_interviewer'

            if group_name:
                group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(group)  # Assign the user to the group
                user.save()

            messages.success(request, f'{role.capitalize()} registered successfully with username: {username}')
            return redirect('leads_managers')

    else:
        form = RegistrationForm()

    return render(request, 'recruit/register_member.html', {'form': form, 'team': team})


# from .forms import TARegistrationForm
# def register_ta_member(request):
#     # Retrieve the manager's team based on the logged-in user's name or identifier
#         # Assuming the manager's name matches the logged-in user's username
#     manager = TAManager.objects.get(name=request.user.username)
#     team = manager.ta_team
#     print(team)

#     if request.method == 'POST':
#         form = TARegistrationForm(request.POST)
#         if form.is_valid():
#             print("ok")
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             role = form.cleaned_data['role']
#             name = form.cleaned_data['name']

#             # Create the User object
#             user = User.objects.create_user(username=username, password=password)
#             user.save()

#             # Assign the user to a group based on their role
#             group_name = None
#             if role == 'ta_member':
#                 TAMember.objects.create(name=name, ta_team=team)
#                 group_name = 'TA_member'

#             if group_name:
#                 group, created = Group.objects.get_or_create(name=group_name)
#                 user.groups.add(group)  # Assign the user to the group
#                 user.save()

#             messages.success(request, f'{role.capitalize()} registered successfully with username: {username}')
#             return redirect('ta_managers')

#     else:
#         form = TARegistrationForm()

#     return render(request, 'recruit/register_ta_member.html', {'form': form, 'team': team})







from rest_framework import viewsets
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class TimesheetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Retrieve all timesheets
        timesheets = Timesheet.objects.all()
        serializer = TimesheetSerializer(timesheets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# views.py
from rest_framework.generics import ListAPIView
from .models import Program, Team
from .serializers import ProgramSerializer, TeamSerializer

class ProgramListView(ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team
from .serializers import TeamSerializer

class TeamListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, program_id=None, *args, **kwargs):
        # Filter teams by program_id if provided
        if program_id:
            teams = Team.objects.filter(program=program_id)
        else:
            teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Program, Team, Employee, Timesheet
from .serializers import ProgramSerializer, TeamSerializer, EmployeeSerializer, TimesheetSerializer

@api_view(["GET"])
def get_programs(request):
    programs = Program.objects.all()
    serializer = ProgramSerializer(programs, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

@api_view(["GET", "POST"])
def manage_employees(request):
    if request.method == "GET":
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        team = Team.objects.get(team_id=data["team"])
        employee = Employee.objects.create(employee_name=data["employee_name"], team=team)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

@api_view(["GET"])
def get_timesheets(request):
    timesheets = Timesheet.objects.all()
    serializer = TimesheetSerializer(timesheets, many=True)
    return Response(serializer.data)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({"access_token": access_token}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # For JWT, blacklisting can be implemented to invalidate the token
            token = request.data.get('access_token')
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()  # Blacklist the refresh token (logout)
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
