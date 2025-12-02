from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('<int:pk>/edit/', views.TodoUpdateView.as_view(), name='todo_edit'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo_delete'),
    path('<int:pk>/toggle/', views.toggle_resolved, name='todo_toggle'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='todos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
