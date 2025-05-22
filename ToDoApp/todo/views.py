from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import Task

# Create your views here.
def index(request):
    return render(request, 'todo/index.html',{})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')  
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form})

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('index')

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')
        
        due_date = None
        if due_date_str:
            try:
                from datetime import datetime
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass 

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date
            )
            return redirect('task_list')
    return render(request, 'todo/create_task.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date', 'created_at')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def update_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        # Process form submission for update
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        else:
            task.due_date = None 
        task.save()
        return redirect('task_list')
    else:
        return render(request, 'todo/update_task.html', {'task': task})


@login_required
def complete_task_view(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed # Toggle the status
        task.save()
    return redirect('task_list') # Redirect back to the list

@login_required
def delete_task_view(request, task_id):
    if request.method == 'POST': # Deletion should always be a POST request
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
    return redirect('task_list') # Redirect back to the list
