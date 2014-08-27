from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.main_view, name="main"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^register/$', views.register_view, name="register"),

    url(r'^member/$', views.member_view, name="member"),
    url(r'^usage-report/$', views.usage_report_view, name="usage-report"),
    url(r'^return-report/$', views.return_report_view, name="return-report"),
    url(r'^delivery-report/$', views.delivery_report_view, name="delivery-report"),
    url(r'^summary-report/$', views.summary_report_view, name="summary-report"),
    url(r'^products/$', views.products_view, name="products"),



    #restful APIs, hacky way for now
    url(r'^rest/item/add/$', views.add_handler, name="add_handler"),
    url(r'^rest/item/update/$', views.update_handler, name="update_handler"),
    url(r'^rest/item/delete/$', views.remove_handler, name="remove_handler"),
    url(r'^rest/item/daily/$', views.get_handler, name="get_handler"),
)

