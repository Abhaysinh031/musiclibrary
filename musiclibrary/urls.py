"""
URL configuration for musiclibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views import View
from library import views as library_views
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponse('Logged out via POST')

    def get(self, request):
        return HttpResponse('This view only handles POST requests')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', library_views.home, name='home'), 
    path('library/', include('library.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='library/logout.html'), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)