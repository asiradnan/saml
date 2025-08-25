#!/usr/bin/env python3
"""
Fix SP2 UnknownSystemEntity Error
This script refreshes SP2 registration and provides restart instructions
"""

import os
import sys
import django

# Setup Django environment for IdP
sys.path.insert(0, '/home/shelby70/Downloads/saml/idp/idp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')
django.setup()

from djangosaml2idp.models import ServiceProvider
from django.core.management import call_command

def refresh_sp2_registration():
    """Refresh SP2 registration to ensure it's properly loaded"""
    print("=== Refreshing SP2 Registration ===")
    
    sp2_entity = 'https://asiradnan.me/saml2/metadata/'
    
    try:
        # Get SP2
        sp2 = ServiceProvider.objects.get(entity_id=sp2_entity)
        print(f"Found SP2: {sp2.entity_id}")
        
        # Re-read metadata file
        metadata_path = '/home/shelby70/Downloads/saml/idp/idp/sp2_metadata.xml'
        with open(metadata_path, 'r') as f:
            metadata_content = f.read()
        
        # Update the metadata in the database
        sp2.local_metadata = metadata_content
        sp2.save()
        
        print(f"✓ SP2 metadata refreshed in database")
        print(f"✓ Updated SP2 record (ID: {sp2.id})")
        
        return True
        
    except ServiceProvider.DoesNotExist:
        print(f"✗ SP2 not found in database")
        return False
    except Exception as e:
        print(f"✗ Error refreshing SP2: {e}")
        return False

def clear_django_cache():
    """Clear Django cache if applicable"""
    print("\n=== Clearing Django Cache ===")
    try:
        # Clear cache if cache is configured
        from django.core.cache import cache
        cache.clear()
        print("✓ Django cache cleared")
    except Exception as e:
        print(f"Note: Could not clear cache (this is usually fine): {e}")

def main():
    """Main function"""
    print("SP2 UnknownSystemEntity Fix")
    print("=" * 30)
    
    # Refresh SP2 registration
    refresh_sp2_registration()
    
    # Clear cache
    clear_django_cache()
    
    print("\n=== Next Steps ===")
    print("1. RESTART the IdP server to reload SP configurations")
    print("2. The IdP server caches SP registrations in memory")
    print("3. After restart, SP2 should be recognized")
    
    print("\n=== IdP Restart Commands ===")
    print("If running IdP with Django development server:")
    print("  1. Stop the server (Ctrl+C)")
    print("  2. Restart with: python3 manage.py runserver")
    
    print("\nIf running IdP in production:")
    print("  1. Restart your WSGI server (gunicorn, uwsgi, etc.)")
    print("  2. Or restart the web server (nginx, apache)")
    
    print("\n=== Test After Restart ===")
    print("1. Try SP2 login: https://asiradnan.me/saml2/login/")
    print("2. Should redirect to IdP without UnknownSystemEntity error")
    
    return True

if __name__ == "__main__":
    main()
