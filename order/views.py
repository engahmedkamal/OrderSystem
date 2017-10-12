from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, OrderForm
from .models import Order


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'order/login.html')
    else:
        return render(request, 'order/index.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'order/login.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'order/index.html')
            else:
                return render(request, 'order/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'order/login.html', {'error_message': 'Invalid login'})
    return render(request, 'order/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'order/index.html')
    return render(request, 'order/register.html', {'form': form})


def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.creator = request.user
        order.save()
    return render(request, 'order/create_order.html', {'form': form})
