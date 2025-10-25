from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserProfile, Post, Comment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_on')


# Show UserProfile inline on the built-in User admin page
User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)


try:
    admin.site.unregister(User)
except Exception:
    # If the User model wasn't registered yet, ignore
    pass

admin.site.register(User, CustomUserAdmin)