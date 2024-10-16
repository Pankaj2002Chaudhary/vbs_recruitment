from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Interviewer)
admin.site.register(Program)
admin.site.register(Team)
admin.site.register(Manager)
admin.site.register(Employee)
admin.site.register(POC)
admin.site.register(TATeam)
admin.site.register(TAManager)
admin.site.register(TAMember)
admin.site.register(Feedback)