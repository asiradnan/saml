"""
Custom SAML signal handlers for processing attributes and updating user data
"""
import logging
from django.dispatch import receiver
from django.contrib.auth.models import User
from djangosaml2.signals import pre_user_save, post_authenticated

logger = logging.getLogger(__name__)

@receiver(pre_user_save, sender=User)
def custom_update_user(sender, instance, attributes, user_modified, **kwargs):
    """
    Signal handler to update user attributes from SAML data before saving
    """
    logger.debug(f"Processing SAML attributes for user: {instance.username}")
    logger.debug(f"Received attributes: {attributes}")
    
    # Track if we made any changes
    modified = False
    
    # Update first name
    if 'first_name' in attributes and attributes['first_name']:
        first_name = attributes['first_name'][0] if isinstance(attributes['first_name'], list) else attributes['first_name']
        if instance.first_name != first_name:
            instance.first_name = first_name
            modified = True
            logger.debug(f"Updated first_name to: {first_name}")
    
    # Try alternative attribute names for first name
    if not instance.first_name:
        for attr_name in ['cn', 'givenName']:
            if attr_name in attributes and attributes[attr_name]:
                first_name = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                instance.first_name = first_name
                modified = True
                logger.debug(f"Updated first_name from {attr_name} to: {first_name}")
                break
    
    # Update last name
    if 'last_name' in attributes and attributes['last_name']:
        last_name = attributes['last_name'][0] if isinstance(attributes['last_name'], list) else attributes['last_name']
        if instance.last_name != last_name:
            instance.last_name = last_name
            modified = True
            logger.debug(f"Updated last_name to: {last_name}")
    
    # Try alternative attribute names for last name
    if not instance.last_name:
        for attr_name in ['sn']:
            if attr_name in attributes and attributes[attr_name]:
                last_name = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                instance.last_name = last_name
                modified = True
                logger.debug(f"Updated last_name from {attr_name} to: {last_name}")
                break
    
    # Update email
    if 'email' in attributes and attributes['email']:
        email = attributes['email'][0] if isinstance(attributes['email'], list) else attributes['email']
        if instance.email != email:
            instance.email = email
            modified = True
            logger.debug(f"Updated email to: {email}")
    elif 'mail' in attributes and attributes['mail']:
        email = attributes['mail'][0] if isinstance(attributes['mail'], list) else attributes['mail']
        if instance.email != email:
            instance.email = email
            modified = True
            logger.debug(f"Updated email from mail to: {email}")
    
    # Check for email in urn:oid format (common in SAML)
    if not instance.email:
        for attr_name in attributes:
            if 'mail' in attr_name.lower() or '1.2.840.113549.1.9.1.1' in attr_name:
                email = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                instance.email = email
                modified = True
                logger.debug(f"Updated email from {attr_name} to: {email}")
                break
    
    if modified:
        logger.info(f"Modified user {instance.username} with SAML attributes")
    else:
        logger.debug(f"No modifications needed for user {instance.username}")
    
    return modified

@receiver(post_authenticated)
def store_saml_attributes_in_session(sender, user, session, attribute_mapping, attributes, **kwargs):
    """
    Signal handler to store SAML attributes in session after authentication
    """
    logger.debug(f"Storing SAML attributes in session for user: {user.username}")
    logger.debug(f"Attributes to store: {attributes}")
    
    # Store the attributes in session
    session['samlUserdata'] = attributes
    session['samlAttributeMapping'] = attribute_mapping
    session['samlNameId'] = getattr(user, 'username', 'unknown')
    
    # Save the session
    session.save()
    
    logger.info(f"Stored SAML attributes in session for user: {user.username}")
    logger.debug(f"Session keys after storing: {list(session.keys())}")
