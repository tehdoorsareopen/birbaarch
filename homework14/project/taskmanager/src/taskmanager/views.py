from django.shortcuts import render


from .decorators import test

@test
def index(request):
    context = {'latest_question_list': 'latest_question_list'}
    return render(request, 'tasks/index.html', context)
