#!/usr/bin/env python3
"""
Script to register the Service Provider in the IdP admin panel
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')
django.setup()

from djangosaml2idp.models import ServiceProvider

def register_sp():
    """Register the SP in the IdP database"""
    
    # SP configuration
    entity_id = "http://localhost:8000/saml2/metadata/"
    pretty_name = "Django SAML SP"
    
    # Check if SP already exists
    existing_sp = ServiceProvider.objects.filter(entity_id=entity_id).first()
    
    if existing_sp:
        print(f"✅ SP already registered: {entity_id}")
        existing_sp.active = True
        existing_sp.save()
        print(f"✅ SP activated: {pretty_name}")
    else:
        # Create new SP
        sp = ServiceProvider.objects.create(
            entity_id=entity_id,
            pretty_name=pretty_name,
            active=True,
            _processor="idp_app.processors.CustomSAMLProcessor",
            _attribute_mapping="""{
    "email": "email",
    "first_name": "first_name", 
    "last_name": "last_name",
    "username": "username",
    "is_staff": "is_staff",
    "is_superuser": "is_superuser"
}"""
        )
        print(f"✅ SP registered successfully:")
        print(f"   Entity ID: {sp.entity_id}")
        print(f"   Name: {sp.pretty_name}")
        print(f"   Active: {sp.active}")
        print(f"   Processor: {sp._processor}")

    # List all registered SPs
    print("\n📋 All registered Service Providers:")
    sps = ServiceProvider.objects.all()
    for sp in sps:
        status = "✅ Active" if sp.active else "❌ Inactive"
        print(f"   - {sp.pretty_name} ({sp.entity_id}) - {status}")

if __name__ == "__main__":
    register_sp()
