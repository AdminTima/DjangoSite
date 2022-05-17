from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration, name='reg'),
    path('profile/<int:user_id>', views.profile, name='profile'),
]
