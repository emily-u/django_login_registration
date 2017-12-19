from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

#================================================#
#                 RENDER METHODS                 #
#================================================#

def index(request):
    return render(request,'loginregistration/index.html')


def success(request):
    try:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request,'loginregistration/result.html',context)

    except KeyError:
        return redirect('/')
    

#================================================#
#                PROCESS METHODS                 #
#================================================#

def regis(request):
    result = User.objects.regis_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')

def login(request):
    result = User.objects.login_validator(request.POST)
    if not result:
        messages.error(request, "login info invalid")
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        messages.success(request, "Successfully logged in!")
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')