from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import random
 
# Create your views here.


def register(request):
    EUFO=UserForm()
    EPFO=ProfileForm()
    d={'EUFO':EUFO,'EPFO':EPFO}
    if request.method=='POST'and request.FILES:
        UFDO=UserForm(request.POST)
        PFDO=ProfileForm(request.POST,request.FILES)
        if UFDO.is_valid()and PFDO.is_valid():
            pw=UFDO.cleaned_data.get('password')
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            # message = f"Hello {UFDO.cleaned_data.get('first_name')}\n \t Your Registration against our application is successfully Done with username:{UFDO.cleaned_data.get('username')} \n\n \t\t Thanks & regards \n \t\tTeam"
            message =f"hello bikash dash \n \t whats your plan tomorrow? \n\n THANKS & REGARDS\n by aryan"
            # message=f"helo manoj mg \n \t tu mg ta? \n\n THANKS & REGRADES\n by to jeje"
            email = UFDO.cleaned_data.get('email')
            send_mail(
                'Registration Successfull',
                message,
                'sumantaparida606@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponse('done')
        return HttpResponse('invalid register')

    return render(request,'register.html',d)


def user_login(request):
    if request.method=='POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        AUO=authenticate(username=un,password=pw)
        if AUO:
            login(request,AUO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse('invalid credentials')
    return render(request,'user_login.html')


def home(request):
    un=request.session.get('username')
    if un:
        UO=User.objects.get(username=un)
        d={'UO':UO}
        return render(request,'home.html',d)
    return render(request,'home.html')


def user_profile(request):
    un=request.session.get('username')
    if un:
        UO=User.objects.get(username=un)
        PO=Profile.objects.get(username=UO)
        d={'UO':UO,'PO':PO}
        return render(request,'user_profile.html',d)
    return render(request,'user_profile.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def forget_password(request):
    if request.method=='POST':
        otp=random.randint(1100,9999)
        un=request.POST.get('un')
        request.session['username']= un
        request.session['otp']= otp
        UO=User.objects.get(username=un)
        if UO:
            email=UO.email
            message=f"Hello{UO.first_name} The request for changing the password has been processed successfully\n please enter the otp(one time password): {otp} to confirm its you \n\n please do not share the otp with any one"
            send_mail(
                'request to change',
                message,
                'sumantaparida606@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('otp'))
        return HttpResponse('user not found')
    return render(request,'forget_password.html')


def otp(request):
    if request.method=='POST':
        uotp=request.POST.get='otp'
        gotp=request.session.get='otp'
        if uotp==str(gotp):
            return HttpResponseRedirect(reverse(new_password))
        return HttpResponse('invalid otp')
    return render(request,'otp.html')


def new_password(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        cpw = request.POST.get('cpw')
        if pw == cpw:
            un = request.session.get('username')
            print(un,'3'*30)
            UO = User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('Password doesnot match')
    return render(request, 'new_password.html')


def change_password(request):
    if request.method=='POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            un=request.session.get('username')
            uo=User.objects.get(username=un)
            uo.set_password(pw)
            uo.save()
            return HttpResponseRedirect(reverse(user_login))
        return HttpResponse('pw& cpw missmatch')

    return render (request,'change_password.html')

