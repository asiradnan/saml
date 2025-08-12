from django.apps import AppConfig

class SamlSpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saml_sp'
    
    def ready(self):
        import saml_handlers  # Import our signal handlers
