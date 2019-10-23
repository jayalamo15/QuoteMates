from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new_quote$', views.new_quote),
    url(r'^quote/(?P<quote_id>\d+)/like$', views.like_quote),
    url(r'^myaccount/(?P<user_id>\d+)$', views.edit_account),
    url(r'^myaccount/(?P<user_id>\d+)/update$', views.update_account),
    url(r'^user/(?P<user_id>\d+)$', views.show_user),
    url(r'^quote/(?P<quote_id>\d+)/delete$', views.delete)
]