#!/usr/bin/env python3
"""
Multi-SP SAML Test Script
This script validates that both Service Providers are properly configured 
and registered with the Identity Provider.
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

def test_idp_configuration():
    """Test IdP configuration for multiple SPs"""
    print("=== Identity Provider Configuration Test ===")
    
    # Check SAML_IDP_SPCONFIG
    print(f"✓ SAML_IDP_SPCONFIG contains {len(settings.SAML_IDP_SPCONFIG)} SPs")
    
    for entity_id, config in settings.SAML_IDP_SPCONFIG.items():
        print(f"  • {entity_id}")
        processor = config.get('processor', 'Unknown')
        print(f"    Processor: {processor}")
        attrs = list(config.get('attribute_mapping', {}).keys())
        print(f"    Attributes: {', '.join(attrs)}")
    
    return True

def test_database_registration():
    """Test database registration of SPs"""
    print("\n=== Database Registration Test ===")
    
    expected_sps = [
        'https://istiaque.me/saml2/metadata/',
        'https://asiradnan.me/saml2/metadata/'
    ]
    
    registered_sps = ServiceProvider.objects.filter(active=True)
    print(f"✓ Found {registered_sps.count()} active Service Providers in database")
    
    all_good = True
    for expected_entity_id in expected_sps:
        sp = registered_sps.filter(entity_id=expected_entity_id).first()
        if sp:
            print(f"  ✓ {expected_entity_id}")
            print(f"    ID: {sp.id}, Name: {sp.pretty_name or 'N/A'}")
        else:
            print(f"  ✗ {expected_entity_id} NOT FOUND")
            all_good = False
    
    return all_good

def test_metadata_files():
    """Test metadata files exist"""
    print("\n=== Metadata Files Test ===")
    
    files_to_check = [
        ('/home/shelby70/Downloads/saml/idp/idp/sp_metadata.xml', 'SP1 metadata in IdP'),
        ('/home/shelby70/Downloads/saml/idp/idp/sp2_metadata.xml', 'SP2 metadata in IdP'),
        ('/home/shelby70/Downloads/saml/sp/sp/idp_metadata.xml', 'IdP metadata in SP1'),
        ('/home/shelby70/Downloads/saml/sp2/sp/idp_metadata.xml', 'IdP metadata in SP2'),
    ]
    
    all_good = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"  ✓ {description}: {file_path}")
        else:
            print(f"  ✗ {description}: {file_path} (missing or empty)")
            all_good = False
    
    return all_good

def test_certificates():
    """Test certificate files exist"""
    print("\n=== Certificates Test ===")
    
    cert_files = [
        ('/home/shelby70/Downloads/saml/idp/idp/certificates/public.cert', 'IdP public certificate'),
        ('/home/shelby70/Downloads/saml/idp/idp/certificates/private.key', 'IdP private key'),
        ('/home/shelby70/Downloads/saml/sp/sp/certificates/idp_public.cert', 'SP1 IdP certificate copy'),
        ('/home/shelby70/Downloads/saml/sp2/sp/certificates/idp_public.cert', 'SP2 IdP certificate copy'),
        ('/home/shelby70/Downloads/saml/sp2/sp/certificates/sp_public.cert', 'SP2 public certificate'),
        ('/home/shelby70/Downloads/saml/sp2/sp/certificates/sp_private.key', 'SP2 private key'),
    ]
    
    all_good = True
    for file_path, description in cert_files:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"  ✓ {description}: {file_path}")
        else:
            print(f"  ✗ {description}: {file_path} (missing or empty)")
            all_good = False
    
    return all_good

def get_sp_urls():
    """Generate test URLs for both SPs"""
    print("\n=== Test URLs ===")
    
    idp_base = "https://idp.asiradnan.com"
    
    print("SP1 (istiaque.me) URLs:")
    print(f"  Login URL: https://istiaque.me/saml2/login/")
    print(f"  SAML Request: {idp_base}/idp/sso/redirect/?next=https://istiaque.me/")
    
    print("\nSP2 (asiradnan.me) URLs:")
    print(f"  Login URL: https://asiradnan.me/saml2/login/")
    print(f"  SAML Request: {idp_base}/idp/sso/redirect/?next=https://asiradnan.me/")
    
    print(f"\nIdP Login: {idp_base}/login/")
    print(f"IdP Metadata: {idp_base}/metadata")

def main():
    """Run all tests"""
    print("Multi-SP SAML Configuration Validation")
    print("=" * 50)
    
    tests = [
        test_idp_configuration,
        test_database_registration,
        test_metadata_files,
        test_certificates,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"  ✗ Error in {test_func.__name__}: {e}")
            results.append(False)
    
    get_sp_urls()
    
    print(f"\n=== Summary ===")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} tests passed! Multi-SP setup is ready.")
    else:
        print(f"✗ {total - passed} tests failed. Check configuration.")
    
    print(f"\nNext steps:")
    print(f"1. Start both SP servers for testing")
    print(f"2. Test authentication flow from SP1 → IdP → SP1")
    print(f"3. Test authentication flow from SP2 → IdP → SP2")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
