__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'accounts.views.home_view', name='home'),
    url(r'^sign_up/$', 'accounts.views.sign_up_view', name='sign_up'),
    url(r'^log_in/$', 'accounts.views.log_in_view', name='log_in'),
    url(r'^log_out/$', 'accounts.views.log_out_view', name='log_out'),
    # url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
)