from django.contrib import admin
from user.models import Task, Category, State

# Register your models here.
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(State)
