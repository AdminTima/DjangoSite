from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from . import models


def all_recent_polls(request):
    questions = models.Question.objects.raw('SELECT * FROM polls_question')
    return render(request, 'polls/recent.html', {'questions': questions})


def check_users_who_vote(user, question_id):
    voted_user = models.Users_Who_Voted.objects.filter(user__username=user, cur_question=question_id)
    print(len(voted_user))
    # print(user)
    if voted_user:
        return True


def detail(request, question_id):
    if check_users_who_vote(request.user.get_username(), question_id):
        return HttpResponseRedirect(reverse(results, kwargs={'question_id': question_id}))
    else:
        question = get_object_or_404(models.Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    if check_users_who_vote(request.user.get_username(), question_id):
        return HttpResponseRedirect(reverse(results, kwargs={'question_id': question_id}))
    question = get_object_or_404(models.Question, pk=question_id)
    error = ''
    selected_choice = request.POST['choice']
    if selected_choice:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
            selected_choice.votes = F('votes') + 1
            new_voted_user = models.Users_Who_Voted.objects.create(user=request.user, cur_question=question)
            selected_choice.save()
            return HttpResponseRedirect(reverse(results, kwargs={'question_id': question_id}))
        except KeyError:
            error = 'Key error occured'
    else:
        error = "You did not select any choice"
        return render(request, 'polls/detail.html', {'question': question, 'error': error})


def results(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
