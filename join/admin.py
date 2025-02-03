from django.contrib import admin
from .models import Task

class CustomerAdmin(admin.ModelAdmin):
    list_filter= ['title']

# Register your models here.
admin.site.register(Task, CustomerAdmin)