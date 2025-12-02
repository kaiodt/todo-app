# Django TODO Application

A simple yet powerful TODO application built with Django that helps you organize and manage your tasks efficiently[web:45].

## Features

- ✅ **User Authentication**: Secure registration, login, and logout functionality
- ✅ **CRUD Operations**: Create, read, update, and delete TODOs
- ✅ **Priority Levels**: Set tasks as High, Medium, or Low priority
- ✅ **Due Dates**: Assign and track due dates for tasks
- ✅ **Task Status**: Mark tasks as resolved/completed with automatic timestamp
- ✅ **Overdue Detection**: Visual indicators for overdue tasks
- ✅ **Flexible Sorting**: Sort tasks by name, due date, or priority
- ✅ **Organized Views**: Separate sections for active and completed tasks
- ✅ **Collapsible Sections**: Toggle visibility of task sections
- ✅ **User Isolation**: Each user only sees their own tasks
- ✅ **Responsive Design**: Built with Bootstrap 5 for mobile-friendly interface

## Tech Stack

- **Python**: 3.13
- **Django**: 5.2.8
- **Package Manager**: uv
- **Frontend**: Bootstrap 5 with Bootstrap Icons
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)

## Project Structure

```
todo-app/
├── config/ # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── todos/ # Main application
│   ├── migrations/
│   ├── templates/
│   │   └── todos/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── todo_list.html
│   │       ├── todo_form.html
│   │       └── todo_confirm_delete.html
│   ├── models.py # Todo model
│   ├── views.py # View logic
│   ├── forms.py # Todo form
│   ├── urls.py # URL routing
│   └── tests.py # Test suite
├── manage.py
├── pyproject.toml
└── README.md
```

## Installation

### Prerequisites

- Python 3.13 or higher
- uv package manager (install from https://docs.astral.sh/uv/)

### Setup Instructions

1. **Clone the repository** (or create the project):

```shell
git clone <your-repo-url>
cd todo-app
```

2. **Create virtual environment and install dependencies**:

```shell
uv sync
```

If starting from scratch:

```shell
uv init todo-app
cd todo-app
uv add django
```

3. **Run database migrations**:

```shell
uv run python manage.py migrate
```

4. **Create a superuser** (optional, for admin access):

```shell
uv run python manage.py createsuperuser
```

5. **Run the development server**:

```shell
uv run python manage.py runserver
```

6. **Access the application**:

- Home: http://127.0.0.1:8000/
- TODO List: http://127.0.0.1:8000/todos/
- Admin Panel: http://127.0.0.1:8000/admin/

## Usage

### Getting Started

1. Visit the home page and click **Register** to create a new account
2. After registration, you'll be automatically logged in
3. Click **+ New TODO** to create your first task

### Managing TODOs

- **Create**: Click the "+ New TODO" button and fill in the form
- **Edit**: Click the "Edit" button on any task
- **Delete**: Click the "Delete" button and confirm
- **Mark as Complete**: Check the checkbox next to a task
- **Sort**: Use the sorting buttons to organize by Name, Due Date, or Priority

### Task Organization

- **Active Tasks**: Shows incomplete tasks (expanded by default)
- **Completed Tasks**: Shows finished tasks (collapsed by default)
- Click section headers to expand/collapse sections

### Visual Indicators

- **Red background**: Overdue tasks
- **Badge colors**:
- Red: High priority
- Yellow: Medium priority
- Gray: Low priority
- **OVERDUE badge**: Appears on tasks past their due date

## Running Tests

Run the complete test suite[web:45]:

```shell
uv run python manage.py test todos
```

Run with verbose output:

```shell
uv run python manage.py test todos --verbosity=2
```

Run specific test classes:

```shell
uv run python manage.py test todos.tests.TodoModelTest
uv run python manage.py test todos.tests.TodoViewsTest
uv run python manage.py test todos.tests.AuthenticationTest
```

## Database Schema

### Todo Model

| Field | Type | Description |
|-------|------|-------------|
| user | ForeignKey | Owner of the TODO |
| title | CharField(200) | Task title |
| description | TextField | Detailed description |
| due_date | DateField | Due date (optional) |
| priority | CharField | low/medium/high |
| is_resolved | BooleanField | Completion status |
| resolved_at | DateTimeField | Timestamp when resolved |
| created_at | DateTimeField | Creation timestamp |
| updated_at | DateTimeField | Last update timestamp |

## Development

### Adding New Features

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes
3. Write tests for new functionality
4. Run tests to ensure everything works
5. Commit and push changes

### Code Style

This project follows Django best practices:
- Class-based views for CRUD operations
- Model properties for computed fields
- Form validation using Django forms
- User authentication with LoginRequiredMixin

## Configuration

### Settings

Key settings in `config/settings.py`:

```python
LOGIN_REDIRECT_URL = 'todo_list'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
```

### Database

Default: SQLite (development)

To use PostgreSQL in production, update `DATABASES` in settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Collect static files: `python manage.py collectstatic`
5. Use a production server (Gunicorn + Nginx)
6. Set up environment variables for sensitive data

## Troubleshooting

### Common Issues

**Issue**: Logout returns 405 error
- **Solution**: Ensure logout is triggered via POST request using a form, not a link

**Issue**: Can't see other users' TODOs
- **Solution**: This is by design - each user only sees their own tasks

**Issue**: Overdue indicator not showing
- **Solution**: Ensure the task has a due date in the past and is not marked as resolved

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Styled with [Bootstrap 5](https://getbootstrap.com/)
- Icons from [Bootstrap Icons](https://icons.getbootstrap.com/)
- Package management by [uv](https://docs.astral.sh/uv/)
