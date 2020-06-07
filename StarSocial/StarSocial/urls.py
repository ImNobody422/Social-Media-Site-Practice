"""StarSocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # Don't forget to check whether this can work without the following line
    # This is for some urls provided by auth app, like "accounts/profile"
    # Can be avoided by re-define redirection url to other pages
    # path('accounts/', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
