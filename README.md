# SAML SSO Implementation - IdP & SP

This repository contains a complete SAML Single Sign-On implementation with both Identity Provider (IdP) and Service Provider (SP) components built with Django.

## 🏗️ Architecture Overview

```
┌─────────────────┐       SAML SSO        ┌─────────────────┐
│   Identity      │◄─────────────────────►│   Service       │
│   Provider      │                       │   Provider      │
│   (Port 9000)   │                       │   (Port 8000)   │
└─────────────────┘                       └─────────────────┘
```

## 📁 Project Structure

```
saml/
├── idp/                    # Identity Provider
│   ├── env/               # Python virtual environment
│   ├── idp/               # Django project
│   │   ├── certificates/  # SSL certificates
│   │   ├── templates/     # HTML templates
│   │   ├── idp_app/       # Custom IdP app
│   │   └── manage.py      # Django management
│   └── README.md          # IdP documentation
│
├── sp/                     # Service Provider
│   ├── env/               # Python virtual environment
│   ├── sp/                # Django project
│   │   ├── certificates/  # SSL certificates
│   │   ├── templates/     # HTML templates
│   │   ├── sp_app/        # Custom SP app
│   │   ├── attribute_maps/# SAML attribute mapping
│   │   └── manage.py      # Django management
│   └── README.md          # SP documentation
│
└── README.md              # This file
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.12+
- OpenSSL (for certificate generation)
- curl (for testing)

### 1. Start the Identity Provider (IdP)
```bash
cd idp
source env/bin/activate
cd idp
python manage.py runserver localhost:9000
```

### 2. Start the Service Provider (SP)
```bash
# In a new terminal
cd sp
source env/bin/activate
cd sp
python manage.py runserver localhost:8000
```

### 3. Test SAML SSO
1. **Open SP**: Visit http://localhost:8000/
2. **Login**: Click "Login with SAML"
3. **Authenticate**: Use credentials `admin/admin123` at IdP
4. **Success**: Return to SP as authenticated user

## 🔧 Components

### Identity Provider (IdP) - Port 9000
- **Technology**: Django + djangosaml2idp
- **Purpose**: Authenticates users and provides SAML assertions
- **Entity ID**: `http://localhost:9000/idp/metadata`
- **Login**: admin/admin123

**Key Features:**
- ✅ SAML 2.0 compliant IdP
- ✅ User authentication with Django users
- ✅ Digital signing of responses and assertions
- ✅ Single Sign-On (SSO) support
- ✅ Single Logout (SLO) support
- ✅ Metadata generation

### Service Provider (SP) - Port 8000
- **Technology**: Django + djangosaml2
- **Purpose**: Consumes SAML assertions from IdP
- **Entity ID**: `http://localhost:8000/saml2/metadata/`

**Key Features:**
- ✅ SAML 2.0 compliant SP
- ✅ Automatic user creation from SAML attributes
- ✅ Session management
- ✅ Assertion validation
- ✅ Single Logout support
- ✅ Attribute mapping

## 🔐 Security Configuration

### Certificates
- Self-signed certificates for development
- Separate key pairs for IdP and SP
- Used for signing and encryption

### SAML Security Features
- **Response Signing**: ✅ Enabled
- **Assertion Signing**: ✅ Enabled
- **Request Signing**: ✅ Required by IdP
- **Assertion Encryption**: ✅ Supported
- **Signature Verification**: ✅ Enabled

## 🔄 SAML SSO Flow

