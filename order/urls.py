from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^main_order/(?P<order_id>[0-9]+)/', views.order_detail_view, name='main_order'),
    url(r'^order_detail/(?P<order_id>[0-9]+)/', views.order_detail_view, name='order_detail'),
]
