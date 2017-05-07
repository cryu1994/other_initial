from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^add$', views.add),
    url(r'^add_items$', views.add_new),
    url(r'^show/(?P<id>\d+)$', views.show_item),
    url(r'^add_list/(?P<id>\d+)$', views.add_to_my_list),
    url(r'^delete/(?P<id>\d+)$', views.destroy)
]
