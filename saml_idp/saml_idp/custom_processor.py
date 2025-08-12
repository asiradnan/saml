from djangosaml2idp.processors import BaseProcessor
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomProcessor(BaseProcessor):
    """
    Custom processor for handling SAML authentication requests.
    This processor maps user attributes to SAML attributes.
    """

    def create_identity(self, user, sp_attribute_mapping, **kwargs):
        """
        Create the identity dictionary to be sent in the SAML assertion.
        """
        identity = {}

        # Basic user attributes - send both standard and direct names
        if hasattr(user, 'username'):
            identity['uid'] = user.username

        if hasattr(user, 'email') and user.email:
            identity['mail'] = user.email
            identity['email'] = user.email  # Direct mapping

        # Name attributes - send both standard and direct names
        if hasattr(user, 'first_name') and user.first_name:
            identity['cn'] = user.first_name  # Common Name
            identity['givenName'] = user.first_name
            identity['first_name'] = user.first_name  # Direct mapping

        if hasattr(user, 'last_name') and user.last_name:
            identity['sn'] = user.last_name  # Surname
            identity['last_name'] = user.last_name  # Direct mapping

        # Full name
        if hasattr(user, 'first_name') and hasattr(user, 'last_name'):
            full_name = f"{user.first_name} {user.last_name}".strip()
            if full_name:
                identity['displayName'] = full_name

        # User status and metadata - send as both text and boolean
        if hasattr(user, 'is_active'):
            identity['accountStatus'] = 'active' if user.is_active else 'inactive'
            identity['is_active'] = user.is_active

        if hasattr(user, 'is_staff'):
            identity['staffStatus'] = 'staff' if user.is_staff else 'regular'
            identity['is_staff'] = user.is_staff

        if hasattr(user, 'is_superuser'):
            identity['adminStatus'] = 'admin' if user.is_superuser else 'user'
            identity['is_superuser'] = user.is_superuser

        if hasattr(user, 'date_joined'):
            identity['memberSince'] = user.date_joined.isoformat()

        if hasattr(user, 'last_login') and user.last_login:
            identity['lastLogin'] = user.last_login.isoformat()

        # Groups and permissions
        if hasattr(user, 'groups'):
            groups = [group.name for group in user.groups.all()]
            if groups:
                identity['eduPersonAffiliation'] = groups
                identity['memberOf'] = groups

        # User permissions
        if hasattr(user, 'user_permissions'):
            permissions = [perm.codename for perm in user.user_permissions.all()]
            if permissions:
                identity['userPermissions'] = permissions

        # Custom user profile attributes (if you have a profile model)
        if hasattr(user, 'profile'):
            profile = user.profile
            if hasattr(profile, 'department') and profile.department:
                identity['department'] = profile.department
            if hasattr(profile, 'title') and profile.title:
                identity['title'] = profile.title
            if hasattr(profile, 'phone') and profile.phone:
                identity['telephoneNumber'] = profile.phone
            if hasattr(profile, 'organization') and profile.organization:
                identity['organization'] = profile.organization

        return identity

    def has_access(self, user):
        """
        Check if the user has access to the service.
        """
        return user.is_authenticated and user.is_active