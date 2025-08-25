#from typing import Any

from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date

from django.conf import settings

from .models import StudentUser, Recruiter
from django.contrib import messages
from .models import Job
from django.db.models import Q
from fuzzywuzzy import process


from .models import Feedback
from .forms import FeedbackForm, AdminReplyForm

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

#from django.template.loader import render_to_string for forget process

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

#from django.core.paginator import Paginator





def index (request):
    #feedback_list = Feedback.objects.all().order_by("-created_at")
    #paginator = Paginator(feedback_list, 6)  # show 6 feedbacks per page
    #page_number = request.GET.get("page")
    #feedbacks = paginator.get_page(page_number)
    return render(request, "index.html")



@staff_member_required
def admin_jobs_view(request):
    jobs = Job.objects.all().order_by('-start_date')
    return render(request, 'admin_jobs.html', {'job': jobs})



def faqs (request):
    return render (request,'faqs.html')





#@login_required(login_url='admin_login')
def admin_login (request):
    error= ""
    if request.method=='POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error ="no"
                message = "Login Successful"
                return redirect('admin_home')

            else:
                error ="yes"
                message = "Invalid email or password."
        except:
            error="yes"
            message = "Invalid email or password."
    d = {'error':error}
    return render (request,'admin_login.html',d)



def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email'] #email=e
        company = request.POST['company']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(username=e, first_name=f, last_name=l, password=p)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=company, type="recruiter", status="pending")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'recruiter_signup.html', d)

def user_login(request):
    error = ""

    if request.method == "POST":
        u= request.POST['uname']
        p= request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
             try:
               user1 = StudentUser.objects.get(user=user)
               if user1.type =="student":
                   login(request, user)
                   error = "no"
                   return redirect(user_home)

               else:
                    error = "yes"


             except:
                 error = "yes"

    else:
        error = "yes"
        #message = "Invalid email or password."
        #redirect('user_login')
    d = {'error': error}
    return render(request, 'user_login.html', d)


def recruiter_login(request):
    error = ""

    if request.method == "POST":
        u= request.POST['uname']
        p= request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
             try:
               user1 =Recruiter.objects.get(user=user)
               if user1.type =="recruiter" and user1.status!="pending":
                   login(request, user)
                   error = "no"

               else:
                    error = "not"

             except:
                 error = "yes"

    else:
        error = "yes"

    d = {'error': error}
    return render(request, 'recruiter_login.html', d)





