# SAML User Attributes - Comprehensive Guide

This guide explains how to get more user information from the SAML Service Provider (SP) beyond just the username.

## 🎯 What We've Enhanced

Your SAML system now captures and provides access to comprehensive user information including:

### Basic User Information

- `uid` (username)
- `mail` (email)
- `cn` / `givenName` (first name)
- `sn` (last name)
- `displayName` (full name)

### User Status & Metadata

- `accountStatus` (active/inactive)
- `staffStatus` (staff/regular)
- `adminStatus` (admin/user)
- `memberSince` (date joined)
- `lastLogin` (last login timestamp)

### Group & Permission Information

- `eduPersonAffiliation` (groups)
- `memberOf` (groups - alternative format)
- `userPermissions` (user permissions)

### Organization Information

- `department` (user's department)
- `title` (job title)
- `telephoneNumber` (phone)
- `organization` (organization name)

## 🔧 How It Works

### 1. Identity Provider (IdP) Side

The IdP's `custom_processor.py` now extracts comprehensive user information from Django's User model and sends it in SAML assertions.

### 2. Service Provider (SP) Side

The SP is configured to:

- Accept all these attributes as optional
- Map them to appropriate user fields
- Store them in the session for access

## 🚀 How to Access User Information

### Method 1: Using the Enhanced Protected View

Visit `http://localhost:8000/protected/` after authentication to see a comprehensive display of all user information.

### Method 2: Using the User Profile API

Access `http://localhost:8000/api/user-profile/` to get user information in JSON format:

```json
{
  "django_user": {
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "is_staff": true,
    "is_superuser": true,
    "date_joined": "2024-01-15T10:30:00Z",
    "last_login": "2024-01-20T14:45:00Z",
    "groups": ["Administrators", "Editors"]
  },
  "saml_attributes": {
    "uid": ["admin"],
    "mail": ["admin@example.com"],
    "displayName": ["John Doe"],
    "accountStatus": ["active"],
    "staffStatus": ["staff"],
    "adminStatus": ["admin"],
    "memberSince": ["2024-01-15T10:30:00"],
    "lastLogin": ["2024-01-20T14:45:00"],
    "eduPersonAffiliation": ["Administrators", "Editors"]
  },
  "saml_name_id": "admin",
  "saml_session_index": "session_123456"
}
```

### Method 3: Programmatic Access in Your Views

Use the provided utility functions in your Django views:

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .views import get_user_attribute_value, get_all_user_attributes

@login_required
def my_custom_view(request):
    # Get a specific attribute
    department = get_user_attribute_value(request, 'department')
    account_status = get_user_attribute_value(request, 'accountStatus')

    # Get all SAML attributes
    all_attributes = get_all_user_attributes(request)

    # Access Django user information
    user = request.user

    context = {
        'department': department,
        'account_status': account_status,
        'all_saml_attributes': all_attributes,
        'user': user,
    }

    return render(request, 'my_template.html', context)
```

### Method 4: Direct Session Access

Access SAML data directly from the session:

```python
@login_required
def my_view(request):
    # Get all SAML user data
    saml_userdata = request.session.get('samlUserdata', {})

    # Get specific attributes
    email = saml_userdata.get('mail', [''])[0] if 'mail' in saml_userdata else ''
    groups = saml_userdata.get('eduPersonAffiliation', [])
    display_name = saml_userdata.get('displayName', [''])[0]

    # Note: SAML attributes are typically stored as lists
    # So access the first element for single-value attributes
```

## 📊 Complete Attribute Reference

| SAML Attribute         | Description              | Example Value                   |
| ---------------------- | ------------------------ | ------------------------------- |
| `uid`                  | Username                 | `["john.doe"]`                  |
| `mail`                 | Email address            | `["john.doe@company.com"]`      |
| `cn`                   | Common name (first name) | `["John"]`                      |
| `sn`                   | Surname (last name)      | `["Doe"]`                       |
| `givenName`            | Given name               | `["John"]`                      |
| `displayName`          | Full display name        | `["John Doe"]`                  |
| `accountStatus`        | Account status           | `["active"]`                    |
| `staffStatus`          | Staff status             | `["staff"]`                     |
| `adminStatus`          | Admin status             | `["admin"]`                     |
| `memberSince`          | Member since date        | `["2024-01-15T10:30:00"]`       |
| `lastLogin`            | Last login timestamp     | `["2024-01-20T14:45:00"]`       |
| `eduPersonAffiliation` | Group memberships        | `["Administrators", "Editors"]` |
| `memberOf`             | Groups (alternative)     | `["Administrators", "Editors"]` |
| `userPermissions`      | User permissions         | `["add_user", "change_user"]`   |
| `department`           | Department               | `["Engineering"]`               |
| `title`                | Job title                | `["Senior Developer"]`          |
| `telephoneNumber`      | Phone number             | `["+1-555-1234"]`               |
| `organization`         | Organization             | `["ACME Corp"]`                 |

## 🧪 Testing the Enhanced Features

### 1. Start Your Services

```bash
# Terminal 1 - Start IdP
cd saml_idp && source ../idp_env/bin/activate && python manage.py runserver 8001

# Terminal 2 - Start SP
cd saml_sp && source ../sp_env/bin/activate && python manage.py runserver 8000
```

### 2. Test Authentication Flow

1. Visit `http://localhost:8000/protected/`
2. Login with admin credentials at the IdP
3. View the comprehensive user information display

### 3. Test API Access

1. After authentication, visit `http://localhost:8000/api/user-profile/`
2. View the JSON response with all user data

## 🛠️ Customization Options

### Adding Custom Attributes

To add more custom attributes, modify three files:

#### 1. IdP Custom Processor (`saml_idp/saml_idp/custom_processor.py`)

```python
def create_identity(self, user, sp_attribute_mapping, **kwargs):
    identity = {
        # ... existing attributes ...
        'customAttribute': 'custom_value',
    }
    return identity
```

#### 2. SP Settings (`saml_sp/saml_sp/settings.py`)

```python
# Add to optional_attributes list
'optional_attributes': [
    # ... existing attributes ...
    'customAttribute',
],

# Add to SAML_ATTRIBUTE_MAPPING
SAML_ATTRIBUTE_MAPPING = {
    # ... existing mappings ...
    'customAttribute': ('custom_field', ),
}
```

#### 3. Attribute Maps (`saml_sp/attribute_maps/basic.py`)

```python
MAP = {
    "fro": {
        # ... existing mappings ...
        'customAttribute': 'custom_field',
    },
    "to": {
        # ... existing mappings ...
        'custom_field': 'customAttribute',
    }
}
```

### Creating User Profile Models

If you want to store additional user information, create a user profile model:

```python
# In your Django app models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
```

## 🔐 Security Considerations

1. **Attribute Validation**: Always validate SAML attributes before using them
2. **Session Security**: SAML attributes are stored in Django sessions - ensure proper session security
3. **Data Sensitivity**: Be careful with sensitive attributes like permissions or status
4. **Access Control**: Implement proper access controls for the user profile API

## 🐛 Troubleshooting

### Common Issues

1. **Missing Attributes**: Check if the IdP is sending the attributes and the SP is configured to accept them
2. **Attribute Format**: SAML attributes are usually lists - access `attribute[0]` for single values
3. **Session Expiry**: SAML attributes are session-based and will be lost when the session expires

### Debug Tips

1. Enable Django debug mode to see detailed error messages
2. Check the SAML metadata at `http://localhost:8000/saml2/metadata/`
3. View the raw session data: `print(request.session.get('samlUserdata'))`

## 📚 Additional Resources

- [djangosaml2 Documentation](https://djangosaml2.readthedocs.io/)
- [SAML 2.0 Specification](https://docs.oasis-open.org/security/saml/v2.0/)
- [Django User Model Reference](https://docs.djangoproject.com/en/stable/ref/contrib/auth/#user-model)

---

🎉 **Success!** You now have comprehensive access to user information through your SAML Service Provider. The system captures and provides access to detailed user attributes, status information, groups, permissions, and custom organizational data.
