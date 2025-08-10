# SAML Implementation Troubleshooting Guide

## Issues Found and Fixed

### 1. **Missing Custom Processor** ✅ FIXED
- **Problem**: IdP settings referenced `saml_idp.custom_processor.CustomProcessor` that didn't exist
- **Solution**: Created `saml_idp/custom_processor.py` with proper SAML attribute mapping

### 2. **Missing SSL Certificates** ✅ FIXED
- **Problem**: Both IdP and SP were missing required SSL certificates
- **Solution**: Generated certificates using `generate_certificates.sh` script
- **Files Created**:
  - IdP: `saml_idp/certs/mycert.pem` and `saml_idp/certs/mykey.pem`
  - SP: `saml_sp/certificates/sp_certificate.pem` and `saml_sp/certificates/sp_private_key.pem`

### 3. **Entity ID Mismatch** ✅ FIXED
- **Problem**: SP metadata had wrong entity ID (`http://localhost:8000/idp/metadata/` instead of `http://localhost:8000/saml2/metadata/`)
- **Solution**: Updated SP metadata to use correct entity ID

### 4. **Incorrect SP Metadata** ✅ FIXED
- **Problem**: SP metadata contained IdP information instead of SP information
- **Solution**: Completely rewrote SP metadata with proper SPSSODescriptor

### 5. **Missing Test Views** ✅ FIXED
- **Problem**: No way to test the SAML flow
- **Solution**: Added test views to both IdP and SP

## Current Configuration

### IdP (Port 8001)
- **Entity ID**: `http://localhost:8001/idp/metadata/`
- **SSO Endpoints**: 
  - POST: `http://localhost:8001/idp/sso/post/`
  - Redirect: `http://localhost:8001/idp/sso/redirect/`
- **Custom Processor**: `saml_idp.custom_processor.CustomProcessor`

### SP (Port 8000)
- **Entity ID**: `http://localhost:8000/saml2/metadata/`
- **ACS Endpoint**: `http://localhost:8000/saml2/acs/`
- **Required Attributes**: `uid`, `mail`
- **Optional Attributes**: `eduPersonAffiliation`

## Testing Steps

### 1. Install Dependencies
```bash
# Install IdP dependencies
cd saml_idp
pip install -r requirements.txt

# Install SP dependencies  
cd ../saml_sp
pip install -r requirements.txt
cd ..
```

### 2. Start Services
```bash
./start_services.sh
```

### 3. Test SAML Flow
1. Visit `http://localhost:8000/protected/` (SP protected page)
2. You should be redirected to IdP login: `http://localhost:8001/idp/login/`
3. Login with Django admin credentials
4. You should be redirected back to SP with SAML assertion

## Common Issues and Solutions

### Issue: "CustomProcessor not found"
- **Solution**: Ensure `saml_idp/custom_processor.py` exists and is properly imported

### Issue: "Certificate file not found"
- **Solution**: Run `./generate_certificates.sh` to create required certificates

### Issue: "Entity ID mismatch"
- **Solution**: Check that SP metadata entity ID matches SP settings

### Issue: "SAML assertion not received"
- **Check**:
  1. IdP and SP are running on correct ports
  2. Certificates are valid and accessible
  3. SP metadata is properly configured
  4. Custom processor is working correctly

### Issue: "Authentication failed"
- **Check**:
  1. User exists in Django admin
  2. User has proper permissions
  3. Custom processor `has_access()` method returns True

## Debugging

### Enable Debug Logging
Both IdP and SP have debug logging enabled in settings. Check console output for:
- SAML request/response details
- Certificate validation errors
- Attribute mapping issues

### Check Django Admin
- Ensure users exist in Django admin
- Check user permissions and groups
- Verify user attributes (username, email)

### Test Individual Components
1. **Test IdP**: Visit `http://localhost:8001/` - should show "SAML IdP is running successfully!"
2. **Test SP**: Visit `http://localhost:8000/` - should show "SAML SP is running successfully!"
3. **Test IdP Metadata**: Visit `http://localhost:8001/idp/metadata/` - should show IdP metadata
4. **Test SP Metadata**: Visit `http://localhost:8000/saml2/metadata/` - should show SP metadata

## Next Steps

1. **Test the basic flow** using the steps above
2. **Check logs** for any remaining errors
3. **Verify attribute mapping** in the custom processor
4. **Test with real user data** if needed
5. **Configure additional SAML settings** as required

## Support

If you continue to experience issues:
1. Check the Django console logs for both IdP and SP
2. Verify all certificates are properly generated and accessible
3. Ensure all required packages are installed
4. Check that ports 8000 and 8001 are available 