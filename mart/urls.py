from django.conf.urls import include, url
from django.contrib import admin
from ads.views import *
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # Examples:
    # url(r'^$', 'mart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', home),
    url(r'^accounts/social/login/cancelled/', login_cancelled),
    url(r'^accounts/inactive/',account_inactive),
    url(r'^accounts/signup/',login_cancelled),
    url(r'^getdata/', adapi),
    url(r'^logout/',logout_view),
    url(r'^post-ad/$',postad),
    url(r'^myads/$',myads),
    url(r'^contact/$',contact),
    url(r'^loginpage/',loginpage),
    url(r'^login/',login),
    url(r'^success_login/',success_login),
    url(r'^myadsapi/$',myadsapi),
    url(r'^soldapi/$',soldapi),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^greendayauth/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
