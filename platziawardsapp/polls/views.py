from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Question


def index(request):
    questions = Question.objects.all()
    context = {
        "latest_question_list": questions
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return HttpResponse(f"This is the question {question_id}")


def results(request, question_id):
    return HttpResponse(f"This are the results of the question {question_id}")


def vote(request, question_id):
    return HttpResponse(f"You are voting for the question {question_id}")
