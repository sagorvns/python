# Django Framework – Interview Guide (Using Your Task Backend)

A simple explanation of Django using your **task_backend** project so you can answer interview questions confidently.

---

## 1. What is Django?

**Short answer:** Django is a **high-level Python web framework** that helps you build web applications quickly. It follows the principle of **“batteries included”**—it gives you things like an admin panel, ORM (database access), authentication, and URL routing out of the box.

**In one line:** *“Django is a Python framework for building web apps; it handles URLs, database, and business logic in an organized way.”*

---

## 2. Project vs App

| Concept | In your project | Purpose |
|--------|------------------|---------|
| **Project** | `task_backend` (root folder with `config/`, `manage.py`) | The whole website. Contains settings, main URL config, and a list of apps. |
| **App** | `api` (folder with `models.py`, `views.py`, etc.) | A **reusable module** that does one thing (e.g. “Task API”). A project can have many apps. |

**Interview tip:** *“A project is the overall application; apps are pluggable components. In my project, `config` is the project settings, and `api` is the app that handles tasks.”*

---

## 3. How a Request Flows (Important for Interviews)

When someone visits **`GET /api/tasks/`**:

1. **Django** receives the request.
2. **`config/urls.py`** (ROOT_URLCONF) says: “anything under `/api/` → go to `api.urls`”.
3. **`api/urls.py`** uses the **router**: “`/tasks/` with GET → `TaskViewSet.list`”.
4. **`TaskViewSet`** (in `api/views.py`) runs:
   - Gets all tasks: `Task.objects.all()`
   - Uses **TaskSerializer** to convert them to JSON.
5. **Response**: JSON list of tasks is sent back.

So: **URL → View → Model (database) + Serializer → JSON response.**

---

## 4. Main Components (With Your Code)

### 4.1 Models (`api/models.py`)

**What it is:** A Python class that **defines a database table**. Django’s ORM turns it into SQL and lets you use Python instead of writing SQL.

**Your code:**
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Interview Q: “What is a Django model?”**  
*“A model is a Python class that represents a database table. Each attribute is a column. Django creates the table and lets me query it with Python, e.g. `Task.objects.all()`.”*

**Interview Q: “What’s the difference between `blank=True` and `null=True`?”**  
*“`blank=True` is for forms/validation—the field can be empty. `null=True` is for the database—the column can store NULL. For `CharField`/`TextField`, we often use both for optional text.”*

---

### 4.2 Migrations (`api/migrations/`)

**What it is:** Migrations are **version control for your database schema**. They turn model changes into SQL (create/alter tables) so the DB stays in sync with your code.

**Commands you use:**
- `python manage.py makemigrations` – create migration files from model changes.
- `python manage.py migrate` – apply those migrations to the database.

**Interview Q: “What are Django migrations?”**  
*“They’re files that describe changes to the database (new tables, new columns). I run `makemigrations` after changing models, then `migrate` to apply them. That way the schema stays consistent across environments.”*

---

### 4.3 Views (`api/views.py`) – and Django REST Framework

**What it is:** Views are where **request handling and business logic** live. They take an HTTP request and return an HTTP response. In your project you use **Django REST Framework (DRF)** and **ViewSets**.

