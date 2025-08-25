#!/usr/bin/env python
import os
import sys
import django

# Add the Django project to the Python path
sys.path.append('/home/shelby70/Downloads/saml/idp/idp')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')

# Setup Django
django.setup()

from djangosaml2idp.models import ServiceProvider

def register_sp():
    """Register the SP in the IdP admin panel with production URLs"""
    
    # Production SP details
    sp_entity_id = "https://istiaque.me/saml2/metadata/"
    old_entity_id = "http://localhost:8000/saml2/metadata/"
    
    print(f"Registering SP with Entity ID: {sp_entity_id}")
    
    # Read SP metadata from local file
    metadata_file = '/home/shelby70/Downloads/saml/idp/idp/sp_metadata.xml'
    
    try:
        with open(metadata_file, 'r') as f:
            sp_metadata = f.read()
        print("✓ SP metadata loaded from local file")
    except FileNotFoundError:
        print(f"✗ SP metadata file not found: {metadata_file}")
        return False
    except Exception as e:
        print(f"✗ Failed to read SP metadata: {e}")
        return False
    
    # Check if SP already exists with production entity ID
    existing_sp = ServiceProvider.objects.filter(entity_id=sp_entity_id).first()
    
    if existing_sp:
        print(f"✓ SP already exists with production Entity ID: {existing_sp.id}")
        print(f"  Entity ID: {existing_sp.entity_id}")
        print(f"  Active: {existing_sp.active}")
        print(f"  Local Metadata: {existing_sp.local_metadata is not None}")
        
        # Update the existing SP with new metadata
        existing_sp.local_metadata = sp_metadata
        existing_sp.active = True
        existing_sp.save()
        print("✓ Updated existing SP with new metadata")
        return True
    
    # Check if there's an old SP with localhost entity ID and update it
    old_sp = ServiceProvider.objects.filter(entity_id=old_entity_id).first()
    
    if old_sp:
        print(f"✓ Found old SP with localhost Entity ID: {old_sp.id}")
        print("  Updating it to use production Entity ID...")
        
        # Update the old SP with new entity ID and metadata
        old_sp.entity_id = sp_entity_id
        old_sp.local_metadata = sp_metadata
        old_sp.active = True
        old_sp.save()
        print("✓ Successfully updated old SP to production Entity ID")
        return True
    
    # Create new SP
    try:
        sp = ServiceProvider.objects.create(
            entity_id=sp_entity_id,
            local_metadata=sp_metadata,
            active=True
        )
        
        # Try to set NameID format if the field exists
        try:
            sp._name_id_format = 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress'
            sp._nameid_field = 'email'
            sp.save()
        except AttributeError:
            # Some versions might not have these fields
            pass
        
        print(f"✓ Successfully registered new SP:")
        print(f"  ID: {sp.id}")
        print(f"  Entity ID: {sp.entity_id}")
        print(f"  Active: {sp.active}")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to register SP: {e}")
        return False

def list_registered_sps():
    """List all registered service providers"""
    sps = ServiceProvider.objects.all()
    print(f"\nRegistered Service Providers ({sps.count()}):")
    print("-" * 50)
    
    for sp in sps:
        print(f"ID: {sp.id}")
        print(f"Entity ID: {sp.entity_id}")
        print(f"Active: {sp.active}")
        # Handle different attribute names across versions
        try:
            print(f"NameID Format: {getattr(sp, '_name_id_format', 'Not set')}")
            print(f"NameID Field: {getattr(sp, '_nameid_field', 'Not set')}")
        except AttributeError:
            print("NameID Format: Not available")
            print("NameID Field: Not available")
        print(f"Has Metadata: {sp.local_metadata is not None}")
        print("-" * 30)

if __name__ == "__main__":
    print("🔧 SAML SP Registration Script")
    print("=" * 40)
    
    # List existing SPs first
    list_registered_sps()
    
    # Register/update the SP
    success = register_sp()
    
    if success:
        print("\n✅ SP registration completed successfully!")
        print("\nUpdated SP list:")
        list_registered_sps()
    else:
        print("\n❌ SP registration failed!")
    
    print("\n" + "=" * 40)
