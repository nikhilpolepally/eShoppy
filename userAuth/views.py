from django.shortcuts import redirect, render
from django.contrib import messages
import urllib.request
import urllib
import json
from django.views import View
import requests
import urllib3

from eShoppy import settings
from .utils import TokenGenerator, contains_special_characters, generate_token, check_password_complexity
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        if contains_special_characters(firstname) == True:
            messages.warning(
                request, "Special characters not allowed in first name")
            return render(request, 'signup.html')
        if contains_special_characters(lastname) == True:
            messages.warning(
                request, "Special characters not allowed in last name")
            return render(request, 'signup.html')
        if check_password_complexity(password) == False:
            messages.warning(
                request, "Password should contains minimm 8 letters including alpha numerical & special characters")
            return render(request, 'signup.html')
        try:
            if User.objects.get(username=email):
                messages.info(request, "Please choose different email")
                return render(request, 'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(
            email=email, username=email, password=password, first_name=firstname, last_name=lastname)
        user.is_active = True
        user.save()
        messages.success(
            request, f"Your account created successfully. Plase login")
        return redirect('/account/login/')
    return render(request,"signup.html")
    



# Login


def userLogin(request):
    if request.method == "POST":
        print(list(request.POST.items()))
        username = request.POST['email']
        userpassword = request.POST['password']
        myuser = authenticate(username=username, password=userpassword)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/account/login')
    return render(request, 'login.html')

# Logout


def Userlogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/account/login')




