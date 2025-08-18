#!/usr/bin/env python
import os
import sys
import django
import requests
from xml.etree import ElementTree as ET

# Add the Django project to the Python path
sys.path.append('/home/asiradnan/A Laptop/Kaj Kormo/Code/Practice/saml/idp/idp')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')

# Setup Django
django.setup()

from djangosaml2idp.models import ServiceProvider

def register_sp():
    """Register the SP in the IdP admin panel"""
    
    # SP details
    sp_entity_id = "http://localhost:8000/saml2/metadata/"
    sp_metadata_url = "http://localhost:8000/saml2/metadata/"
    
    print("Fetching SP metadata...")
    try:
        # Fetch SP metadata
        response = requests.get(sp_metadata_url, timeout=10)
        response.raise_for_status()
        
        # Validate XML
        try:
            ET.fromstring(response.text)
            sp_metadata = response.text
            print("✓ SP metadata fetched and validated successfully")
        except ET.ParseError as e:
            print(f"✗ Invalid XML in SP metadata: {e}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to fetch SP metadata: {e}")
        return False
    
    # Check if SP already exists
    existing_sp = ServiceProvider.objects.filter(entity_id=sp_entity_id).first()
    
    if existing_sp:
        print(f"✓ SP already exists with ID: {existing_sp.id}")
        print(f"  Entity ID: {existing_sp.entity_id}")
        print(f"  Active: {existing_sp.active}")
        
        # Update the metadata
        existing_sp.remote_metadata_url = sp_metadata_url
        existing_sp.local_metadata = sp_metadata
        existing_sp.active = True
        existing_sp.save()
        print("✓ SP metadata updated successfully")
        return True
    
    # Create new SP
    try:
        sp = ServiceProvider.objects.create(
            entity_id=sp_entity_id,
            remote_metadata_url=sp_metadata_url,
            local_metadata=sp_metadata,
            active=True
        )
        print(f"✓ SP registered successfully with ID: {sp.id}")
        print(f"  Entity ID: {sp.entity_id}")
        print(f"  Metadata URL: {sp.remote_metadata_url}")
        print(f"  Active: {sp.active}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to register SP: {e}")
        return False

if __name__ == "__main__":
    print("=== Registering SP in IdP Admin Panel ===")
    success = register_sp()
    
    if success:
        print("\n✓ SP registration completed successfully!")
        print("\nNext steps:")
        print("1. SP is now registered and should be able to authenticate")
        print("2. Try logging in at: http://localhost:8000/saml2/login/")
        print("3. Check IdP admin panel: http://localhost:9000/admin/")
    else:
        print("\n✗ SP registration failed!")
        print("Please check the error messages above and try again.")
