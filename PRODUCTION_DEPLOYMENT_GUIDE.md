# SAML Production Deployment Configuration

## 🎯 Production Domains Configured

- **Identity Provider (IdP)**: `https://idp.asiradnan.com/`
- **Service Provider (SP)**: `https://istiaque.me/`

## ✅ Changes Made for Production

### 1. Security Settings

- ✅ `DEBUG = False` for both IdP and SP
- ✅ HTTPS enforcement enabled (`SECURE_SSL_REDIRECT = True`)
- ✅ HTTP Strict Transport Security (HSTS) enabled
- ✅ Additional security headers added:
  - Content-Type sniffing protection
  - XSS filter enabled
  - Clickjacking protection (X-Frame-Options: DENY)
  - Secure cookies for HTTPS

### 2. Domain Configuration

- ✅ IdP Base URL: `https://idp.asiradnan.com`
- ✅ SP Base URL: `https://istiaque.me`
- ✅ All SAML endpoints updated to use HTTPS production domains

### 3. SAML Configuration Updates

- ✅ IdP Entity ID: `https://idp.asiradnan.com/metadata`
- ✅ SP Entity ID: `https://istiaque.me/saml2/metadata/`
- ✅ Updated metadata files with production URLs
- ✅ Disabled debug mode for SAML libraries

### 4. Key SAML Endpoints

#### Identity Provider (IdP)

- Metadata: `https://idp.asiradnan.com/idp/metadata/`
- SSO POST: `https://idp.asiradnan.com/idp/sso/post/`
- SSO Redirect: `https://idp.asiradnan.com/idp/sso/redirect/`
- SLO POST: `https://idp.asiradnan.com/idp/slo/post/`
- SLO Redirect: `https://idp.asiradnan.com/idp/slo/redirect/`

#### Service Provider (SP)

- Metadata: `https://istiaque.me/saml2/metadata/`
- ACS (Assertion Consumer Service): `https://istiaque.me/saml2/acs/`
- SLS (Single Logout Service): `https://istiaque.me/saml2/ls/`
- SLS POST: `https://istiaque.me/saml2/ls/post/`

## 🔧 Deployment Steps

### 1. Deploy IdP to `https://idp.asiradnan.com/`

```bash
cd idp/idp
# Ensure your web server (nginx/apache) is configured for HTTPS
# Deploy the Django application with proper WSGI server (gunicorn/uwsgi)
python manage.py collectstatic --noinput
python manage.py migrate
```

### 2. Deploy SP to `https://istiaque.me/`

```bash
cd sp/sp
# Ensure your web server (nginx/apache) is configured for HTTPS
# Deploy the Django application with proper WSGI server (gunicorn/uwsgi)
python manage.py collectstatic --noinput
python manage.py migrate
```

### 3. SSL Certificate Requirements

- Ensure valid SSL certificates are installed for both domains
- The existing self-signed certificates in the project are for SAML signing/encryption, not HTTPS

### 4. Test SAML Flow

1. Visit: `https://istiaque.me/profile/` (protected resource)
2. Should redirect to: `https://idp.asiradnan.com/login/`
3. After authentication, should redirect back with SAML assertion
4. User should be logged into the SP

## 🔐 Certificate Management

### Current Status

- ✅ SAML signing certificates are configured
- ✅ IdP certificate: `idp/idp/certificates/private.key` & `public.cert`
- ✅ SP certificate: `sp/sp/certificates/sp_private.key` & `sp_public.cert`

### Important Notes

- The certificates in the project are for **SAML message signing/encryption**
- You still need **valid SSL/TLS certificates** for HTTPS on your web servers
- For production, consider using certificates from a trusted CA instead of self-signed

## 🚨 Important Pre-Deployment Checklist

### IdP Deployment

- [ ] Configure web server (nginx/apache) with SSL for `idp.asiradnan.com`
- [ ] Set up proper WSGI server (gunicorn/uwsgi)
- [ ] Create Django superuser for IdP admin access
- [ ] Run database migrations
- [ ] Configure static files serving

### SP Deployment

- [ ] Configure web server (nginx/apache) with SSL for `istiaque.me`
- [ ] Set up proper WSGI server (gunicorn/uwsgi)
- [ ] Run database migrations
- [ ] Configure static files serving

### SAML Registration

- [ ] Register the SP in the IdP's admin interface
- [ ] Verify metadata exchange between IdP and SP
- [ ] Test complete SAML authentication flow

## 🔍 Troubleshooting

### Common Issues

1. **SSL Certificate Errors**: Ensure valid certificates are installed on web servers
2. **CORS Issues**: May need to configure CORS headers if assets are served from different domains
3. **Static Files**: Ensure `collectstatic` is run and static files are properly served
4. **Database Permissions**: Ensure proper database permissions for both applications

### Debug Mode (Temporary)

If issues occur, you can temporarily enable debug mode by changing:

```python
DEBUG = True
# And for SAML debugging:
'debug': 1  # in SAML_CONFIG
```

## 🎉 Configuration Complete!

Your SAML SSO system is now configured for production with the domains:

- **IdP**: `https://idp.asiradnan.com/`
- **SP**: `https://istiaque.me/`

All localhost references have been updated to use your production domains, and proper security settings have been enabled for HTTPS deployment.
