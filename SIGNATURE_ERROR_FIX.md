# SAML Signature Error Fix

## 🐛 **Problem Analysis**

The error "IncorrectlySigned - Request was not signed correctly" occurred due to several configuration mismatches:

### **Root Causes:**

1. **URL Endpoint Mismatch**:

   - IdP was configured with `/sso/post/` endpoints
   - But Django SAML IdP library uses `/idp/sso/post/` by default
   - SP was trying to send requests to wrong URLs

2. **Certificate Verification Issues**:

   - IdP expects signed requests from SP (when `want_authn_requests_signed: True`)
   - IdP needs SP's public certificate to verify the signed requests
   - SP's certificate wasn't available to the IdP

3. **Metadata Configuration**:
   - IdP wasn't properly loading SP metadata for certificate validation

## ✅ **Fixes Applied**

### **1. URL Endpoint Corrections**

Fixed both IdP and SP configurations to use correct Django SAML IdP URLs:

```python
# Corrected URLs in both configs:
'https://idp.asiradnan.com/idp/sso/post/'      # Was: /sso/post/
'https://idp.asiradnan.com/idp/sso/redirect/'  # Was: /sso/redirect/
'https://idp.asiradnan.com/idp/slo/post/'      # Was: /slo/post/
'https://idp.asiradnan.com/idp/slo/redirect/'  # Was: /slo/redirect/
```

### **2. Certificate Management**

- ✅ Copied SP's public certificate to IdP: `sp_public.cert`
- ✅ Added SP metadata configuration to IdP settings
- ✅ Configured proper certificate paths for signature verification

### **3. Temporary Debug Configuration**

For testing and troubleshooting:

- ✅ Disabled signature requirements temporarily (`want_authn_requests_signed: False`)
- ✅ Disabled SP request signing temporarily (`authn_requests_signed: False`)
- ✅ Enabled debug mode in both IdP and SP

## 🧪 **Testing Steps**

### **Phase 1: Basic Flow Test (No Signatures)**

1. Deploy the updated configurations
2. Test SAML flow: Visit `https://istiaque.me/profile/`
3. Should redirect to IdP login without signature errors
4. After login, should redirect back to SP successfully

### **Phase 2: Re-enable Signatures (After Phase 1 works)**

Once basic flow works, gradually re-enable signatures:

1. **Enable SP request signing**:

   ```python
   # In SP settings.py
   'authn_requests_signed': True,
   'logout_requests_signed': True,
   ```

2. **Enable IdP signature verification**:

   ```python
   # In IdP settings.py
   'want_authn_requests_signed': True,
   ```

3. **Test again** - should work with proper signatures

### **Phase 3: Production Security**

Once everything works with signatures:

1. **Disable debug modes**:

   ```python
   # IdP settings.py
   'debug': False,

   # SP settings.py
   'debug': 0,
   ```

2. **Re-enable production security settings**

## 🔍 **Why This Error Occurred**

### **Technical Explanation:**

1. **SAML Request Signing**: When `want_authn_requests_signed: True`, the IdP expects all authentication requests from the SP to be digitally signed using the SP's private key.

2. **Signature Verification**: The IdP uses the SP's public certificate (from metadata) to verify that:

   - The request actually came from the trusted SP
   - The request wasn't tampered with in transit
   - The SP has the corresponding private key (proving identity)

3. **URL Routing**: Django SAML IdP has specific URL patterns:

   - `/idp/metadata/` - IdP metadata endpoint
   - `/idp/sso/post/` - Single Sign-On POST binding
   - `/idp/sso/redirect/` - Single Sign-On Redirect binding
   - `/idp/slo/post/` - Single Logout POST binding

4. **Certificate Chain**: The trust relationship works like this:
   ```
   SP signs request with sp_private.key
        ↓
   IdP verifies signature using sp_public.cert
        ↓
   If valid: Process authentication
   If invalid: Return "IncorrectlySigned" error
   ```

## 🚨 **Common SAML Signature Issues**

### **Certificate Problems:**

- Expired certificates
- Wrong certificate format (PEM vs DER)
- Certificate not accessible to IdP
- Certificate CN mismatch

### **Configuration Problems:**

- URL mismatches between SP and IdP configs
- Metadata not properly loaded
- Signature algorithms not matching
- Time synchronization issues (clock skew)

### **Network Problems:**

- Requests being modified by proxy/firewall
- SSL termination affecting signatures
- Content-encoding issues

## 📋 **Verification Checklist**

After applying fixes:

- [ ] SP can redirect to IdP without errors
- [ ] IdP login page loads correctly
- [ ] Authentication completes successfully
- [ ] User is redirected back to SP with SAML assertion
- [ ] SP processes the SAML response correctly
- [ ] User is logged into SP application

## 🔧 **Next Steps**

1. **Test the current configuration** with signatures disabled
2. **If successful**, gradually re-enable signatures as described above
3. **Monitor logs** for any remaining issues
4. **Restore production security settings** once fully working

The key insight is that SAML signature verification requires perfect alignment between certificates, URLs, and configuration on both sides of the SSO relationship.
