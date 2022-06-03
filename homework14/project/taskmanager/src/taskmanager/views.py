from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# from .decorators import test
from .models import Task
from .forms import CreateTaskForm
from .signals import new_task_added, task_completed


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
            # assigned_on = form.cleaned_data['assigned_on']
            created_by = request.user
            task = Task.objects.create(
                name=name,
                description=description,
                # assigned_on=assigned_on,
                created_by=created_by,
            )
            new_task_added.send(sender=Task, instance=task)
            return HttpResponseRedirect(reverse('taskmanager:index'))
    else:
        form = CreateTaskForm()

    return render(request, 'tasks/create.html', {'form': form})


def complete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.completed = True
    task.save()
    task_completed.send(sender=Task, instance=task)
    return HttpResponseRedirect(reverse('taskmanager:index'))


def reassign_tasks(request):
    tasks = Task.objects.filter(completed=False)
    for task in tasks:
        task.assigned_on = task.get_random_user_to_assign()
        task.save()
    return HttpResponseRedirect(reverse('taskmanager:index'))


def view_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    context = {'task': task}
    return render(request, 'tasks/view.html', context)


# def login(request):
#     # tasks = Task.objects.all()
#     # context = {'tasks': tasks}
#     return render(request, 'auth/login.html')
