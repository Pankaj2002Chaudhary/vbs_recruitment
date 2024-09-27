from django.contrib import admin
from django.urls import path
from recruitment_portal.views import *
urlpatterns = [
  path('api/candidate-input',CandidateFormListCreate.as_view(),name='candidate-input'),
  path('', home, name='home'),
  path('login/', login_page, name='login'),
  path('candidate_details/', candidate_details , name="details"),
  path('add_candidate/', add_candidate, name='add_candidate'),
]
