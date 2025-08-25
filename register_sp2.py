#!/usr/bin/env python3
import os
import sys
import django

# Add the IdP project to the Python path
sys.path.insert(0, '/home/shelby70/Downloads/saml/idp/idp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')

# Setup Django
django.setup()

# Now we can import Django models
from djangosaml2idp.models import ServiceProvider
from django.contrib.auth.models import User

def register_sp2():
    """Register SP2 (asiradnan.me) in the IdP database"""
    
    # Define SP2 details
    entity_id = 'https://asiradnan.me/saml2/metadata/'
    sp_name = 'asiradnan.me Service Provider'
    
    try:
        # Check if SP2 already exists
        existing_sp = ServiceProvider.objects.filter(entity_id=entity_id).first()
        
        if existing_sp:
            print(f"SP2 already exists: {existing_sp}")
            print(f"Entity ID: {existing_sp.entity_id}")
            print(f"Active: {existing_sp.active}")
            return existing_sp
        
        # Create new ServiceProvider for SP2
        sp2 = ServiceProvider.objects.create(
            entity_id=entity_id,
            pretty_name=sp_name,
            active=True,
            local_metadata=open('/home/shelby70/Downloads/saml/idp/idp/sp2_metadata.xml', 'r').read()
        )
        
        print(f"Successfully registered SP2:")
        print(f"Entity ID: {sp2.entity_id}")
        print(f"Pretty Name: {sp2.pretty_name}")
        print(f"Active: {sp2.active}")
        print(f"ID: {sp2.id}")
        
        return sp2
        
    except Exception as e:
        print(f"Error registering SP2: {e}")
        return None

def list_all_sps():
    """List all registered Service Providers"""
    print("\n=== All Registered Service Providers ===")
    sps = ServiceProvider.objects.all()
    
    if not sps:
        print("No Service Providers registered.")
        return
    
    for sp in sps:
        print(f"ID: {sp.id}")
        print(f"Entity ID: {sp.entity_id}")
        print(f"Pretty Name: {sp.pretty_name}")
        print(f"Active: {sp.active}")
        print("-" * 50)

if __name__ == "__main__":
    print("=== SP2 Registration Script ===")
    register_sp2()
    list_all_sps()
