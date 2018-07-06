from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        """Return five users."""
        return User.objects.all()[:5]


# def index(request):
#   return render(request, 'user/index.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return render(request, 'user/index.html', {
            'message': f"{username} your acc was create, you can log in now."
        })
    else:
        return render(request, 'user/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'user/login.html', {'message': 'Invalid data'})
    else:
        return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_view(request):
    if not request.user.is_authenticated:
        return render(request, 'user/login.html', {'message': 'You have to login'})
    else:
        return render(request, 'user/user.html', {
            'user': request.user
        })
