from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Group,Messages
from accounts.models import Friend
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.contrib.auth.decorators import login_required


class Home(LoginRequiredMixin,View):
    login_url = 'login'
    
    def get(self, request, *args, **kwargs):
        username = request.user
        user = User.objects.get(username=username)
        name1 = user.username 
        friends = None
        # print(user,'<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>')
        try:
            friends = Friend.objects.get(user=user).friends.all()
        except Exception as e:
            print(e)
        # print(friends,'<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>')
        context = {
            'user':user,
            "friends":friends
        }


        if request.GET.get('userid') is not None:
            userid = request.GET.get('userid')
            # print(userid,'<<<<<<<<<<<<<<<<>>>>>>>>>>>>')
            person = User.objects.get(id = userid)
            name2 = person.username
            context['person']=person
            q1_name = f'{name1}{name2}'
            q2_name = f'{name2}{name1}'
            try:
                group = Group.objects.get(models.Q(name=q1_name) | models.Q(name=q2_name))
                # print(group,"hladlafdahldfhafd")
                # print(person)
                messages = Messages.objects.filter(group=group)
                context['messages']=messages
            except Exception as e:
                print(e)
            # print('Message',message)
        
        print(context)
        return render(request,'app/chat_app.html',context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        admin = User.objects.get(username=user)
        friends = Friend.objects.filter(user=admin)
        user2 = request.POST.get('userid')
        user2 = User.objects.get(id = user2)
        if friends.exists():
            friend = Friend.objects.get(user = admin)
            friend.friends.add(user2)
            friend.save()
            friend = Friend.objects.get(user = user2)
            print(friend,'>>>>>>>>>>>>>>>>>>>>')
            friend.friends.add(admin)
            friend.save()
            return redirect('home')
        friend = Friend.objects.create(user=admin)
        friend.friends.add(user2)
        friend.save()
        friend = Friend.objects.get(user = user2)
        friend.friends.add(admin)
        friend.save()
        return redirect('home')

@login_required
def Friends(request):
    login_url = 'login'
    context = {}
    search = request.GET.get('search-name')
    if not search:
        searchedfriends = User.objects.all()
        context['searchedfriends']=searchedfriends
        return render(request, 'app/friends.html',context=context)

    else:
        print(search,"adadaassdfdsaffs")
        searchedfriends = User.objects.filter(username__icontains=search)
        if searchedfriends is None:
            return HttpResponse('No such user')
        else:  
            context['searchedfriends']=searchedfriends
            return render(request, 'app/friends.html',context=context)
