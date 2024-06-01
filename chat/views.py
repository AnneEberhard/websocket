from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Chat,  Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def index(request):
    """
    Renders the chat index page that lists all available chat rooms.
    Requires user to be authenticated to access this page.

    :param request: HttpRequest object.
    :return: HttpResponse object with the rendered template.
    """
    chat_rooms = Chat.objects.all()
    return render(request, "chat/index.html", {'chat_rooms': chat_rooms})


@login_required(login_url='/login/')
def room(request, room_slug):
    """
    Renders a specific chat room identified by a slug. If the room does not exist, it is created.
    Requires user to be authenticated to access this page.

    :param request: HttpRequest object.
    :param room_slug: The slug of the chat room to render.
    :return: HttpResponse object with the rendered template.
    """
    room_name = room_slug.replace('-', ' ').title()

    chat, created = Chat.objects.get_or_create(slug=room_slug, defaults={'room_name': room_name})

    messages = Message.objects.filter(chat=chat).order_by('created_at')
    
    return render(request, "chat/room.html", {"room_name": chat.room_name, "slug": chat.slug,"messages": messages})


def login_view(request):
    """
    Processes the login request. If POST, it authenticates the user and returns a JSON response.
    If not POST, returns the login page.

    :param request: HttpRequest object.
    :return: JsonResponse if POST, otherwise HttpResponse with rendered template.
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
    Handles the registration of new users. If POST, it processes the form data, attempts to create a new user,
    and returns a JSON response. If not POST, returns the registration page.

    :param request: HttpRequest object.
    :return: JsonResponse if POST, otherwise HttpResponse with rendered template.
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
    Logs out the current user and redirects to the login page.

    :param request: HttpRequest object.
    :return: HttpResponseRedirect to the login page.
    """
    logout(request)
    return HttpResponseRedirect('/login/')


def imprint_view(request):
    """
    Renders the imprint page.

    :param request: HttpRequest object.
    :return: HttpResponse with the rendered template.
    """
    return render(request, 'legal/imprint.html')


def privacy_policy_view(request):
    """
    Renders the privacy policy page.

    :param request: HttpRequest object.
    :return: HttpResponse with the rendered template.
    """
    return render(request, 'legal/privacy_policy.html')