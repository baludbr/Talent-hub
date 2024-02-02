from django.contrib import admin
from .models import *
# Register your models here.
models_to_register = [User, Qualifications, Candidates_us]
for i in models_to_register:
    admin.site.register(i)
admin.site.register(Job)
admin.site.register(JobApplicants)