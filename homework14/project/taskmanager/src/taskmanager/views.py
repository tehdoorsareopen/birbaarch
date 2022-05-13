from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from .decorators import test
from .models import Task
from .forms import CreateTaskForm


# @test
def index(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'tasks/index.html', context)


def user_tasks(request):
    tasks = Task.objects.filter(assigned_on=request.user)
    context = {'tasks': tasks}
    return render(request, 'tasks/index.html', context)


def create_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            assigned_on = form.cleaned_data['assigned_on']
            created_by = request.user
            Task.objects.create(
                name=name,
                description=description,
                assigned_on=assigned_on,
                created_by=created_by,
            )
            return HttpResponseRedirect(reverse('taskmanager:index'))
    else:
        form = CreateTaskForm()

    return render(request, 'tasks/create.html', {'form': form})


def view_task(request, task_id):
    task = Task.objects.get(pk=task_id)

    return render(request, 'tasks/view.html', {'task': task})
