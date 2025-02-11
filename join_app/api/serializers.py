from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import Task, Subtask, Contact

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


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})

        full_name = self.validated_data['name'].strip()
        name_parts = full_name.split()

        if len(name_parts) < 2:
            raise serializers.ValidationError({'error': 'Please provide at least a first and last name'})

        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:])  
        username = f"{first_name}_{last_name}".replace(" ", "_").lower()

        account = User(
            email=self.validated_data['email'],
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        account.set_password(pw)
        account.save()

        Contact.objects.create(
            user=account,
            name=full_name,
            email=account.email,
            phone=""  
        )

        return account

   
class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Diese E-Mail ist nicht registriert."})

        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError({"password": "Falsches Passwort."})

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]  
        
    def update(self, instance, validated_data):
        """
        Speichert die aktualisierten Benutzerdaten.
        """
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance