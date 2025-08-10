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

        # Map user attributes to SAML attributes
        if hasattr(user, 'username'):
            identity['uid'] = user.username

        if hasattr(user, 'email'):
            identity['mail'] = user.email

        # Add groups if available
        if hasattr(user, 'groups'):
            groups = [group.name for group in user.groups.all()]
            if groups:
                identity['eduPersonAffiliation'] = groups

        return identity

    def has_access(self, user):
        """
        Check if the user has access to the service.
        """
        return user.is_authenticated and user.is_active