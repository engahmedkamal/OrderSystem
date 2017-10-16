from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, OrderForm, OrderDetailForm
from .models import Order, OrderDetail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import datetime


def redirect_to_index(request):
    orders = Order.objects.all().order_by('timestamp').reverse();
    search_text = request.GET.get("search_text")
    if search_text:
        orders = orders.filter(
            Q(restaurant_name__contains=search_text)
        ).distinct()
        return render(request, 'order/index.html', {'orders': orders, 'search_text': search_text})
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
    template_name = 'order/order_main_page.html'
    users_order_details = user_order_details_for_order(order)
    context = {'order': order, 'order_detail': users_order_details}
    if order.status == '2':
        context['user_costs'] = calculate_user_price(order, users_order_details)
    return render(request, template_name, context)


def calculate_user_price(order, user_order_details):
    dic = {}
    delivery_fees = order.delivery_fees / len(user_order_details)
    tax_percentage = order.tax_percentage
    for user, order_details in user_order_details.items():
        total_cost = delivery_fees
        for order_detail in order_details:
            total_cost += order_detail.price
        total_cost += (total_cost * tax_percentage) / 100
        dic[user.id] = str(total_cost)
    return dic


def user_order_details_for_order(order):
    dic = {}
    for order_detail in order.orderdetail_set.all():
        if not dic.has_key(order_detail.user):
            dic[order_detail.user] = []
        dic[order_detail.user].append(order_detail)
    return dic;


def create_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.creator = request.user
        order.save()
        return redirect_to_index(request)
    return render(request, 'order/create_order.html', {'form': form})


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        order = form.save(commit=False)
        order.save()
        return redirect_to_index(request)
    return render(request, 'order/edit_order.html', {'form': form, 'order_name': order.restaurant_name})


def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect_to_index(request)


def user_order(request, order_id):
    user_orders = OrderDetail.objects.filter(user=request.user, order=Order.objects.filter(pk=order_id))
    return render(request, 'order/user_order.html', {'user_orders': user_orders, 'order_id': order_id})


def create_user_item(request, order_id):
    form = OrderDetailForm(request.POST or None)
    if form.is_valid():
        order_detail = form.save(commit=False)
        order_detail.user = request.user
        order_detail.order = Order.objects.get(pk=order_id)
        order_detail.save()
        return user_order(request, order_id)
    return render(request, 'order/create_user_item.html', {'form': form})


def edit_user_item(request, user_item_id):
    order_detail = get_object_or_404(OrderDetail, id=user_item_id)
    form = OrderDetailForm(request.POST or None, instance=order_detail)
    if form.is_valid():
        order_detail = form.save(commit=False)
        order_detail.save()
        return user_order(request, order_detail.order.id)
    return render(request, 'order/edit_user_item.html', {'form': form, 'item_name': order_detail.item_name})


def delete_user_item(request, order_id, user_item_id):
    order_detail = get_object_or_404(OrderDetail, id=user_item_id)
    order_detail.delete()
    return user_order(request, order_id)


def delete_user_order(request, order_id):
    OrderDetail.objects.filter(user__id=request.user.id, order__id=order_id).delete()
    return order_detail_view(request, order_id)


def group_order_details_by_item_value(order):
    orders_dict = {}
    for orderDet in order.orderdetail_set.all():
        if orders_dict.has_key(orderDet.item_name):
            orders_dict[orderDet.item_name] = orders_dict.get(orderDet.item_name) + orderDet.quantity
        else:
            orders_dict[orderDet.item_name] = orderDet.quantity
    return orders_dict


def order_sum(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 1
    order.save()
    template_name = 'order/order_sum_page.html'
    orders_dict = group_order_details_by_item_value(order)
    return render(request, template_name, {'order': order, 'order_details': orders_dict})


def order_sum_redirect(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery_time = request.POST['delivery_time']
    if delivery_time and int(delivery_time) >= 15:
        order.delivery_time = int(delivery_time)
    else:
        orders_dict = group_order_details_by_item_value(order)
        return render(request, 'order/order_sum_page.html', {'order': order, 'order_details': orders_dict, 'delivery_time_error': True})
    order.ordered_at = datetime.datetime.now()
    order.status = 2
    order.save()
    return order_detail_view(request, order_id)


def enter_order_values(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_name = 'order/order_sum_page.html'
    orders_dict = group_order_details_by_item_value(order)
    return render(request, template_name, {'order': order, 'order_details': orders_dict})


def order_reopen(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 0
    order.save()
    return order_detail_view(request, order_id)
