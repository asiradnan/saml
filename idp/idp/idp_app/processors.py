from djangosaml2idp.processors import BaseProcessor
import logging

logger = logging.getLogger(__name__)


class CustomSAMLProcessor(BaseProcessor):
    """Custom SAML processor for handling attribute mapping"""
    
    def get_attributes(self, user):
        """Return user attributes for SAML response"""
        logger.info(f"CustomSAMLProcessor.get_attributes called for user: {user.username}")
        
        attributes = {}
        
        # Map Django user attributes to SAML attributes
        if hasattr(user, 'username') and user.username:
            attributes['uid'] = [user.username]
            logger.info(f"Added uid: {user.username}")
            
        if hasattr(user, 'email') and user.email:
            attributes['mail'] = [user.email]
            logger.info(f"Added mail: {user.email}")
            
        if hasattr(user, 'first_name') and user.first_name:
            attributes['cn'] = [user.first_name]
            logger.info(f"Added cn: {user.first_name}")
            
        if hasattr(user, 'last_name') and user.last_name:
            attributes['sn'] = [user.last_name]
            logger.info(f"Added sn: {user.last_name}")
            
        # Add staff and superuser status
        if hasattr(user, 'is_staff'):
            attributes['is_staff'] = ['true' if user.is_staff else 'false']
            
        if hasattr(user, 'is_superuser'):
            attributes['is_superuser'] = ['true' if user.is_superuser else 'false']
        
        logger.info(f"Final attributes: {attributes}")
        return attributes
