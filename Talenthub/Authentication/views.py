from django.shortcuts import render,HttpResponse,get_object_or_404
from django.utils import timezone
from .models import *
import random
from django.core.mail import send_mail
from django.core.files.base import ContentFile
YEAR_CHOICES = [r for r in range(1975, timezone.now().year + 4)]
def mail(subject,message,tomail):
            email_from = "dwarampudibalajireddy@gmail.com"
            recipient_list =tomail
            send_mail(subject, message, email_from, [recipient_list],fail_silently=False)
def dashboard(request):
    return render(request,"index.html")
def register(request):
    global resume1
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        if(User.objects.filter(email=email).values()):
            return render(request, "register.html", {"yrs": YEAR_CHOICES,"msg":"Mail Found"})
        password=request.POST.get('password')
        con=int(request.POST.get('cont_no'))
        adh=int(request.POST.get('ad_no'))
        if(User.objects.filter(aadhar_no=adh).values()):
            return render(request, "register.html", {"yrs": YEAR_CHOICES,"msg":"Aadhar Not Found"})
        t_s=request.POST.get('t_s')
        t_p_y=int(request.POST.get('t_p_y'))
        t_m=request.POST.get('t_m')
        i_s=request.POST.get('i_s')
        i_p_y=int(request.POST.get('i_p_y'))
        i_m=request.POST.get('i_m')
        u_s=request.POST.get('u_s')
        u_p_y=request.POST.get('u_p_y')
        u_m=request.POST.get('u_m')
        o_s_s=request.POST.get('o_s_s')
        o_s=request.POST.get('o_s')
        o_p_y=request.POST.get('o_p_y')
        o_m=request.POST.get('o_m')
        user = {
                "name":name,
                "email":email,
                "password":password,
                "contact_no":int(con),
                "aadhar_no":int(adh)
            }
        quali ={
                "tenth_school":t_s,
                "tenth_passout_year":int(t_p_y),
                "tenth_marks":t_m,
                "inter_school":i_s,
                "inter_passout_year":int(i_p_y),
                "inter_marks":i_m,
                "ug_school":u_s,
                "ug_passout_year":int(u_p_y),
                "ug_marks":u_m,
                "oth_specialisation":(o_s_s if o_s_s else "NA"),
                "oth_school":(o_s if o_s else "NA"),
                "oth_passout_year":(int(o_p_y) if o_s!=1975 else 0),
                "oth_marks":(o_m if o_s else "NA"),
        }
        request.session['user']=user
        request.session['quali']=quali
        request.session['zoom']=request.POST['zoomid']
        resume_file = request.FILES.get("resume")
        resume_content = resume_file.read()
        resume1 = ContentFile(resume_content, name=resume_file.name)
        otp=random.randrange(100000, 1000000)
        request.session['otp']=otp
        print(otp)
        msg= f"Tq for registered into Talent Hub!!.Your OTP is {otp}"
        mail("OTP For Verification",msg,email)
        return render(request,"otp.html")
    return render(request, "register.html",{"yrs": YEAR_CHOICES})
def verification(request):
    try:
        otpp = int(request.POST['otp'])
        exp = int(request.session["otp"])
        print(otpp, exp)
        if otpp == exp:
            user_data = request.session.get("user")
            quali_data = request.session.get("quali")
            user = User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                contact_no=user_data['contact_no'],
                aadhar_no=user_data['aadhar_no']
            )
            qua = Qualifications.objects.create(
                tenth_school=quali_data['tenth_school'],
                tenth_passout_year=quali_data['tenth_passout_year'],
                tenth_marks=quali_data['tenth_marks'],
                inter_school=quali_data['inter_school'],
                inter_passout_year=quali_data['inter_passout_year'],
                inter_marks=quali_data['inter_marks'],
                ug_school=quali_data['ug_school'],
                ug_passout_year=quali_data['ug_passout_year'],
                ug_marks=quali_data['ug_marks'],
                oth_specialisation=quali_data['oth_specialisation'],
                oth_school=quali_data['oth_school'],
                oth_passout_year=quali_data['oth_passout_year'],
                oth_marks=quali_data['oth_marks']
            )
            cs = Candidates_us.objects.create(
                user=user,
                qualifications=qua,
                resume=resume1,
                zoom_id=request.session.get("zoom")
            )

            return render(request, "register.html", {"yrs": YEAR_CHOICES, "msg": "Success"})
        else:
            return render(request, "register.html", {"yrs": YEAR_CHOICES, "msg": "Wrong OTP"})
    except Exception as e:
        print(str(e))
        return render(request, "register.html", {"yrs": YEAR_CHOICES, "msg": "Error occurred during verification"})
def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        x=User.objects.filter(email=email,password=password).values()
        if x:
                user=User.objects.get(email=email,password=password)
                cand=Candidates_us.objects.get(user=user)
                request.session['role']=cand.role
                request.session['email']=email
                return render(request,"nav.html",{"msg":cand.role})
        else:
            return render(request,"login.html",{"msg":"Invalid Credentaials"})
    return render(request,"login.html")  

