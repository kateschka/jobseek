from django.contrib import admin
from .models import Job, Interview, Company, Recruiter, JobHistory

admin.site.register(Job)
admin.site.register(Interview)
admin.site.register(Company)
admin.site.register(Recruiter)
admin.site.register(JobHistory)
