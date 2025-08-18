# SAML Service Provider (SP) Setup

This is a Django-based SAML Service Provider implementation using `djangosaml2`.

## 🚀 Quick Start

### 1. Make sure the IdP is running
The IdP should be running on `http://localhost:9000`

### 2. Activate the Virtual Environment
```bash
source env/bin/activate
```

### 3. Start the SP Server
```bash
cd sp
python manage.py runserver localhost:8000
```

### 4. Access the SP
- **SP Home Page**: http://localhost:8000/
- **SP Metadata**: http://localhost:8000/saml2/metadata/
- **User Profile**: http://localhost:8000/profile/ (after login)

## 🔧 Testing SAML SSO

1. **Open the SP**: Visit http://localhost:8000/
2. **Click "Login with SAML"**: This will redirect you to the IdP
3. **Login at IdP**: Use credentials `admin/admin123`
4. **Return to SP**: After successful authentication, you'll be redirected back
5. **View Profile**: Check your user profile to see SAML attributes

## 📋 SP Configuration Details

### Entity Information
- **Entity ID**: `http://localhost:8000/saml2/metadata/`
- **Base URL**: `http://localhost:8000`

### SP Endpoints
- **ACS (Assertion Consumer Service)**: `http://localhost:8000/saml2/acs/`
- **SLS (Single Logout Service)**: `http://localhost:8000/saml2/ls/`
- **Metadata**: `http://localhost:8000/saml2/metadata/`

### IdP Configuration
- **IdP Entity ID**: `http://localhost:9000/idp/metadata`
- **SSO URL**: `http://localhost:9000/idp/sso/redirect/`
- **SLO URL**: `http://localhost:9000/idp/slo/redirect/`

## 🔐 Security Features

- ✅ SAML 2.0 compliant
- ✅ Digital signature verification
- ✅ Assertion validation
- ✅ Single Logout support
- ✅ Automatic user creation/update
- ✅ Secure session management

## 👤 User Attributes

The SP receives and maps these attributes from the IdP:

| SAML Attribute | Django User Field | Description |
|----------------|-------------------|-------------|
| `uid`          | `username`        | User identifier |
| `mail`         | `email`           | Email address |
| `cn`           | `first_name`      | First name |
| `sn`           | `last_name`       | Last name |

## 📁 Important Files

- `sp/settings.py` - SAML SP configuration
- `sp/urls.py` - URL routing including SAML endpoints
- `certificates/sp_private.key` - SP private key for signing
- `certificates/sp_public.cert` - SP public certificate
- `idp_metadata.xml` - IdP metadata (downloaded automatically)
- `attribute_maps/basic.py` - SAML attribute mapping

## 🛠️ Configuration Details

### Authentication Backends
The SP uses both Django's default authentication and SAML:
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
]
```

### SAML Configuration
Key configuration in `settings.py`:
- **Entity ID**: `http://localhost:8000/saml2/metadata/`
- **Required Attributes**: `uid` (username)
- **Optional Attributes**: `mail`, `cn`, `sn`
- **Metadata Source**: Local file (`idp_metadata.xml`)

## 🔄 SAML Flow

1. **User accesses SP**: Visits protected resource
2. **SP initiates SSO**: Generates SAML AuthnRequest
3. **Redirect to IdP**: User is redirected to IdP for authentication
4. **IdP authentication**: User logs in at IdP
5. **SAML Response**: IdP sends SAML Response to SP's ACS
6. **User creation/update**: SP creates or updates user based on SAML attributes
7. **Login complete**: User is logged into SP with Django session

## 🧪 Testing Scenarios

### Test 1: Basic SSO
1. Visit http://localhost:8000/
2. Click "Login with SAML"
3. Authenticate at IdP
4. Verify return to SP with user logged in

### Test 2: User Attributes
1. Complete SSO login
2. Visit http://localhost:8000/profile/
3. Verify SAML attributes are displayed
4. Check Django user fields are populated

### Test 3: Single Logout
1. Login via SAML
2. Click "Logout" in SP
3. Verify logout from both SP and IdP

## 🔍 Troubleshooting

### Common Issues

1. **"SAML Response not found"**
   - Check IdP is running on port 9000
   - Verify metadata is up to date

2. **Certificate errors**
   - Ensure certificates exist in `certificates/` directory
   - Check certificate permissions

3. **Attribute mapping issues**
   - Review `attribute_maps/basic.py`
   - Check IdP attribute configuration

### Debug Mode
The SP is configured with debug mode enabled. Check Django logs for detailed error information.

## 📚 Dependencies

- Django 5.2.5
- djangosaml2
- pysaml2
- lxml
- defusedxml

## 🚨 Security Notes

- This configuration is for development and testing
- Self-signed certificates are used (not for production)
- Debug mode is enabled
- For production:
  - Use proper SSL certificates
  - Disable debug mode
  - Configure proper security headers
  - Use environment variables for sensitive data

## 🔗 Integration Notes

This SP is specifically configured to work with the IdP running on `localhost:9000`. The configuration includes:

- Proper entity ID matching
- Correct endpoint URLs
- Compatible attribute mapping
- Synchronized certificates and metadata

Both IdP and SP should be running simultaneously for full SAML SSO functionality.
