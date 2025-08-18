#!/usr/bin/env python3
"""
Test script to verify SAML SSO flow between SP and IdP
"""

import requests
import sys
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def test_saml_flow():
    """Test the complete SAML SSO flow"""
    session = requests.Session()
    
    print("🔍 Testing SAML SSO Flow...")
    print("=" * 50)
    
    # Step 1: Access SP login endpoint
    print("1. Accessing SP SAML login endpoint...")
    try:
        sp_login_response = session.get('http://localhost:8000/saml2/login/')
        print(f"   Status: {sp_login_response.status_code}")
        
        if sp_login_response.status_code == 200:
            # Parse the auto-submit form
            soup = BeautifulSoup(sp_login_response.text, 'html.parser')
            form = soup.find('form', {'name': 'SSO_Login'})
            
            if form:
                action = form.get('action')
                saml_request = form.find('input', {'name': 'SAMLRequest'})
                relay_state = form.find('input', {'name': 'RelayState'})
                
                print(f"   Form action: {action}")
                print(f"   SAMLRequest present: {saml_request is not None}")
                print(f"   RelayState present: {relay_state is not None}")
                
                if action and saml_request:
                    # Step 2: Post SAML request to IdP
                    print("\n2. Posting SAML request to IdP...")
                    
                    data = {
                        'SAMLRequest': saml_request.get('value'),
                        'RelayState': relay_state.get('value') if relay_state else ''
                    }
                    
                    idp_response = session.post(action, data=data, allow_redirects=False)
                    print(f"   Status: {idp_response.status_code}")
                    
                    if idp_response.status_code in [200, 302]:
                        print("   ✅ IdP responded successfully")
                        if 'location' in idp_response.headers:
                            print(f"   Redirect to: {idp_response.headers['location']}")
                        return True
                    else:
                        print(f"   ❌ IdP error: {idp_response.status_code}")
                        print(f"   Response: {idp_response.text[:200]}...")
                        return False
                else:
                    print("   ❌ Invalid SAML request form")
                    return False
            else:
                print("   ❌ No SSO_Login form found")
                print(f"   Response content: {sp_login_response.text[:200]}...")
                return False
        else:
            print(f"   ❌ SP login failed: {sp_login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_endpoints():
    """Test individual endpoints"""
    print("\n🔍 Testing Individual Endpoints...")
    print("=" * 50)
    
    endpoints = [
        ('SP Home', 'http://localhost:8000/'),
        ('SP Metadata', 'http://localhost:8000/saml2/metadata/'),
        ('IdP Home', 'http://localhost:9000/'),
        ('IdP Metadata', 'http://localhost:9000/idp/metadata/'),
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

if __name__ == "__main__":
    test_endpoints()
    print()
    success = test_saml_flow()
    
    if success:
        print("\n🎉 SAML flow test completed successfully!")
        print("Next steps:")
        print("1. Open http://localhost:8000/ in a browser")
        print("2. Click 'Login with SAML'")
        print("3. Login with admin/admin123 at the IdP")
    else:
        print("\n❌ SAML flow test failed!")
        print("Check the server logs for more details.")