1. **User Access**: User visits SP (http://localhost:8000/)
2. **SSO Initiation**: SP generates SAML AuthnRequest
3. **IdP Redirect**: User redirected to IdP (http://localhost:9000/idp/sso/post/)
4. **Authentication**: User authenticates at IdP (redirected to /idp/login/process/)
5. **SAML Response**: IdP sends signed SAML Response to SP
6. **Assertion Processing**: SP validates and processes SAML assertion
7. **User Creation**: SP creates/updates user based on SAML attributes
8. **Session Creation**: SP creates Django session for user
9. **Access Granted**: User can access SP resources

## 📊 Configuration Matrix

| Component | Port | Entity ID | Purpose |
|-----------|------|-----------|---------|
| IdP | 9000 | `http://localhost:9000/idp/metadata` | Authentication |
| SP | 8000 | `http://localhost:8000/saml2/metadata/` | Resource Access |

## 🧪 Testing & Validation

### Automated Flow Test
```bash
cd /path/to/saml
python test_saml.py
```

### Manual Testing
1. **IdP Metadata**: http://localhost:9000/idp/metadata/
2. **SP Metadata**: http://localhost:8000/saml2/metadata/
3. **SSO Flow**: Start at http://localhost:8000/ → Login
4. **User Profile**: http://localhost:8000/profile/ (after login)

### Automated Testing
```bash
# Test IdP metadata
curl -s "http://localhost:9000/idp/metadata/" | head -5

# Test SP metadata  
curl -s "http://localhost:8000/saml2/metadata/" | head -5

# Test SP home page
curl -s "http://localhost:8000/" | grep "SAML"
```

## 🔧 Customization

### Adding New SPs to IdP
Edit `idp/idp/idp/settings.py`:
```python
SAML_IDP_SPCONFIG = {
    'http://new-sp.example.com/metadata/': {
        'processor': 'djangosaml2idp.processors.BaseProcessor',
        'attribute_mapping': {
            'email': 'email',
            'first_name': 'first_name',
            'last_name': 'last_name',
        }
    }
}
```

### Modifying Attribute Mapping
Edit `sp/sp/attribute_maps/basic.py` to change how SAML attributes map to Django user fields.

## 📚 Documentation

- **IdP Documentation**: [idp/README.md](idp/README.md)
- **SP Documentation**: [sp/README.md](sp/README.md)
- **SAML 2.0 Specification**: [OASIS SAML 2.0](https://docs.oasis-open.org/security/saml/v2.0/)

## 🛠️ Development Notes

### Environment Setup
Each component has its own Python virtual environment with specific dependencies:
- **IdP**: djangosaml2idp, pysaml2, lxml
- **SP**: djangosaml2, pysaml2, lxml

### Database
Both IdP and SP use SQLite databases for simplicity. The IdP includes a pre-created admin user.

### Certificates
Self-signed certificates are generated automatically and stored in respective `certificates/` directories.

## 🚨 Production Considerations

This implementation is designed for development and testing. For production:

1. **Security**:
   - Use proper SSL certificates from a CA
   - Implement proper session security
   - Configure HTTPS endpoints
   - Use secure secret keys

2. **Database**:
   - Use production databases (PostgreSQL, MySQL)
   - Implement proper user management
   - Set up database backups

3. **Deployment**:
   - Use proper web servers (nginx, Apache)
   - Configure load balancing
   - Implement monitoring and logging
   - Use environment variables for configuration

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'djangosaml2'"**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Certificate errors**
   - Check certificates exist in `certificates/` directories
   - Verify certificate permissions

3. **Metadata not found**
   - Ensure both servers are running
   - Check port availability (8000, 9000)

4. **SAML Response errors**
   - Check clock synchronization
   - Verify entity IDs match configuration
   - Review Django debug logs
   - Ensure IdP URLs are properly configured

5. **Login redirect fails**
   - Verify IdP URL configuration in `idp/urls.py`
   - Check that djangosaml2idp URLs are included properly
   - Test individual endpoints with `python test_saml.py`

### Debug Information
Both applications run in debug mode with detailed error logging. Check the terminal output for specific error messages.

## 📞 Support

For issues and questions:
1. Check the component-specific README files
2. Review Django and SAML logs
3. Verify configuration against the documentation
4. Test individual components separately

---

## 🎯 Success Criteria

You've successfully set up SAML SSO when:
- ✅ IdP runs on http://localhost:9000
- ✅ SP runs on http://localhost:8000  
- ✅ Both metadata endpoints return valid XML
- ✅ SAML login flow works end-to-end
- ✅ User attributes are properly mapped
- ✅ Single logout functions correctly

**Happy SAML SSO testing! 🔐**
