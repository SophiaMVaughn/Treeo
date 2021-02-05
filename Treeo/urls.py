"""Treeo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as dauth_views
from users_acc import views as users_acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('ReqAppt.urls')),
    path('', include('Upload_Download.urls')),
    path('login/', dauth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', dauth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-reset/', dauth_views.PasswordResetView.as_view(template_name='pass_reset.html'), name='pass_reset'),
    path('password-reset/done/', dauth_views.PasswordResetDoneView.as_view(template_name='pass_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', dauth_views.PasswordResetConfirmView.as_view(template_name='pass_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', dauth_views.PasswordResetCompleteView.as_view(template_name='pass_reset_complete.html'), name='password_reset_complete'),
    path('register/', users_acc_views.register, name='register'),
    path('profile/', users_acc_views.profile, name='profile'),
    path('edit_profile/', users_acc_views.edit_profile, name='edit_profile'),
    path('', users_acc_views.home, name='home'),
]