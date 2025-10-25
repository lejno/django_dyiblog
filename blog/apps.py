from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        # Import signals to ensure UserProfile objects are created on user creation
        try:
            import blog.signals  # noqa: F401
        except Exception:
            # Avoid raising errors during some management commands where app registry isn't fully ready
            pass
