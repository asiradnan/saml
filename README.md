# SAML Single Sign-On Implementation

A complete Django-based SAML Single Sign-On (SSO) system with Identity Provider (IdP) and Service Provider (SP) components.

## 🌟 Features

- **Complete SAML 2.0 Implementation**: Full SSO workflow with proper metadata exchange
- **Modern UI**: Beautiful, responsive login interface
- **Security Hardened**: Comprehensive security headers and best practices
- **Health Monitoring**: Built-in health check endpoints
- **Comprehensive Logging**: Detailed error handling and logging throughout
- **Production Ready**: Proper certificate management and configuration

## 🏗️ Architecture

```
┌─────────────────┐    SAML SSO     ┌─────────────────┐
│   Service       │◄──────────────►│   Identity      │
│   Provider      │                 │   Provider      │
│   (Port 8000)   │                 │   (Port 8001)   │
└─────────────────┘                 └─────────────────┘
```

- **Identity Provider (IdP)**: Handles user authentication and issues SAML assertions
- **Service Provider (SP)**: Consumes SAML assertions for user authorization

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- OpenSSL (for certificate generation)
- xmlsec1 library

### 1. Clone and Setup

```bash
git clone <repository-url>
cd saml
```

### 2. Generate Certificates

```bash
./generate_certificates.sh
```

### 3. Install Dependencies

```bash
# Create and activate virtual environments
python3 -m venv idp_env
python3 -m venv sp_env

# Install IdP dependencies
source idp_env/bin/activate
pip install Django==5.2.4 djangosaml2idp==0.7.2 pysaml2 defusedxml cryptography
deactivate

# Install SP dependencies
source sp_env/bin/activate
pip install Django==5.2.4 djangosaml2==1.11.1 pysaml2 defusedxml cryptography
deactivate
```

### 4. Setup Databases

```bash
# Setup IdP database
cd saml_idp
source ../idp_env/bin/activate
python3 manage.py migrate
python3 manage.py createsuperuser  # Username: admin, Password: admin123
deactivate
cd ..

# Setup SP database
cd saml_sp
source ../sp_env/bin/activate
python3 manage.py migrate
python3 manage.py createsuperuser  # Username: admin, Password: admin123
deactivate
cd ..
```

### 5. Start Services

```bash
# Start IdP (Terminal 1)
cd saml_idp && source ../idp_env/bin/activate && python3 manage.py runserver 8001

# Start SP (Terminal 2)
cd saml_sp && source ../sp_env/bin/activate && python3 manage.py runserver 8000
```

Or use the provided script:

```bash
./start_services.sh
```

## 🔧 Configuration

### Identity Provider (IdP) - Port 8001

**Key Configuration** (`saml_idp/saml_idp/settings.py`):

- **Entity ID**: `http://localhost:8001/idp/metadata/`
- **SSO Endpoints**: POST and Redirect bindings
- **Custom Processor**: Maps user attributes to SAML assertions
- **Certificate**: Auto-generated in `saml_idp/certs/`

### Service Provider (SP) - Port 8000

**Key Configuration** (`saml_sp/saml_sp/settings.py`):

- **Entity ID**: `http://localhost:8000/saml2/metadata/`
- **ACS Endpoint**: `http://localhost:8000/saml2/acs/`
- **Required Attributes**: `uid`, `mail`
- **Optional Attributes**: `eduPersonAffiliation`
- **Certificate**: Auto-generated in `saml_sp/certificates/`

## 🔐 Testing SAML Flow

1. **Access Protected Resource**:

   ```
   http://localhost:8000/protected/
   ```

2. **Automatic Redirect**: You'll be redirected to the IdP login page

3. **Login**: Use the admin credentials:

   - Username: `admin`
   - Password: `admin123`

4. **Success**: You'll be redirected back to the SP with SAML assertion

## 📡 API Endpoints

### Identity Provider (IdP)

- **Home**: `http://localhost:8001/`
- **Metadata**: `http://localhost:8001/idp/metadata/`
- **SSO Login**: `http://localhost:8001/idp/login/`
- **Health Check**: `http://localhost:8001/health/`
- **Admin**: `http://localhost:8001/admin/`

### Service Provider (SP)