def navbar(request):
    return render(request,'nav.html')
def profile(request):
    email=request.session.get("email")
    user=User.objects.get(email=email)
    cand_us=Candidates_us.objects.get(user=user)
    return render(request,"profile.html",{"candidate":cand_us})
def logout(request):
    request.session.flush()
    return render(request,'login.html',{"msg":"Logout Successfully"})      
def openings(request):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        jobs=Job.objects.filter(application_status=True).values
        return render(request,"openings.html",{"jobs":jobs})
    return HttpResponse("Session Time out")
def job_detail(request,job_id):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        jobs=Job.objects.filter(application_status=True).values
        job = Job.objects.get(id=job_id, application_status=True)
        user=User.objects.get(email=request.session.get("email"))
        if(JobApplicants.objects.filter(job_id=job_id,candidate_id=user.id).values()):
            return render(request, "openings.html", {"msg": f"Already Applied","jobs":jobs})
        else:
            application = JobApplicants.objects.create(
                job_id=job_id,
                candidate_id=user.id,
                status="In Progress"
            )
            mail(f"Application for {job.title} ","You applied to {job.title}.Our Talent Acquisition team will catch you soon.",request.session.get("email"))
            return render(request, "openings.html", {"msg": f"Applied for {job.title}","jobs":jobs})
    return HttpResponse("Session Time out")
def applied_jobs(request):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        user = get_object_or_404(User, email=request.session.get("email"))
        job_ids = JobApplicants.objects.filter(candidate_id=user.id).values_list('job_id', flat=True)
        print(job_ids.values)
        jobs = Job.objects.filter(id__in=job_ids)
        applied_jobs = [
            {
                'job_title': job.title,
                'company': job.company,
                'salary': job.salary,
                'status': applicant.status
            }
            for job, applicant in zip(jobs, JobApplicants.objects.filter(candidate_id=user.id, job_id__in=job_ids))
        ]
        return render(request, "appliedjobs.html", {"jobs": applied_jobs})
    return HttpResponse("Session Time out")
def addjob(request):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            company = request.POST.get('company')
            location = request.POST.get('location')
            salary = request.POST.get('salary')
            email=request.session.get("email")
            print(email)
            user=User.objects.get(email=email)
            Job.objects.create(
                title=title,
                description=description,
                company=company,
                location=location,
                salary=salary,
                application_deadline=request.POST.get('deadline'),
                posted_by = user
            )
            return render(request,"addjob.html",{"msg":"Added Successfully"})
        return render(request,"addjob.html")
    return HttpResponse("Session Time out")


def create_job(request):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        email=request.session.get("email")
        user_id=User.objects.get(email=email)
        jobs=Job.objects.filter(posted_by=user_id)
        return render(request,"created_jobs.html",{"jobs":jobs})
    return HttpResponse("Session Time out")
def showparticipants(request, job_id):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        applicants = JobApplicants.objects.filter(job_id=job_id)
        users = User.objects.filter(id__in=[applicant.candidate_id for applicant in applicants])
        return render(request, 'show_participants.html', {'users': users,"jj":job_id})
    return HttpResponse("Session Time out")
def statusupdate(request,user_id,job_id):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        if request.method=='POST':
            print("Hello")
            return HttpResponse(J.status)
        print(user_id,job_id)
        J = JobApplicants.objects.get(job_id=job_id,candidate_id=user_id)
        request.session['update_user_id']=user_id
        request.session['update_job_id']=job_id
        user=User.objects.get(id=user_id)
        cand=Candidates_us.objects.get(user=user)
        print(J.status)
        print(cand.zoom_id)
        return render(request,"interview_schedule.html",{"status":J.status,"zoom_id":cand.zoom_id})
    return HttpResponse("Session Time out")
def interviews(request):
    if request.session['role']==Candidates_us.objects.get(user=User.objects.get(email=request.session['email'])).role:
        if request.method=='POST':
            interview_date=request.POST['date']
            zoom_id=request.POST['zoomId']
            promotion=request.POST['promotion']
            user_id=request.session['update_user_id']
            user_mail=User.objects.get(id=user_id).email
            J = JobApplicants.objects.get(job_id=request.session['update_job_id'],candidate_id=request.session['update_user_id'])
            mail("Job Update",f"You are selected for {promotion}.We schedule a interview call with you on {interview_date} in Zoom.Zoom Id:{zoom_id}. All the Best",user_mail)
            print(f"You are selected for {promotion}.We schedule a interview call with you on {interview_date} in Zoom {zoom_id}. All the Best")
            J.status=promotion
            J.save()
            return render(request,"interview_schedule.html",{"status":J.status,"zoom_id":zoom_id})
    return HttpResponse("Session Time out")
  