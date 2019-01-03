"""fuseproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import *
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = "YBAdminApp"

urlpatterns = [
    url(r'^Home', views.Home, name='Home'),
    url(r'^product/$', views.product, name='product'),
    url(r'^bkList', views.bkList, name='bkList'),
    url(r'^bookingUpdate', views.bookingUpdate, name='bookingUpdate'),
    url(r'^messageSend', views.messageSend, name='messageSend'),
    url(r'^prUpdate', views.productUpdate, name='productUpdate'),
    url(r'^bkSearch', views.bkSearch, name='bkSearch'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logoutuser, name='logout'),
    url(r'^booking/(?P<booking_id>\d+)/$', views.booking_detail, name='booking_detail'),
    url(r'^message/(?P<booking_id>\d+)/$', views.message_detail, name='message_detail'),
    url(r'^prdetail/(?P<product_id>\d+)/$', views.product_detail, name='product_detail'),
    #url(r'^(?P<Id>[-\w]+)/$', views.booking_detail,  'booking_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
