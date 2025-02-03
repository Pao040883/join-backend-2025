from rest_framework import viewsets, generics
from ..models import Task, Subtask, Contact, User
from .serializers import TaskSerializer, SubtaskSerializer, ContactSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet für Tasks"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def partial_update(self, request, *args, **kwargs):
        """Erlaubt Updates einzelner Felder, z. B. `type`."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubtaskViewSet(viewsets.ModelViewSet):
    """ViewSet für Subtasks"""
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SubtasksByTaskView(generics.ListAPIView):
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Subtask.objects.filter(task_id=task_id)


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet für Kontakte"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet für Benutzer"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DashboardView(APIView):
    """APIView für Dashboard-Statistiken"""

    def get(self, request):
        total_tasks = Task.objects.count()
        total_todos = Task.objects.filter(type="todo").count()
        total_done = Task.objects.filter(type="done").count()
        total_urgent = Task.objects.filter(prio="urgent").count()
        total_progress = Task.objects.filter(type="progress").count()
        total_feedback = Task.objects.filter(type="feedback").count()

        # 🔹 Das **kleinste** `due_date` für "urgent"-Aufgaben abrufen
        oldest_due_task = Task.objects.filter(prio="urgent").order_by("due_date").first()

        # Falls keine "urgent"-Aufgabe existiert, Standardwert setzen
        if oldest_due_task:
            oldest_due_date = oldest_due_task.due_date.strftime("%B %d, %Y")  # 🔹 Formatierung
        else:
            oldest_due_date = "No urgent tasks"

        return Response({
            "sum_tasks": total_tasks,
            "sum_todos": total_todos,
            "sum_done": total_done,
            "sum_urgent": total_urgent,
            "sum_progress": total_progress,
            "sum_feedback": total_feedback,
            "oldest_due_date": oldest_due_date  # 🔹 Ältestes Datum mit Standardwert
        })