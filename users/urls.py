from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration, name='reg'),
    path('profile', views.profile, name='profile'),
    path('login', views.loginuser, name='login'),
    path('logout', views.logout, name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('reset_password', views.PasswReset.as_view(), name='password_reset'),

]
