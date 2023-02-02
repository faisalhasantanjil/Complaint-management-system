from ast import Return
from .tokens import generate_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from compsys import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
import json
import re
from django.views.generic import ListView
from multiprocessing import context

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from compsys.info import EMAIL_HOST_USER
# from requests import request

# Create your views here.


def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None


@login_required
def home(request):
    current_user = request.user
    alluser = Userlogin.objects.all()
    alluser = list(alluser)
    for user in alluser:
        if user.email == current_user.email or user.name == current_user.first_name:
            context = {'users': user}
            return render(request, 'home/home.html', context)

    return redirect('/registerinfo')


@login_required
def lodgecomplain(request):

    current_user = request.user
    alluser = Userlogin.objects.all()
    alluser = list(alluser)
    for user in alluser:
        if user.email == current_user.email:
            lodger = user.id

    if request.method == "POST":
        reason = request.POST.get('reason')
        perpenetrer = request.POST.getlist('accuser[]')
        reviewer = request.POST.get('reviewer[]')
        image = request.FILES.get('image')

        for user in alluser:
            for i in range(len(perpenetrer)):
                if user.id == perpenetrer[i]:
                    print(user.id)
                    perpenetrer[i] = perpenetrer[i] + ":" + user.name

        print(perpenetrer)
        print(reviewer)
        print(lodger)
        complainlodge = Complains.objects.create(
            lodger=lodger, perpenetrer=perpenetrer, reviewer=reviewer, reason=reason, image=image)
        complainlodge.save()

        return redirect('/home')


def reviewcomplain(request):
    alluser = Userlogin.objects.all()
    faculty = alluser.filter(role="Faculty")
    faculty = list(faculty)
    current_user = request.user
    print("Current user:", current_user.username)
    print(faculty)

    for fac in faculty:
        if fac.email == current_user.email:
            print("test:", current_user.username)
            print("test2:", fac.name)
            return render(request, 'home/reviewcomplain.html')

    return redirect('/home')


def complainlist(request):
    current_user = request.user
    usr = Userlogin.objects.get(email=current_user.email)
    complains = Complains.objects.filter(lodger=usr.id)
    comp = Complains.objects.all().first()
    print(type(comp.perpenetrer))

    return render(request, 'home/complainlist.html', {'complain': complains})


def complain(request, pk_test):
    complain = Complains.objects. get(id=pk_test)
    reviewer = Userlogin.objects.get(id=complain.reviewer)

    context = {'complain': complain, 'reviewername': reviewer}
    return render(request, 'home/complain.html', context)


def reviewlist(request):
    current_user = request.user
    usr = Userlogin.objects.get(email=current_user.email)
    complains = Complains.objects.filter(
        reviewer=usr.id)
    comp = Complains.objects.all().first()

    return render(request, 'home/reviewlist.html', {'complain': complains})


def review(request, pk_test):
    complain = Complains.objects. get(id=pk_test)
    reviewer = Userlogin.objects.get(id=complain.reviewer)
    current_user = request.user
    lodger = Userlogin.objects.get(id=complain.lodger)
    if request.method == "POST":
        comment = request.POST['comment']
        status = request.POST.get('status[]')
        complain.status = status
        complain.comment = comment
        complain.save()
        # email
        subject = "Update on your Complain"
        message = comment
        from_email = settings.EMAIL_HOST_USER
        to_list = [current_user.email, lodger.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('/home')

    context = {'complain': complain, 'reviewername': reviewer}
    return render(request, 'home/review.html', context)


def updatecomplain(request, pk_test):
    complain = Complains.objects. get(id=pk_test)
    if request.method == "POST":
        comment = request.POST['comment']
        status = request.POST.get('status[]')
        complain.status = status
        complain.comment = comment
        complain.save()
        return redirect('/home')

    return render(request, 'home/home.html')


def registerinfo(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role[]')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        id = request.POST.get('id')
        image = request.FILES.get('image')
        myuser = User.objects.create_user(username, email, pass1)

        usersave = Userlogin.objects.create(
            name=username, email=email, role=role, id=id, image=image)

        myuser.is_active = False
        myuser.save()
        usersave.save()

        # email
        subject = "Confirmation email"
        message = "Welcome! click here to confirm"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        current_site = get_current_site(request)
        email_subject = "confirm your email to site"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),

        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('/home')

    return render(request, 'home/registerinfo.html')


def signin(request):

    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate_user(email, password)

        if user is not None:
            if user.is_active:
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/home')

            else:
                return redirect('/signin')

        else:
            return redirect('/signin')

    return render(request, 'home/signin.html')


def signout(request):
    logout(request)
    return redirect('/signin')


class InfoListView(ListView):
    model = Userlogin
    template_name = 'home/lodgecomplain.html'

    def get_context_data(self, **kwargs):
        alluser = Userlogin.objects.all()
        faculty = alluser.filter(role="Faculty")

        context = super().get_context_data(**kwargs)
        context["qs_json2"] = json.dumps(list(faculty.values()))
        context["qs_json"] = json.dumps(list(Userlogin.objects.values()))
        return context


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/home')

    else:
        return render(request, 'activation_failed.html')


class InfoListView2(ListView):
    model = Userlogin
    template_name = 'home/lodgeforuser.html'

    def get_context_data(self, **kwargs):
        alluser = Userlogin.objects.all()
        faculty = alluser.filter(role="Faculty")

        context = super().get_context_data(**kwargs)
        context["qs_json2"] = json.dumps(list(faculty.values()))
        context["qs_json"] = json.dumps(list(Userlogin.objects.values()))
        return context


def lodgingforuser(request):

    if request.method == "POST":
        reason = request.POST.get('reason')
        perpenetrer = request.POST.getlist('accuser[]')
        # perpenetrer = list(map(int, perpenetrer))
        reviewer = request.POST.get('reviewer[]')
        lodger = request.POST.get('lodger[]')
        image = request.FILES.get('image')

        print(perpenetrer)
        print(reviewer)
        print(lodger)
        complainlodge = Complains.objects.create(
            lodger=lodger, perpenetrer=perpenetrer, reviewer=reviewer, reason=reason, image=image)
        complainlodge.save()

        return redirect('/home')
