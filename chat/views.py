from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve, reverse
from .models import Chat,  Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json

@login_required(login_url='/login/')
def index(request):
    """
    This function renders the entry site with a list of chat rooms.
    """
    chat_rooms = Chat.objects.all()
    return render(request, "chat/index.html", {'chat_rooms': chat_rooms})


@login_required(login_url='/login/')
def room(request, room_slug):
    """
    This functions renders the room.
    """
    room_name = room_slug.replace('-', ' ').title()

    chat, created = Chat.objects.get_or_create(slug=room_slug, defaults={'room_name': room_name})

    messages = Message.objects.filter(chat=chat).order_by('created_at')
    
    return render(request, "chat/room.html", {"room_name": chat.room_name, "slug": chat.slug,"messages": messages})


def login_view(request):
    """
    This function processes the login request and returns a JSON response for POST and a HTTP for other requests.
    """
    redirect = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': redirect or '/chat/'}, safe=False, content_type='application/json')
        else:
            return JsonResponse({'success': False, 'message': 'Wrong username or password'}, safe=False, content_type='application/json')
    else:
        return render(request, 'auth/login.html', {'redirect': redirect})


def register_view(request):
    """
    This functions processes the register request and returns a JSON response for POST and a HTTP for other requests.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('repeat_password')
        try:
            if password == repeatPassword:
                User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                return JsonResponse({'success': True, 'redirect': '/login/'}, safe=False, content_type='application/json')
            else:
                return JsonResponse({'success': False, 'passwordNoMatch': True}, safe=False, content_type='application/json')
        except Exception as e:
                return JsonResponse({'success': False, 'error': True}, safe=False, content_type='application/json')
    else:
        return render(request, 'auth/register.html')


def logout_view(request):
    """
    This functions initates logout and returns to login.html.
    """
    logout(request)
    return HttpResponseRedirect('/login/')


def imprint_view(request):
    """
    This functions renders the imprint.html.
    """
    return render(request, 'legal/imprint.html')


def privacy_policy_view(request):
    """
    This functions renders the privacy_policy.html.
    """
    return render(request, 'legal/privacy_policy.html')