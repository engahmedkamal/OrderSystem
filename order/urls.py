from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create_order/$', views.create_order, name='create_order'),
    url(r'^delete_album/(?P<order_id>[0-9]+)$', views.delete_order, name='delete_order'),
    url(r'^user_order/(?P<order_id>[0-9]+)$', views.user_order, name='user_order'),
    url(r'^create_user_item/(?P<order_id>[0-9]+)$', views.create_user_item, name='create_user_item'),
    url(r'^delete_user_item/(?P<order_id>[0-9]+)/(?P<user_item_id>[0-9]+)$', views.delete_user_item, name='delete_user_item'),
]
