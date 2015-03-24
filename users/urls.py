__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('users.views',
    url(r'^$', 'home_view', name='home'),
    url(r'^list/$', 'list_view', name='list'),
    url(r'^requests/$', 'requests_view', name='requests'),
    url(r'^friends/$', 'friends_view', name='friends'),
    url(r'^friends/(?P<user_id>\d+)/add/$', 'add_view', name='add'),
    url(r'^friends/(?P<user_id>\d+)/accept/$', 'accept_view', name='accept'),
    url(r'^friends/(?P<user_id>\d+)/reject/$', 'reject_view', name='reject'),
    url(r'^feed/$', 'feed_view', name='feed'),
)