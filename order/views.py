from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from django.views import generic
from .models import Order,OrderDetail
from django.shortcuts import render,get_object_or_404

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
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            return render(request, 'order/index.html')
    return render(request,'order/register.html',{'form':form})


def order_detail_view(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    template_name = 'order/orderMainPage.html'
    order_detail_grouped_by_user = dict()
    for obj in order.orderdetail_set.all():
        order_detail_grouped_by_user.setdefault(obj.user, []).append(obj)
    return render(request,template_name,{'order':order,'order_detail':order_detail_grouped_by_user})