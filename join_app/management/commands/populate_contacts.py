from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Contact

class Command(BaseCommand):
    help = 'Fügt alle bestehenden Benutzer als Kontakte hinzu'

    def handle(self, *args, **kwargs):
        users_without_contact = User.objects.exclude(email__in=Contact.objects.values_list('email', flat=True))

        count = 0
        for user in users_without_contact:
            Contact.objects.create(
                name=f"{user.first_name} {user.last_name}",
                email=user.email,
                phone=""
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} Benutzer wurden als Kontakte hinzugefügt."))