**Your code:**
```python
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

**ModelViewSet** gives you for free:
- **list** – GET `/api/tasks/` (all tasks)
- **create** – POST `/api/tasks/`
- **retrieve** – GET `/api/tasks/{id}/`
- **update** – PUT `/api/tasks/{id}/`
- **partial_update** – PATCH `/api/tasks/{id}/`
- **destroy** – DELETE `/api/tasks/{id}/`

**Interview Q: “What is a ViewSet?”**  
*“A ViewSet groups all CRUD logic for a model in one class. With ModelViewSet and a router, you get list, create, retrieve, update, and delete without writing each view by hand.”*

**Interview Q: “What’s the difference between PUT and PATCH?”**  
*“PUT usually replaces the whole resource; PATCH updates only the fields you send. In DRF, that’s `update` vs `partial_update`.”*

---

### 4.4 Serializers (`api/serializers.py`)

**What it is:** In DRF, serializers do two things:
1. **Serialization:** Python objects (e.g. `Task`) → JSON (for the response).
2. **Deserialization:** JSON (from the request) → Python objects + validation → save to DB.

**Your code:**
```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
```

**Interview Q: “What does a serializer do?”**  
*“It converts model instances to JSON for the API response, and converts incoming JSON to validated data for creating/updating models. It also runs validation, like my custom `validate_title`.”*

---

### 4.5 URLs (`config/urls.py` and `api/urls.py`)

**What it is:** URL configuration **maps URLs to views**. The project has a root `urls.py`; each app can have its own and you `include()` them.

**Your code:**
- **config/urls.py:** `path('api/', include('api.urls'))` → all `/api/...` go to the `api` app.
- **api/urls.py:** Router registers `TaskViewSet` under `tasks` → `/api/tasks/`, `/api/tasks/1/`, etc.

**Interview Q: “How does Django route a URL to a view?”**  
*“Django matches the request path against `urlpatterns` in `urls.py`. We use `include()` to delegate under a prefix (e.g. `api/`) to the app’s `urls.py`, and the DRF router registers routes for the ViewSet.”*

---

### 4.6 Settings (`config/settings.py`)

**What it is:** Central configuration: database, installed apps, middleware, security, third-party settings (e.g. DRF, CORS).

**Important in your project:**
- **INSTALLED_APPS** – Django and third-party apps plus your `api` app.
- **DATABASES** – SQLite for development.
- **ROOT_URLCONF** – points to `config.urls`.
- **MIDDLEWARE** – runs on every request (e.g. security, sessions, CORS).
- **CORS** – so the React frontend (different port) can call your API.

**Interview Q: “What is middleware?”**  
*“Middleware is code that runs on every request and response. It runs in order: e.g. CORS, security, sessions, auth. It can modify the request/response or short-circuit and return a response.”*

---

### 4.7 Admin (`api/admin.py`)

**What it is:** Django’s built-in **admin site** to manage model data (CRUD in the browser).

**Your code:**
```python
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description')
```

**Interview Q: “What is Django admin?”**  
*“It’s an auto-generated admin panel. You register your models and optionally customize list display, filters, and search. It’s useful for internal tools and debugging.”*

---

## 5. Quick Glossary

| Term | Meaning in your project |
|------|--------------------------|
| **ORM** | Object-Relational Mapping – use Python (`Task.objects.filter(completed=False)`) instead of raw SQL. |
| **MVT** | Model (data), View (logic), Template (HTML). Your project is API-only, so “Template” is replaced by JSON via serializers. |
| **CRUD** | Create, Read, Update, Delete – all provided by `TaskViewSet`. |
| **WSGI** | Protocol Django uses to talk to the web server (e.g. Gunicorn in production). |
| **manage.py** | Entry point for Django commands: `runserver`, `migrate`, `makemigrations`, `createsuperuser`, etc. |

---

## 6. Common Interview Questions – Short Answers

**Q: Why Django?**  
*“It’s batteries-included, has a strong ORM, built-in admin, and a clear structure. Good for fast development and maintainable code.”*

**Q: What is the Django ORM?**  
*“It lets me interact with the database using Python classes and methods. For example, `Task.objects.filter(completed=False)` instead of writing SQL.”*

**Q: How do you add a new field to an existing model?**  
*“Add the field in `models.py`, then run `makemigrations` and `migrate`. Django generates and applies the migration.”*

**Q: What’s the difference between Django and Django REST Framework?**  
*“Django is the web framework. DRF is an add-on for building REST APIs: serializers, ViewSets, authentication, permissions. My task API uses Django for the app and DRF for the API layer.”*

**Q: How would you secure the API for production?**  
*“Use proper permissions (e.g. IsAuthenticated), remove AllowAny, use HTTPS, set DEBUG=False, keep SECRET_KEY secret, restrict CORS and ALLOWED_HOSTS, and use environment variables for secrets.”*

---

## 7. One-Page “Tell me about your project” Script

*“I built a task manager backend with Django and Django REST Framework. The project has one app, `api`, which exposes a REST API for tasks.*

*I defined a `Task` model with title, description, completed flag, and timestamps. I use a ModelViewSet and a router so I get list, create, retrieve, update, and delete without writing each view. Serializers convert tasks to and from JSON and handle validation.*

*I use SQLite in development and Django’s migrations for schema changes. The admin is registered for the Task model so I can manage data from the admin panel. CORS is configured so a React frontend on another port can call the API.*

*I also added a custom action on the ViewSet to toggle a task’s completed status via PATCH.”*

---

Use this guide with your actual `task_backend` code so you can point to files and lines when explaining. Good luck in your interview.
