from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import FormMixin
from rest_framework import viewsets, permissions
from user.forms import RegisterForm, LoginForm, TaskForm, CategoryForm, TaskDetailForm
from user.models import Task, Category, State
from user.serializers import TaskSerializer, CategorySerializer, StateSerializer, UserSerializer


class LoginView(FormView):
    template_name = 'login.html'
    success_url = '/dashboard/'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return self.form_valid(form)
            else:
                print('error')
        else:
            return self.form_invalid(form)


class RegisterView(FormView):
    template_name = 'register.html'
    success_url = '/login/'
    form_class = RegisterForm


    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            user = User.objects.create_user(form.data['username'], form.data['email'], form.data['password'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TaskView(FormView):
    template_name = 'task.html'
    success_url = '/dashboard/'
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            task = Task.objects.create(name=form.data['name'], category_id=form.data['category'], state_id=form.data['state'], user_id=request.user.id)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TaskDetailView(FormMixin, DetailView):
    template_name = 'task_detail.html'
    model = Task
    form_class = TaskDetailForm
    success_url = '/dashboard/'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['form'] = TaskDetailForm(initial={'name': self.object.name, 'category': self.object.category.id, 'state': self.object.state.id})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            task = self.get_object()
            
            task.name = form.data['name']
            task.category = Category.objects.get(id=form.data['category'])
            task.state = State.objects.get(id=form.data['state'])

            task.save()
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CategoryView(FormView):
    template_name = 'category.html'
    success_url = '/dashboard/'
    form_class = CategoryForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            category = Category.objects.create(name=form.data['name'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CategoryListView(ListView):
    template_name = 'category_list.html'
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['tasks'] = Task.objects.all()
        return context


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]