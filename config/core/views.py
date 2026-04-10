from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task
from .forms import TaskForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    # SEARCH — checks if ?search=something is in the URL
    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(title__icontains=search)  # icontains = case-insensitive search

    # FILTER BY STATUS
    status = request.GET.get('status', '')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    # FILTER BY PRIORITY
    priority = request.GET.get('priority', '')
    if priority in ['low', 'medium', 'high']:
        tasks = tasks.filter(priority=priority)

    # Pass search and filter values back to template so the form remembers them
    context = {
        'tasks': tasks,
        'search': search,
        'status': status,
        'priority': priority,
    }
    return render(request, 'core/task_list.html', context)

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'core/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Task.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        return redirect("task-list")

    return render(request, "core/task_create.html")

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'core/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('task-list')

    return render(request, 'core/task_confirm_delete.html', {'task': task})

def register(request):
    if request.user.is_authenticated:
        return redirect('task-list')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task-list")

    else:
        form = UserCreationForm()

    return render(request, "core/register.html", {"form": form})

@api_view(['GET'])
def api_task_list(request):
    tasks = Task.objects.filter(user=request.user)
    
    # Search support in API too
    search = request.query_params.get('search', '')
    if search:
        tasks = tasks.filter(title__icontains=search)
    
    # Filter by priority
    priority = request.query_params.get('priority', '')
    if priority in ['low', 'medium', 'high']:
        tasks = tasks.filter(priority=priority)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)  # 201 = Created
    return Response(serializer.errors, status=400)  # 400 = Bad request

@api_view(['PUT', 'PATCH'])
def api_update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def api_delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return Response({"message": "Task deleted successfully"}, status=204)  # 204 = No content