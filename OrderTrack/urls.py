from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('website.urls',namespace="website")),
    url(r'^admin/', include(admin.site.urls)),

   #login/logout
   url(r'^accounts/logout/$', auth_views.logout, name="logout"),
   #override the default urls
   url(r'^password/change/$',auth_views.password_change,
       {'post_change_redirect': '/password/change/done/'},name='password_change'),
   url(r'^password/change/done/$',auth_views.password_change_done,name='password_change_done'),
   url(r'^password/reset/$', auth_views.password_reset,
       {'post_reset_redirect':'/password/reset/done/'},name='password_reset'),
   url(r'^password/reset/done/$',auth_views.password_reset_done, name='password_reset_done'),
   url(r'^password/reset/complete/$',auth_views.password_reset_complete,name='password_reset_complete'),
   url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm, {'post_reset_redirect': '/password/reset/complete/'},name='password_reset_confirm'),


)
