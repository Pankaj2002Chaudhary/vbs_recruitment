from django.contrib import admin
from django.urls import path
from recruitment_portal.views import *
from . import views



urlpatterns = [
  path('api/candidate-input',CandidateFormListCreate.as_view(),name='candidate-input'),
  path('', landing_page, name='landing_page'),
  path('common_page/',common_page, name='common_page'),
  path('login/', login_page, name='login'),
  path('logout/',logout_page,name="logout"),
  path('candidate_details/<id>/', candidate_details , name="details"),
  path('add_candidate/', add_candidate, name='add_candidate'),
  path('edit/<id>/',editCandidate,name='editCandidate'),
  path('delete/<id>/',delete,name='delete'),
  path('add_feedback/<id>/',add_feedback,name='add_feedback'),
  path('team_manager_leads/',leads_managers,name='leads_managers'),
  path('ta_managers/',ta_managers,name='ta_managers'),
  path('ta_members/',ta_members,name='ta_members'),
  path('add_ta_member/',add_ta_member, name='add_ta_member'),

]



