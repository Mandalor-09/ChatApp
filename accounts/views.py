from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import HttpResponseRedirect

class Register(View):

    def get(self, request, *args, **kwargs):
        return render(request,'accounts/register.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        user = User.objects.filter(username=username)
        
        if password1 != password2:
            messages.warning(request,'Password MisMatched')
            return HttpResponseRedirect(request.path_info)
        elif user.exists():
            messages.warning(request,'User Exist... Pls Login')
            return HttpResponseRedirect(request.path_info)
        else:   
            user = User(username = username)
            user.set_password(password1)
            user.save()

            return redirect('login')


class Login(View):

    def get(self, request, *args, **kwargs):
        return render(request,'accounts/login.html')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)
        user = User.objects.filter(username = username)

        if not user.exists():
            print('User does not exist')
            messages.warning(request,'User Doesnot Exist... Pls Register')
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            messages.warning(request,'Invalid Crediential')
            return HttpResponseRedirect(request.path_info)
        login(request,user)
        messages.success(request,'Login Succesfully')
        return redirect('home')
