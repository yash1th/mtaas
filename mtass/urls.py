from django.conf.urls import patterns, include, url
from django.contrib import admin
from team14 import views

urlpatterns = patterns('',
    # Examples:
     url(r'^$', views.home_page, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard', views.my_dashboard, name='dashboard'),
    url(r'^billing', views.billing_api, name='billing'),
    url(r'^instances', views.instance_details, name='instance'),
     url(r'^bill', views.find_bill, name='instance'),
    url(r'^launch', views.launch_instance, name='launch_instance'),
    url(r'^vnc_view', views.render_emulator, name='vnc')
)
