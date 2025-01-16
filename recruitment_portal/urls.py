from django.contrib import admin
from django.urls import path
from recruitment_portal.views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  # path('api/candidate-input',CandidateFormListCreate.as_view(),name='candidate-input'),
  # path('', landing_page, name='landing_page'),
  path('common_page/',common_page, name='common_page'),
  path('login/', login_page, name='login'),
  path('logout/',logout_page,name="logout"),
  # path('candidate_details/<id>/', candidate_details , name="details"),
  # path('add_candidate/', add_candidate, name='add_candidate'),
  # path('edit/<id>/',editCandidate,name='editCandidate'),
  # path('delete/<id>/',delete,name='delete'),
  # path('add_feedback/<id>/',add_feedback,name='add_feedback'),
  path('team_manager_leads/',leads_managers,name='leads_managers'),
  # path('ta_managers/',ta_managers,name='ta_managers'),
  # path('ta_members/',ta_members,name='ta_members'),
  # path('add_ta_member/',add_ta_member, name='add_ta_member'),
  path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
  path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
  path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
  path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
  path('register-member/', register_member, name='register_member'),
  # path('register_ta_member/', register_ta_member, name='register_ta_member'),
  # path('poc/',poc, name="poc"),
  path('api/timesheet/',TimesheetView.as_view(), name="timesheet"),
  # path('add_interviewer/', views.add_interviewer, name='add_interviewer'),
  path('api/programs/', ProgramListView.as_view(), name='programs_list'),
  path('api/teams/', TeamListView.as_view(), name='team-list'),
  path('api/teams/<int:program_id>/', TeamListView.as_view(), name='team-list-by-program'),
  # path("api/programs/", views.get_programs, name="get_programs"),
  # path("api/teams/", views.get_teams, name="get_teams"),
  path("api/employees/", views.manage_employees, name="manage_employees"),
  # path("api/timesheets/", views.get_timesheets, name="get_timesheets"),
  path('api/login/', LoginView.as_view(), name='login'),
  path('api/logout/', LogoutView.as_view(), name='logout'),

]



