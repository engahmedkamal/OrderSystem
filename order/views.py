from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, OrderForm, OrderDetailForm
from .models import Order, OrderDetail
from django.shortcuts import render, get_object_or_404



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


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_name = 'order/orderMainPage.html'
    order_detail_grouped_by_user = dict()
    for obj in order.orderdetail_set.all():
        order_detail_grouped_by_user.setdefault(obj.user, []).append(obj)
    return render(request, template_name, {'order': order, 'order_detail': order_detail_grouped_by_user})


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

def delete_orderDetail(request, order_id):
    OrderDetail.objects.filter(user__id=request.user.id,order__id=order_id).delete()
    return order_detail_view(request, order_id)

def order_sum(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_name = 'order/orderSumPage.html'
    orders_dict={}
    for orderDet in order.orderdetail_set.all():
        if orders_dict.has_key(orderDet.item_name) :
            orders_dict[orderDet.item_name] =  orders_dict.get(orderDet.item_name)+orderDet.quantity
        else:
            orders_dict[orderDet.item_name] = orderDet.quantity
    return render(request, template_name, {'order': order, 'order_details': orders_dict})
