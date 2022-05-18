from django.db import models
from django.contrib.auth.models import User
import datetime

from django.urls import reverse
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField('Question text', max_length=230)
    published = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    def was_publihed(self, days):
        return self.published >= timezone.now() - datetime.timedelta(days=days)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'question_id': self.id})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=250)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Users_Who_Voted(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='User was deleted')
    cur_question = models.ForeignKey(Question, on_delete=models.CASCADE)


