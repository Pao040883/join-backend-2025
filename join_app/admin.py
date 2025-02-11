from django.contrib import admin
from .models import Task, Subtask, Contact

class CustomerAdmin(admin.ModelAdmin):
    list_filter= ['title']


# Register your models here.
admin.site.register(Task, CustomerAdmin)
admin.site.register(Subtask)
admin.site.register(Contact)