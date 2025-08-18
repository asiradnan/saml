from django.core.management.base import BaseCommand
from djangosaml2idp.views import metadata


class Command(BaseCommand):
    help = 'Generate IdP metadata XML'

    def handle(self, *args, **options):
        """Generate and display the IdP metadata XML"""
        from django.test import RequestFactory
        from django.http import HttpRequest
        
        factory = RequestFactory()
        request = factory.get('/idp/metadata/')
        
        # Generate metadata
        response = metadata(request)
        
        self.stdout.write("IdP Metadata XML:")
        self.stdout.write("=" * 50)
        self.stdout.write(response.content.decode('utf-8'))
        self.stdout.write("=" * 50)
        self.stdout.write(
            self.style.SUCCESS("Metadata generated successfully!")
        )
