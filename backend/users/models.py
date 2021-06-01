from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model."""

    def __str__(self):
        return self.get_full_name() + f' ({self.email})'

    def get_full_name(self):
        """Return full name or email"""
        full_name = ' '.join(
            filter(None, (self.last_name, self.first_name))
        ).strip()
        full_name = full_name or self.email
        return full_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
