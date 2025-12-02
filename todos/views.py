from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Todo
from .forms import TodoForm


class HomeView(TemplateView):
    template_name = 'todos/home.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'todos/register.html'
    success_url = reverse_lazy('todo_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.created_user)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.created_user = None
        return context
    
    def form_valid(self, form):
        self.created_user = form.save()
        login(self.request, self.created_user)
        return redirect(self.success_url)


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user, is_resolved=False)
        sort_by = self.request.GET.get('sort', '')
        
        # Apply sorting if sort parameter exists
        if sort_by:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_todos'] = Todo.objects.filter(
            user=self.request.user, 
            is_resolved=True
        ).order_by('-resolved_at')
        context['current_sort'] = self.request.GET.get('sort', '')
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo_list')
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


def toggle_resolved(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_resolved = not todo.is_resolved
    todo.resolved_at = timezone.now() if todo.is_resolved else None
    todo.save()
    return redirect('todo_list')
