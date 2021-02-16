"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls.py/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from playmaker.login.views import IsLoggedInView, LogoutView
from playmaker.songs.views import SearchView

urlpatterns = [
    path('controller/', include('playmaker.controller.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('has_user', IsLoggedInView.as_view(), name="is-logged-in-view"),
    path('feedback', include('feedback.urls')),
    path('listener/', include('playmaker.listener.urls')),
    path('search/<str:_type>/', SearchView.as_view(), name="search-view"),
    path('social/', include('social_django.urls')),
    path('songs/', include('playmaker.songs.urls')),
    path('rooms/', include('playmaker.rooms.urls'), name="rooms-view"),

]
