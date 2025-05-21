from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm

def home(request, *args, **kwargs): 
    context = {}
    return render(request, 'pages/home.html', context)

def singup(request, *args, **kwargs): 
    context = {
        # 'form': UserCreationForm()
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        pass_one = request.POST.get('password1')
        pass_two = request.POST.get('password2')

        if pass_one == pass_two: 
            try: 
                new_user = User.objects.create_user(username = username, password = pass_one)
                new_user.save()
                login(request, new_user)

                return redirect('tasks_pending')
            except IntegrityError:
                context['message'] = 'Username already exists'
                return render(request, 'pages/singup.html', context)
        else: 
            context['message'] = 'Passwords do not match'
    
    return render(request, 'pages/singup.html', context)

def singin(request, *args, **kwargs): 
    context = {
        # 'form': AuthenticationForm()
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is None: 
            context['message'] = 'Invalid credentials'
        else: 
            login(request, user)
            return redirect('tasks_pending')
            
    return render(request, 'pages/singin.html', context)

@login_required
def singout(request, *args, **kwargs): 
    logout(request)
    return redirect('home')

@login_required
def tasks_pending(request, *args, **kwargs): 
    tasks = Task.objects.filter(user = request.user, completed_at__isnull = True).order_by('created_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'pages/tasks.html', context)

@login_required
def tasks_completed(request, *args, **kwargs): 
    tasks = Task.objects.filter(user = request.user, completed_at__isnull = False).order_by('completed_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'pages/tasks.html', context)

@login_required
def create_task(request, *args, **kwargs): 
    context = {
        # 'form': TaskForm()
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        important = bool(request.POST.get('important'))
        
        try: 
            new_task = Task(
                title = title, 
                description = description, 
                important = important, 
                user = request.user
            )
            new_task.save()

            return redirect('tasks_pending')
        except: 
            context['message'] = 'Error creating task'
    return render(request, 'pages/createTask.html', context)

@login_required
def task_update(request, *args, **kwargs): 
    task_id = kwargs.get('task_id')
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    context = {
        'task': task, 
        # 'form': TaskForm(initial = {
        #     'title': task.title, 
        #     'description': task.description, 
        #     'important': task.important
        # })
    }

    if request.method == 'POST': 
        title = request.POST.get('title')
        description = request.POST.get('description')
        important = bool(request.POST.get('important'))

        try: 
            task.title = title
            task.description = description
            task.important = important

            task.save(update_fields = ['title', 'description', 'important'])
            return redirect('tasks_pending')
        except: 
            context['message'] = 'Error updating task'

    return render(request, 'pages/taskDetail.html', context)

@login_required
def task_complete(request, *args, **kwargs): 
    task_id = kwargs.get('task_id')
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    context = {}

    if request.method == 'POST': 
        task.completed_at = timezone.now()
        task.save(update_fields = ['completed_at'])
        return redirect('tasks_pending')
    return render(request, 'pages/taskDetail.html', context)

@login_required
def task_delete(request, *args, **kwargs): 
    task_id = kwargs.get('task_id')
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    context = {}

    if request.method == 'POST': 
        task.delete()
        return redirect('tasks_pending')
    return render(request, 'pages/taskDetail.html', context)