"""
Custom SAML middleware for processing attributes and updating user data
"""
import logging

logger = logging.getLogger(__name__)

class SAMLAttributeProcessorMiddleware:
    """
    Middleware to process SAML attributes and store them in session
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Process SAML attributes if user just authenticated
        if (hasattr(request, 'user') and 
            request.user.is_authenticated and 
            request.session.get('_auth_user_backend') == 'djangosaml2.backends.Saml2Backend' and
            not request.session.get('saml_attributes_processed')):
            
            self.process_saml_attributes(request)
        
        return response
    
    def process_saml_attributes(self, request):
        """
        Process SAML attributes for the authenticated user
        """
        try:
            logger.debug(f"Processing SAML attributes for user: {request.user.username}")
            
            # Get SAML session info from djangosaml2
            saml_session = getattr(request, 'saml_session', None)
            if saml_session and hasattr(saml_session, 'ava'):
                attributes = saml_session.ava
                logger.debug(f"Found SAML attributes: {attributes}")
                
                # Store attributes in session
                request.session['samlUserdata'] = attributes
                request.session['samlNameId'] = getattr(saml_session, 'name_id', request.user.username)
                request.session['samlSessionIndex'] = getattr(saml_session, 'session_index', None)
                
                # Update user fields
                self.update_user_from_attributes(request.user, attributes)
                
                # Mark as processed
                request.session['saml_attributes_processed'] = True
                request.session.save()
                
                logger.info(f"Processed and stored SAML attributes for user: {request.user.username}")
            else:
                logger.debug("No SAML session attributes found")
                
        except Exception as e:
            logger.error(f"Error processing SAML attributes: {str(e)}", exc_info=True)
    
    def update_user_from_attributes(self, user, attributes):
        """
        Update user fields from SAML attributes
        """
        modified = False
        
        try:
            # Update first name
            for attr_name in ['first_name', 'cn', 'givenName']:
                if attr_name in attributes and attributes[attr_name]:
                    first_name = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                    if user.first_name != first_name:
                        user.first_name = first_name
                        modified = True
                        logger.debug(f"Updated first_name to: {first_name}")
                    break
            
            # Update last name
            for attr_name in ['last_name', 'sn', 'surname']:
                if attr_name in attributes and attributes[attr_name]:
                    last_name = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                    if user.last_name != last_name:
                        user.last_name = last_name
                        modified = True
                        logger.debug(f"Updated last_name to: {last_name}")
                    break
            
            # Update email
            for attr_name in ['email', 'mail']:
                if attr_name in attributes and attributes[attr_name]:
                    email = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                    if user.email != email:
                        user.email = email
                        modified = True
                        logger.debug(f"Updated email to: {email}")
                    break
            
            # Check for email in urn:oid format
            if not user.email:
                for attr_name in attributes:
                    if 'mail' in attr_name.lower() or '1.2.840.113549.1.9.1.1' in attr_name:
                        email = attributes[attr_name][0] if isinstance(attributes[attr_name], list) else attributes[attr_name]
                        user.email = email
                        modified = True
                        logger.debug(f"Updated email from {attr_name} to: {email}")
                        break
            
            if modified:
                user.save()
                logger.info(f"Updated user {user.username} with SAML attributes")
                
        except Exception as e:
            logger.error(f"Error updating user attributes: {str(e)}", exc_info=True)