- **Home**: `http://localhost:8000/`
- **Metadata**: `http://localhost:8000/saml2/metadata/`
- **Protected Page**: `http://localhost:8000/protected/`
- **Health Check**: `http://localhost:8000/health/`
- **Admin**: `http://localhost:8000/admin/`

## 🛡️ Security Features

### Security Headers

- **XSS Protection**: Browser XSS filter enabled
- **Content Type Protection**: MIME-type sniffing disabled
- **Clickjacking Protection**: X-Frame-Options set to DENY
- **HSTS**: HTTP Strict Transport Security (production)

### Session Security

- **HttpOnly Cookies**: Prevent JavaScript access
- **SameSite Protection**: CSRF protection
- **Session Timeout**: 1-hour expiration
- **Secure Cookies**: HTTPS-only in production

### SAML Security

- **Assertion Signing**: All assertions digitally signed
- **Response Signing**: SAML responses signed
- **Certificate Validation**: Proper certificate verification
- **Metadata Validation**: Automatic metadata validation

## 🏥 Monitoring & Health Checks

### Health Check Endpoints

- **IdP Health**: `GET http://localhost:8001/health/`
- **SP Health**: `GET http://localhost:8000/health/`

**Response Format**:

```json
{
  "status": "healthy",
  "service": "SAML IdP",
  "database": "connected",
  "timestamp": "..."
}
```

### Logging

Comprehensive logging is configured for:

- Authentication events
- SAML assertion processing
- Error conditions
- Health checks
- Security events

## 🔧 Advanced Configuration

### Production Deployment

1. **Enable HTTPS**:

   ```python
   # In settings.py
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **Update URLs**: Change `localhost` to your actual domain in:

   - IdP Entity ID
   - SP Entity ID
   - All endpoint URLs

3. **Certificate Management**: Replace self-signed certificates with proper CA-signed certificates

4. **Database**: Configure production database (PostgreSQL/MySQL)

### Custom Attribute Mapping

Edit `saml_idp/saml_idp/custom_processor.py`:

```python
def create_identity(self, user, sp_attribute_mapping, **kwargs):
    identity = {
        'uid': user.username,
        'mail': user.email,
        'givenName': user.first_name,
        'sn': user.last_name,
        # Add custom attributes
    }
    return identity
```

## 🛠️ Troubleshooting

### Common Issues

1. **Certificate Errors**: Re-run `./generate_certificates.sh`
2. **Port Conflicts**: Change ports in settings and restart
3. **Metadata Mismatch**: Verify entity IDs match configuration
4. **Authentication Fails**: Check user exists in Django admin

### Debug Mode

Enable detailed SAML debugging:

```python
SAML_CONFIG = {
    'debug': True,
    # ... other settings
}
```

### Log Analysis

Check application logs for detailed error information:

- Django console output
- SAML library debug messages
- Security-related warnings

## 📁 Project Structure

```
saml/
├── generate_certificates.sh      # Certificate generation script
├── start_services.sh            # Service startup script
├── TROUBLESHOOTING.md           # Detailed troubleshooting guide
├── README.md                    # This documentation
│
├── saml_idp/                    # Identity Provider
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── certs/                   # SSL certificates
│   ├── templates/               # Login templates
│   └── saml_idp/               # Django app
│       ├── settings.py         # IdP configuration
│       ├── urls.py             # URL routing
│       ├── views.py            # View handlers
│       └── custom_processor.py # SAML attribute processor
│
├── saml_sp/                     # Service Provider
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── metadata.xml            # SP metadata
│   ├── certificates/           # SSL certificates
│   ├── attribute_maps/         # Attribute mappings
│   └── saml_sp/               # Django app
│       ├── settings.py         # SP configuration
│       ├── urls.py            # URL routing
│       └── views.py           # View handlers
│
├── idp_env/                    # IdP virtual environment
├── sp_env/                     # SP virtual environment
└── ssoready-example-app-python-django-saml/  # Example directory
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and development purposes.

## 🆘 Support

For issues and questions:

1. Check the `TROUBLESHOOTING.md` guide
2. Review application logs
3. Verify configuration against this documentation
4. Test with the provided health check endpoints

---

**🎉 Congratulations!** Your SAML SSO system is now fully operational with modern security practices and comprehensive monitoring.
