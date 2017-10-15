from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^delete_order/(?P<order_id>[0-9]+)$', views.delete_order, name='delete_order'),
    url(r'^main_order/(?P<order_id>[0-9]+)/', views.order_detail_view, name='main_order'),
    url(r'^user_order/(?P<order_id>[0-9]+)/', views.order_detail_view, name='user_order'),
    url(r'^delete_user_order/(?P<order_id>[0-9]+)$', views.delete_orderDetail, name='delete_user_order'),
    url(r'^order_sum/(?P<order_id>[0-9]+)/', views.order_sum, name='order_sum'),
    url(r'^order_sum_redirect/(?P<order_id>[0-9]+)/', views.order_sum_redirect, name='order_sum_redirect'),
]
