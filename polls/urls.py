from django.urls import path
from . import views

urlpatterns = [
    path('recent_polls', views.all_recent_polls, name='recent_polls'),
    path('detail/<int:question_id>', views.detail, name='detail'),
    path('vote/<int:question_id>', views.vote, name='vote'),
    path('results/<int:question_id>', views.results, name='results'),
]
