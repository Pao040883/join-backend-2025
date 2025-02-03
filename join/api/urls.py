from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubtaskViewSet, ContactViewSet, UserViewSet, DashboardView, SubtasksByTaskView

# Router für API-Endpunkte
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path("dashboard/", DashboardView.as_view(), name="dashboard"),  
    path('tasks/<int:task_id>/subtasks/', SubtasksByTaskView.as_view(), name='subtasks-by-task'),
]
