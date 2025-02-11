from django.contrib.auth.models import User
from django.db import models
import random

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "Todo"),
        ("progress", "In progress"),
        ("feedback", "Await feedback"),
        ("done", "Done"), 
    ]
    due_date = models.DateField()
    prio = models.CharField(max_length=6) 
    title = models.CharField(max_length=30)
    description = models.TextField()
    category = models.CharField(max_length=15)
    contacts = models.ManyToManyField("Contact", related_name="tasks")  
    type = models.CharField(max_length=8, choices=STATUS_CHOICES, default="todo")
    position = models.IntegerField(blank=True, null=True)
    
    def subtask_count(self):
        """Gibt die Gesamtanzahl der Subtasks für diesen Task zurück."""
        return self.subtasks.count()

    def done_subtask_count(self):
        """Gibt die Anzahl der offenen Subtasks für diesen Task zurück."""
        return self.subtasks.filter(status="done").count()
    
    def save(self, *args, **kwargs):
        if self.position is None and self.type == 'todo':
            last_position = Task.objects.filter(type='todo').aggregate(models.Max('position'))['position__max']
            self.position = (last_position or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subtask(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=40, verbose_name="Subtask Title")
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name="Status"
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name="Parent Task"
    )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    color = models.CharField(max_length=7, null=True)
    
    def save(self, *args, **kwargs):
        if not self.color:  
            self.color = self.generate_random_color()
        super().save(*args, **kwargs)

    def generate_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def __str__(self):
        return self.name