def user_home (request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student =StudentUser.objects.get(user=user)
    error = " "
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']

        con = request.POST['contact']
        gen = request.POST['gender']

        student.user.first_name = f
        student.user.last_name = l
        student.user.mobile = con
        student.user.gender = gen
        try:

            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            student.image = i
            recruiter.save()
            error = "no"
        except:
            pass

    d = {'student': student, 'error': error}
    return render (request,'user_home.html',d)


def admin_home (request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount=Recruiter.objects.all().count()
    scount = StudentUser.objects.all().count()
    d = {'rcount':rcount,'scount':scount}
    return render (request,'admin_home.html',d)


def recruiter_home (request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = " "
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']


        con = request.POST['contact']
        gen = request.POST['gender']

        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.user.mobile = con
        recruiter.user.gender = gen
        try:

            recruiter.save()
            recruiter.user.save()
            error = "no"
        except:
           error = "yes"

        try:
            i = request.FILES['image']
            recruiter.image = i
            recruiter.save()
            error = "no"
        except:
            pass


    d = { 'recruiter': recruiter,'error': error}
    return render (request,'recruiter_home.html',d)

def Logout (request):
      logout(request)
      return redirect('index')


def user_signup(request):
    error = " "
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(username=e, first_name=f, last_name=l, password=p)
            StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}

    return render(request, 'user_signup.html',d)


def view_users (request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    d= {'data':data}
    return render (request,'view_users.html',d)


def recruiter_pending (request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    d= {'data':data}
    return render (request,'recruiter_pending.html',d)


def add_job (request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user = request.user
        #recruiter = Recruiter.objects.get(user=user)
        recruiter = Recruiter.objects.get(user=request.user)

        try:
            Job.objects.create(recruiter=recruiter, start_date=sd, end_date=ed, title=jt, salary=sal, image=l,
                               description=des, experience=exp, location=loc, skills=skills, creationdate=date.today())
            error = "no"
        except Exception as e:
                          error = "yes"

    d = {'error': error}

    return render (request,'add_job.html',d)


def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user#for current user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'job_list.html',d)


def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    d= {'data':data}
    return render (request,'recruiter_accepted.html',d)


def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    d= {'data':data}
    return render (request,'recruiter_rejected.html',d)


def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    d= {'data':data}
    return render (request,'recruiter_all.html',d)


def delete_user (request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student = User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def delete_recruiter (request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')

def change_status (request,pid):

    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter= Recruiter.objects.get(id=pid)
    if request.method == "POST":
        s = request.POST['status']
        recruiter.status = s
        try:
          recruiter.save()
          error = "no"
          return redirect('recruiter_pending')
        except:
           error = "yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)


def change_passwordadmin (request):

    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""

    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="no"
        except:
           error="yes"

    d={'error':error}
    return render(request,'change_passwordadmin.html',d)


def change_passworduser (request):

    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""

    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="no"
        except:
           error="yes"

    d={'error':error}
    return render(request,'change_passworduser.html',d)


def change_passwordrecruiter (request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""

    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']

        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error="no"
        except:
           error="yes"

    d={'error':error}
    return render(request,'change_passwordrecruiter.html',d)


def edit_job (request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['startdate']
        ed = request.POST['enddate']
        sal = request.POST['salary']

        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']

        job.title = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description= des



        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                job.start_date = sd
                job.save()


            except:
                 pass

        else:
            pass

        if ed:
            try:
                job.end_date = ed
                job.save()


            except:
                pass

        else:
            pass

    d = {'error': error,'job':job}

    return render (request,'edit_job.html',d)



def change_companylogo (request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == 'POST':
        cl = request.FILES['logo']
        job.image = cl



        try:
            job.save()
            error = "no"
        except:
            error = "yes"

    d = {'error': error,'job':job}

    return render (request,'change_companylogo.html',d)


def latestjobs (request):
    job = Job.objects.all().order_by('-start_date')
    d = {'job':job}
    return render (request,'latestjobs.html',d)


def user_latestjobs (request):
    job = Job.objects.all().order_by('-start_date')
    user = request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)

    d = {'job':job,'li':li}
    return render (request,'user_latestjobs.html',d)


def job_detail(request,pid):
    job = Job.objects.get(id=pid)

    d = {'job':job}
    return render (request,'job_detail.html',d)

def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()
    if job.end_date<date1:
        error="close"
    elif job.start_date>date1:
        error="notopen"
    else:
        if request.method == 'POST':
            r = request.FILES['resume']
            Apply.objects.create(job=job,student=student, resume=r, applydate=date.today())
            error="done"

    d = {'error': error}

    return render (request,'applyforjob.html',d)



def appliedcandidates (request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data=Apply.objects.all()

    d = {'data': data}

    return render (request,'appliedcandidates.html',d)





def search_jobs(request):
    title_input = request.GET.get('title', '').strip()
    location_input = request.GET.get('location', '').strip()

    all_titles = Job.objects.values_list('title', flat=True).distinct()
    all_locations = Job.objects.values_list('location', flat=True).distinct()

    matched_title = process.extractOne(title_input, all_titles, score_cutoff=70)
    matched_location = process.extractOne(location_input, all_locations, score_cutoff=70)

    jobs = Job.objects.all()
    if matched_title:
        jobs = jobs.filter(title=matched_title[0])
    if matched_location:
        jobs = jobs.filter(location=matched_location[0])

    return render(request, 'search_results.html', {'jobs': jobs})


def user_jobdetail(request,pid):
    job = Job.objects.get(id=pid)

    d = {'job':job}
    return render (request,'user_jobdetail.html',d)




@login_required
def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect("user_home")
    else:
        form = FeedbackForm()
    return render(request, "submit_feedback.html", {"form": form})

@staff_member_required
def view_feedback(request):
    data = Feedback.objects.all().order_by("-created_at")
    return render(request, "view_feedback.html", {"data": data})

@staff_member_required
def reply_feedback(request, fid):
    feedback = Feedback.objects.get(id=fid)
    if request.method == "POST":
        form = AdminReplyForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect("view_feedback")
    else:
        form = AdminReplyForm(instance=feedback)
    return render(request, "reply_feedback.html", {"form": form, "feedback": feedback})

@staff_member_required
def delete_feedback(request, fid):
    Feedback.objects.get(id=fid).delete()
    return redirect("view_feedback")
''''
@login_required
def my_feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_feedbacks.html", {"my_feedbacks": feedbacks})'''''

@login_required
def my_feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_feedbacks.html", {"my_feedbacks": feedbacks})


@login_required
def recsubmit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect("recruiterr_home")
    else:
        form = FeedbackForm()
    return render(request, "recsubmit_feedback.html", {"form": form})
''''
@login_required
def recmy_feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "recmy_feedbacks.html", {"recmy_feedbacks": feedbacks})'''''

@login_required
def recmy_feedbacks(request):
    feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "recmy_feedbacks.html", {"my_feedbacks": feedbacks})





def studentuser_forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        print(" Submitted Email:", email)

        # Print all registered StudentUser emails
        all_emails = [s.user.email for s in StudentUser.objects.all()]
        print("All Registered Emails (StudentUser):", all_emails)

        # Query the user (case-insensitive)
        user = StudentUser.objects.filter(user__email__iexact=email).first()
        print(" Found User:", user)

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user.user)
            reset_link = request.build_absolute_uri(f"/reset-password/user/{uid}/{token}/")
            print(" Reset Link:", reset_link)
            messages.success(request, "Reset link generated. Check terminal.")
        else:
            messages.error(request, "Email not registered.")
        return redirect('studentuser_forgot_password')

    return render(request, "studentuser_forgot_password.html")



def recruiter_forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        print(" Submitted Email:", email)

        user = Recruiter.objects.filter(user__email__iexact=email).first()
        print(" Found Recruiter:", user)

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user.user)
            reset_link = request.build_absolute_uri(f"/reset-password/recruiter/{uid}/{token}/")
            print(" Recruiter Reset Link:", reset_link)
            messages.success(request, "Reset link generated. Check terminal.")
        else:
            messages.error(request, "Email not registered.")
        return redirect('recruiter_forgot_password')

    return render(request, 'recruiter_forgot_password.html')





def reset_password_view(request, role, uidb64, token):
    model = StudentUser if role == "user" else Recruiter
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_obj = model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, model.DoesNotExist):
        user_obj = None

    if user_obj and default_token_generator.check_token(user_obj.user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            user = user_obj.user
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful. You can now login.")
            return redirect('user_login' if role == 'user' else 'recruiter_login')
        return render(request, 'reset_password.html')
    else:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('studentuser_forgot_password' if role == 'user' else 'recruiter_forgot_password')



def delete_job (request,pid):
    if not request.job.is_authenticated:
        return redirect('job_list')
    job =Job.objects.get(id=pid)
    job.delete()
    return redirect('delete_job')