# SAML Identity Provider (IdP) Setup

This is a Django-based SAML Identity Provider implementation using `djangosaml2idp`.

## 🚀 Quick Start

### 1. Activate the Virtual Environment
```bash
source env/bin/activate
```

### 2. Start the IdP Server
```bash
cd idp
python manage.py runserver localhost:9000
```

### 3. Access the IdP
- **IdP Information Page**: http://localhost:9000/
- **Admin Interface**: http://localhost:9000/admin/
- **Login**: http://localhost:9000/login/
- **User Info**: http://localhost:9000/user-info/
- **Metadata**: http://localhost:9000/idp/metadata/

### 4. Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📋 IdP Configuration Details

### Entity Information
- **Entity ID**: `http://localhost:9000/idp/metadata`
- **Base URL**: `http://localhost:9000/idp`

### SSO Endpoints
- **HTTP-POST**: `http://localhost:9000/idp/sso/post/`
- **HTTP-Redirect**: `http://localhost:9000/idp/sso/redirect/`

### SLO Endpoints
- **HTTP-POST**: `http://localhost:9000/idp/slo/post/`
- **HTTP-Redirect**: `http://localhost:9000/idp/slo/redirect/`

### Security Features
- ✅ Response signing enabled
- ✅ Assertion signing enabled
- ✅ Requires signed authentication requests
- ✅ Self-signed certificates (for development)

## 🔧 Management Commands

### Generate Metadata
```bash
python manage.py generate_metadata
```

### Create Additional Users
```bash
python manage.py createsuperuser
```

## 📁 Important Files

- `certificates/private.key` - Private key for signing
- `certificates/public.cert` - Public certificate for verification
- `idp/settings.py` - SAML configuration
- `idp/urls.py` - URL routing

## 🔗 Service Provider Integration

To integrate a Service Provider with this IdP:

1. **Get the metadata**: Visit http://localhost:9000/idp/metadata/
2. **Configure your SP** with:
   - Entity ID: `http://localhost:9000/idp/metadata`
   - SSO URL: `http://localhost:9000/idp/sso/post/` (or redirect)
   - Public certificate from `certificates/public.cert`

## 🛠️ Development Notes

- This setup uses self-signed certificates suitable for development only
- For production, replace certificates with proper SSL certificates
- Update `ALLOWED_HOSTS` in settings for production domains
- Consider using environment variables for sensitive configuration

## 📖 User Attributes

The IdP provides these user attributes to Service Providers:
- Username
- Email
- First Name
- Last Name
- Staff Status
- Superuser Status

## 🔍 Testing

1. Start the IdP server
2. Visit http://localhost:9000/ to see IdP information
3. Login with admin credentials
4. Visit the metadata URL to verify XML generation
5. Use the metadata to configure a test Service Provider

## 📚 Dependencies

- Django 5.2.5
- djangosaml2idp
- pysaml2
- lxml

## 🚨 Security Notice

This configuration is for development and testing purposes only. For production use:
- Use proper SSL certificates
- Implement proper user authentication
- Configure appropriate security headers
- Use environment variables for sensitive data
- Enable proper logging and monitoring
