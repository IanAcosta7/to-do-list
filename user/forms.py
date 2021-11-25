from django import forms

from user.models import Category, State


class RegisterForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput, required=True)
    username = forms.CharField(widget=forms.TextInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class TaskForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, required=True)
    category = forms.ModelChoiceField(widget=forms.Select, required=True, queryset=Category.objects.all())
    state = forms.ModelChoiceField(widget=forms.Select, required=True, queryset=State.objects.all())


class CategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, required=True)


class TaskDetailForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, required=True)
    category = forms.ModelChoiceField(widget=forms.Select, required=True, queryset=Category.objects.all())
    state = forms.ModelChoiceField(widget=forms.Select, required=True, queryset=State.objects.all())
