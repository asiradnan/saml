# Multi-SP SAML Configuration Guide

## Overview

Your SAML setup now supports **two Service Providers** connecting to one Identity Provider:

- **IdP**: https://idp.asiradnan.com/
- **SP1**: https://istiaque.me/ (working)
- **SP2**: https://asiradnan.me/ (newly configured)

## What Was Configured

### 1. SP2 Setup

- ✅ Updated SP2 settings with production domain `asiradnan.me`
- ✅ Generated SP2 metadata with correct entity ID
- ✅ Configured SAML endpoints for asiradnan.me

### 2. IdP Multi-SP Configuration

- ✅ Added SP2 to `SAML_IDP_SPCONFIG` in IdP settings
- ✅ Registered SP2 entity in IdP database (ID: 3)
- ✅ Both SPs use same attribute processor and mappings

### 3. Certificate Management

- ✅ Copied IdP certificate to SP2 for signature verification
- ✅ SP2 has its own signing certificates

## Configuration Details

### IdP Configuration (`/home/shelby70/Downloads/saml/idp/idp/idp/settings.py`)

```python
SAML_IDP_SPCONFIG = {
    # Service Provider 1 - istiaque.me
    'https://istiaque.me/saml2/metadata/': {
        'processor': 'idp_app.processors.CustomSAMLProcessor',
        'attribute_mapping': { ... }
    },
    # Service Provider 2 - asiradnan.me
    'https://asiradnan.me/saml2/metadata/': {
        'processor': 'idp_app.processors.CustomSAMLProcessor',
        'attribute_mapping': { ... }
    }
}
```

### SP2 Configuration (`/home/shelby70/Downloads/saml/sp2/sp/sp/settings.py`)

```python
BASE_URL = 'https://asiradnan.me'
SAML_CONFIG = {
    'entityid': f'{BASE_URL}/saml2/metadata/',
    'service': {
        'sp': {
            'endpoints': {
                'assertion_consumer_service': [
                    (f'{BASE_URL}/saml2/acs/', saml2.BINDING_HTTP_POST),
                ],
                # ... other endpoints
            },
            'idp': {
                'https://idp.asiradnan.com/metadata': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://idp.asiradnan.com/idp/sso/redirect/',
                        # ... other bindings
                    }
                }
            }
        }
    }
}
```

## Testing the Multi-SP Setup

### 1. Start Development Servers

```bash
cd /home/shelby70/Downloads/saml
./start_both_sps.sh
```

This starts:

- SP1 on http://127.0.0.1:8000/
- SP2 on http://127.0.0.1:8001/

### 2. Test Authentication Flows

**SP1 → IdP → SP1:**

1. Visit: http://127.0.0.1:8000/saml2/login/
2. Should redirect to IdP for authentication
3. After login, should return to SP1

**SP2 → IdP → SP2:**

1. Visit: http://127.0.0.1:8001/saml2/login/
2. Should redirect to IdP for authentication
3. After login, should return to SP2

### 3. Validation Commands

```bash
# Validate complete configuration
python3 test_multi_sp.py

# Check SP registrations
python3 register_sp2.py
```

## Production Deployment

### Domain Configuration

- **IdP**: Deploy at https://idp.asiradnan.com/
- **SP1**: Deploy at https://istiaque.me/
- **SP2**: Deploy at https://asiradnan.me/

### Security Settings

Both SPs have production security settings:

- HTTPS enforcement
- Secure cookies
- CSRF protection
- HSTS headers

### Certificate Management

Ensure all certificates are properly deployed:

- IdP certificates in IdP deployment
- SP certificates in respective SP deployments
- IdP public certificate copied to both SPs

## Troubleshooting

### Common Issues

1. **Certificate mismatch**: Ensure IdP certificate is copied to both SPs
2. **Entity ID mismatch**: Verify database entity IDs match configuration
3. **URL mismatch**: Check all URLs use correct domains and /idp/ prefix

### Debug Mode

For testing, both SPs have debug settings:

```python
DEBUG = True  # Enable for testing
'debug': 1    # SAML debug mode
```

### Logs

Check Django development server logs for SAML-specific errors.

## Files Modified/Created

### New Files

- `/home/shelby70/Downloads/saml/idp/idp/sp2_metadata.xml` - SP2 metadata
- `/home/shelby70/Downloads/saml/register_sp2.py` - SP2 registration script
- `/home/shelby70/Downloads/saml/test_multi_sp.py` - Multi-SP validation
- `/home/shelby70/Downloads/saml/start_both_sps.sh` - Development server startup

### Modified Files

- `/home/shelby70/Downloads/saml/idp/idp/idp/settings.py` - Added SP2 configuration
- `/home/shelby70/Downloads/saml/sp2/sp/sp/settings.py` - Production domain settings

## Success Metrics

✅ All 4 validation tests pass
✅ Both SPs registered in IdP database  
✅ All metadata files present
✅ All certificates in place
✅ Multi-SP SAML ready for production
