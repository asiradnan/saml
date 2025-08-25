#!/usr/bin/env python3
"""
Debug SP2 UnknownSystemEntity Error
This script helps diagnose why SP2 is not being recognized by the IdP
"""

import os
import sys
import django

# Setup Django environment for IdP
sys.path.insert(0, '/home/shelby70/Downloads/saml/idp/idp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idp.settings')
django.setup()

from djangosaml2idp.models import ServiceProvider
from django.conf import settings
import xml.etree.ElementTree as ET

def check_sp2_registration():
    """Check SP2 database registration"""
    print("=== SP2 Database Registration ===")
    
    sp2_entity = 'https://asiradnan.me/saml2/metadata/'
    sp2 = ServiceProvider.objects.filter(entity_id=sp2_entity).first()
    
    if sp2:
        print(f"✓ SP2 found in database")
        print(f"  ID: {sp2.id}")
        print(f"  Entity ID: {sp2.entity_id}")
        print(f"  Active: {sp2.active}")
        print(f"  Pretty Name: {sp2.pretty_name}")
        print(f"  Has metadata: {'Yes' if sp2.local_metadata else 'No'}")
        
        if sp2.local_metadata:
            print(f"  Metadata length: {len(sp2.local_metadata)} characters")
            # Check if metadata is valid XML
            try:
                root = ET.fromstring(sp2.local_metadata)
                print(f"  Metadata XML valid: Yes")
                print(f"  Root element: {root.tag}")
            except ET.ParseError as e:
                print(f"  Metadata XML valid: No - {e}")
        
        return True
    else:
        print(f"✗ SP2 NOT found in database")
        return False

def check_idp_config():
    """Check IdP SAML configuration"""
    print("\n=== IdP SAML Configuration ===")
    
    sp_config = getattr(settings, 'SAML_IDP_SPCONFIG', {})
    sp2_entity = 'https://asiradnan.me/saml2/metadata/'
    
    if sp2_entity in sp_config:
        print(f"✓ SP2 found in SAML_IDP_SPCONFIG")
        config = sp_config[sp2_entity]
        print(f"  Processor: {config.get('processor', 'None')}")
        attrs = config.get('attribute_mapping', {})
        print(f"  Attributes: {', '.join(attrs.keys())}")
        return True
    else:
        print(f"✗ SP2 NOT found in SAML_IDP_SPCONFIG")
        print(f"Available entities: {list(sp_config.keys())}")
        return False

def check_metadata_files():
    """Check metadata files"""
    print("\n=== Metadata Files ===")
    
    sp2_metadata_path = '/home/shelby70/Downloads/saml/idp/idp/sp2_metadata.xml'
    
    if os.path.exists(sp2_metadata_path):
        print(f"✓ SP2 metadata file exists: {sp2_metadata_path}")
        
        with open(sp2_metadata_path, 'r') as f:
            content = f.read()
            print(f"  File size: {len(content)} characters")
            
            # Check if it contains the correct entity ID
            if 'https://asiradnan.me/saml2/metadata/' in content:
                print(f"  ✓ Contains correct entity ID")
            else:
                print(f"  ✗ Does NOT contain correct entity ID")
                
            # Check if it's valid XML
            try:
                root = ET.fromstring(content)
                print(f"  ✓ Valid XML")
                entity_id = root.get('entityID')
                print(f"  Entity ID in XML: {entity_id}")
            except ET.ParseError as e:
                print(f"  ✗ Invalid XML: {e}")
        
        return True
    else:
        print(f"✗ SP2 metadata file missing: {sp2_metadata_path}")
        return False

def suggest_fixes():
    """Suggest potential fixes"""
    print("\n=== Suggested Fixes ===")
    
    print("1. Restart the IdP server to reload configuration")
    print("2. Check if IdP is using the correct database")
    print("3. Verify SP2 sends correct entity ID in SAML requests")
    print("4. Check IdP logs for specific error details")
    print("5. Try re-registering SP2 with updated metadata")

def main():
    """Run all diagnostic checks"""
    print("SP2 UnknownSystemEntity Debug")
    print("=" * 40)
    
    checks = [
        check_sp2_registration,
        check_idp_config,
        check_metadata_files,
    ]
    
    results = []
    for check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Error in {check_func.__name__}: {e}")
            results.append(False)
    
    suggest_fixes()
    
    print(f"\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} checks passed - configuration looks correct")
        print("The issue might be that the IdP server needs to be restarted.")
    else:
        print(f"✗ {total - passed} checks failed - configuration issues found")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
