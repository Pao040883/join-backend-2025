from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubtaskViewSet, ContactViewSet, DashboardView, SubtasksByTaskView, RegistrationView, LoginViewNew, UserViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'contacts', ContactViewSet)

user_view = UserViewSet.as_view({
    'get': 'retrieve',   
    'put': 'update'      
})

urlpatterns = [
    path('', include(router.urls)),  
    path("dashboard/", DashboardView.as_view(), name="dashboard"),  
    path('tasks/<int:task_id>/subtasks/', SubtasksByTaskView.as_view(), name='subtasks-by-task'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginViewNew.as_view(), name='login'),
    path("user/me/", user_view, name="user-detail"),
    path("user/me/update/", user_view, name="user-update"),
]
