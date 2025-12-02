from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo
from .forms import TodoForm


class TodoModelTest(TestCase):
    """Test the Todo model"""
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass123')
        cls.todo = Todo.objects.create(
            user=cls.user,
            title='Test TODO',
            description='Test description',
            due_date=date.today() + timedelta(days=7),
            priority='high',
            is_resolved=False
        )
    
    def test_todo_creation(self):
        """Test that a TODO is created correctly"""
        self.assertEqual(self.todo.title, 'Test TODO')
        self.assertEqual(self.todo.description, 'Test description')
        self.assertEqual(self.todo.priority, 'high')
        self.assertFalse(self.todo.is_resolved)
        self.assertIsNone(self.todo.resolved_at)
    
    def test_todo_str_method(self):
        """Test the string representation of TODO"""
        self.assertEqual(str(self.todo), 'Test TODO')
    
    def test_is_overdue_property(self):
        """Test the is_overdue property"""
        # Future due date - not overdue
        self.assertFalse(self.todo.is_overdue)
        
        # Past due date - overdue
        self.todo.due_date = date.today() - timedelta(days=1)
        self.assertTrue(self.todo.is_overdue)
        
        # Resolved TODO - not overdue even if past due date
        self.todo.is_resolved = True
        self.assertFalse(self.todo.is_overdue)
        
        # No due date - not overdue
        self.todo.due_date = None
        self.assertFalse(self.todo.is_overdue)


class TodoFormTest(TestCase):
    """Test the TodoForm"""
    
    def test_form_valid_data(self):
        """Test form with valid data"""
        form = TodoForm(data={
            'title': 'New TODO',
            'description': 'Description',
            'due_date': date.today(),
            'priority': 'medium',
        })
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_field(self):
        """Test form with missing required field"""
        form = TodoForm(data={
            'description': 'Description',
            'due_date': date.today(),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_form_fields(self):
        """Test that form has the correct fields"""
        form = TodoForm()
        self.assertEqual(list(form.fields.keys()), 
                        ['title', 'description', 'due_date', 'priority'])


class TodoViewsTest(TestCase):
    """Test TODO views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        
        self.todo = Todo.objects.create(
            user=self.user,
            title='Test TODO',
            description='Test description',
            due_date=date.today() + timedelta(days=7),
            priority='high',
        )
        
        self.completed_todo = Todo.objects.create(
            user=self.user,
            title='Completed TODO',
            description='Completed task',
            priority='low',
            is_resolved=True,
            resolved_at=timezone.now()
        )
    
    def test_todo_list_view_requires_login(self):
        """Test that todo list requires authentication"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/todos/login/', response.url)
    
    def test_todo_list_view_authenticated(self):
        """Test todo list view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_list.html')
        self.assertContains(response, 'Test TODO')
        self.assertIn('todos', response.context)
        self.assertIn('completed_todos', response.context)
    
    def test_todo_list_view_shows_only_user_todos(self):
        """Test that users only see their own TODOs"""
        other_todo = Todo.objects.create(
            user=self.other_user,
            title='Other User TODO',
            priority='medium',
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Test TODO')
        self.assertNotContains(response, 'Other User TODO')
    
    def test_todo_list_sorting(self):
        """Test sorting functionality"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create additional todos for sorting
        Todo.objects.create(user=self.user, title='A TODO', priority='low')
        Todo.objects.create(user=self.user, title='Z TODO', priority='high')
        
        # Test sort by title ascending
        response = self.client.get(reverse('todo_list') + '?sort=title')
        self.assertEqual(response.status_code, 200)
        todos = list(response.context['todos'])
        self.assertTrue(todos[0].title <= todos[-1].title)
    
    def test_todo_create_view_get(self):
        """Test GET request to create view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertIsInstance(response.context['form'], TodoForm)
    
    def test_todo_create_view_post(self):
        """Test POST request to create a new TODO"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('todo_create'), {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': date.today(),
            'priority': 'medium',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Todo.objects.filter(title='New TODO').exists())
        new_todo = Todo.objects.get(title='New TODO')
        self.assertEqual(new_todo.user, self.user)
    
    def test_todo_update_view(self):
        """Test updating a TODO"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('todo_edit', args=[self.todo.pk]), {
            'title': 'Updated TODO',
            'description': 'Updated description',
            'due_date': date.today(),
            'priority': 'low',
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated TODO')
        self.assertEqual(self.todo.priority, 'low')
    
    def test_todo_update_view_wrong_user(self):
        """Test that users cannot update other users' TODOs"""
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('todo_edit', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_todo_delete_view(self):
        """Test deleting a TODO"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())
    
    def test_todo_delete_view_wrong_user(self):
        """Test that users cannot delete other users' TODOs"""
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.post(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_toggle_resolved(self):
        """Test toggling TODO resolved status"""
        self.client.login(username='testuser', password='testpass123')
        
        # Toggle to resolved
        self.assertFalse(self.todo.is_resolved)
        response = self.client.post(reverse('todo_toggle', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
        self.assertIsNotNone(self.todo.resolved_at)
        
        # Toggle back to unresolved
        response = self.client.post(reverse('todo_toggle', args=[self.todo.pk]))
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_resolved)
        self.assertIsNone(self.todo.resolved_at)


class AuthenticationTest(TestCase):
    """Test authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_login_view_get(self):
        """Test GET request to login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/login.html')
    
    def test_login_view_post_valid(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
    
    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_logout_view(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
    
    def test_register_view_get(self):
        """Test GET request to register view"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/register.html')
    
    def test_register_view_post_valid(self):
        """Test user registration with valid data"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # User should be logged in after registration
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/home.html')
        self.assertContains(response, 'Welcome to TODO App')
