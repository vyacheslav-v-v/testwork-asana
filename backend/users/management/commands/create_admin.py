from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = ('Create superuser with username `admin` and password `123`.')

    def handle(self, **options):
        """Create superuser with username `admin` and password `123`."""

        User.objects.create_superuser(email='admin@example.com',
                                      username='admin',
                                      password='123')

        self.stdout.write(
            self.style.SUCCESS('Super user is created successfully'))
