from django.conf.urls import patterns, include, url
#from django.conf.urls.defaults import *
from mysite.views import *
from mysite.books import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d+)/$', hours_ahead),
    (r'^admin/', include(admin.site.urls)),
    (r'^meta/$', display_meta),
    #(r'^search-form/$', views.search_form),
    (r'^search/$', views.search),
    (r'^contact/$',views.contact),
)
