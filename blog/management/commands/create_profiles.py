from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile objects for users that are missing them'

    def handle(self, *args, **options):
        User = get_user_model()
        created = 0
        for user in User.objects.all():
            profile, was_created = UserProfile.objects.get_or_create(user=user)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))
        if created == 0:
            self.stdout.write('No missing profiles found.')
        else:
            self.stdout.write(self.style.SUCCESS(f'Created {created} profiles.'))
