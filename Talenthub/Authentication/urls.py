from django.urls import path,include
from .views import *
urlpatterns = [
    path("",dashboard),
    path('register/',register,name='register'),
     path('login/',login,name='login'),
     path('otp/',verification,name='otp'),
     path('nav/',navbar,name='nav'),
     path('profile/',profile,name='profile'),
     path('logout/',logout,name='logout'),
     path("addjob/",addjob,name='add_job'),
     path("list/",create_job,name="lists"),
     path('applicants/<int:job_id>/',showparticipants, name='applicants_job'),
     path('update/<int:user_id>/<int:job_id>/',statusupdate,name='update_status'),
     path('interviews/',interviews,name='interview'),
     path("openings/",openings,name='openings'),
     path('job/<int:job_id>/', job_detail, name='application'),
     path("applied_jobs/",applied_jobs,name="applied"),
]