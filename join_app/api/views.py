from rest_framework import viewsets, generics, status
from ..models import Task, Subtask, Contact
from .serializers import TaskSerializer, SubtaskSerializer, ContactSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, EmailAuthTokenSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubtaskViewSet(viewsets.ModelViewSet):
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
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def update(self, request, *args, **kwargs):

        instance = self.get_object()  # Den aktuellen Contact abrufen
        user = instance.user  # Falls der Contact mit einem User verknüpft ist

        # 1️⃣ Aktualisiert die Contact-Daten
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 2️⃣ Falls ein User existiert, müssen wir seine Daten ebenfalls aktualisieren
        if user:
            user.first_name = instance.name.split(" ")[0]  # Erster Name → first_name
            user.last_name = " ".join(instance.name.split(" ")[1:]) if " " in instance.name else ""  # Rest → last_name
            user.email = instance.email  # E-Mail synchronisieren
            user.save()

        return Response(serializer.data)



class DashboardView(APIView):

    def get(self, request):
        total_tasks = Task.objects.count()
        total_todos = Task.objects.filter(type="todo").count()
        total_done = Task.objects.filter(type="done").count()
        total_urgent = Task.objects.filter(prio="urgent").count()
        total_progress = Task.objects.filter(type="progress").count()
        total_feedback = Task.objects.filter(type="feedback").count()

        oldest_due_task = Task.objects.filter(prio="urgent").order_by("due_date").first()

        if oldest_due_task:
            oldest_due_date = oldest_due_task.due_date.strftime("%B %d, %Y") 
        else:
            oldest_due_date = "No urgent tasks"

        return Response({
            "sum_tasks": total_tasks,
            "sum_todos": total_todos,
            "sum_done": total_done,
            "sum_urgent": total_urgent,
            "sum_progress": total_progress,
            "sum_feedback": total_feedback,
            "oldest_due_date": oldest_due_date
        })

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email
            }
        else:
            data=serializer.errors
        
        return Response(data)
    

class LoginViewNew(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
                })

        return Response(serializer.errors, status=400)


class UserViewSet(viewsets.ViewSet):

    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def update(self, request):

        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)