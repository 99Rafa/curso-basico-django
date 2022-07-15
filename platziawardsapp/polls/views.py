from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from polls.models import Question


def index(request):
    questions = Question.objects.all()
    context = {
        "latest_question_list": questions
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    return HttpResponse(f"This are the results of the question {question_id}")


def vote(request, question_id):
    return HttpResponse(f"You are voting for the question {question_id}")
