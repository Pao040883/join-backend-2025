from rest_framework import serializers
from ..models import Task, Subtask, Contact, User

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'

    def validate_task(self, value):
        if not Task.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Die angegebene Task-ID existiert nicht.")
        return value



class TaskSerializer(serializers.ModelSerializer):
    contacts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Contact.objects.all()
    )
    total_subtasks = serializers.SerializerMethodField()
    done_subtasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_total_subtasks(self, obj):
        return obj.subtask_count()

    def get_done_subtasks(self, obj):
        return obj.done_subtask_count()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
