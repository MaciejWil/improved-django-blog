"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views

from blog.views import contact, LogoutView, SignUp


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^contact/$', contact, name='contact'),
    url(r'',include('blog.urls')),
    url(r'^categories/', include('blog.urls_categories')),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/',LogoutView.as_view(), name='logout'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^api/blog/', include('blog.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
