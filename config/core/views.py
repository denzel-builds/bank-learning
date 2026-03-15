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
    return render(request, 'core/task_list.html', {'tasks': tasks})

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
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)

    return Response(serializer.data)

@api_view(['PUT'])
def api_update_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def api_delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return Response({"message": "Task deleted successfully"})