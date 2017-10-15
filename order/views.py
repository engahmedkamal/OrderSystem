from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, OrderForm, OrderDetailForm
from .models import Order, OrderDetail


def redirect_to_index(request):
    orders = Order.objects.all().order_by('timestamp');
    return render(request, 'order/index.html', {'orders': orders})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'order/login.html')
    else:
        return redirect_to_index(request)


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
                return redirect_to_index(request)
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
            return redirect_to_index(request)
    return render(request, 'order/register.html', {'form': form})


def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.creator = request.user
        order.save()
        return redirect_to_index(request)
    return render(request, 'order/create_order.html', {'form': form})


def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect_to_index(request)


def user_order(request, order_id):
    user_orders = OrderDetail.objects.filter(user=request.user, order=Order.objects.filter(pk=order_id))
    return render(request,'order/user_order.html', {'user_orders' : user_orders, 'order_id' : order_id})


def create_user_item(request, order_id):
    form = OrderDetailForm(request.POST or None)
    if form.is_valid():
        order_detail = form.save(commit=False)
        order_detail.user = request.user
        order_detail.order = Order.objects.get(pk=order_id)
        order_detail.save()
        return user_order(request, order_id)
    return render(request, 'order/create_order.html', {'form' : form})


def delete_user_item(request, order_id, user_item_id):
    order_detail = OrderDetail.objects.get(pk=user_item_id)
    order_detail.delete()
    return user_order(request, order_id)
