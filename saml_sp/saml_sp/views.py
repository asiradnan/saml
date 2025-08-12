from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import logging
import traceback

# Configure logger
logger = logging.getLogger(__name__)

def home(request):
    """Simple home view for testing"""
    try:
        logger.info(f"SP home page accessed from {request.META.get('REMOTE_ADDR')}")
        return HttpResponse("SAML SP is running successfully!")
    except Exception as e:
        logger.error(f"Error in SP home view: {str(e)}\n{traceback.format_exc()}")
        return HttpResponse("Service temporarily unavailable", status=500)

@login_required
def protected(request):
    """Protected view to test authentication"""
    try:
        username = request.user.username if request.user.is_authenticated else "Anonymous"
        logger.info(f"Protected SP view accessed by user: {username}")
        
        # Build comprehensive user information display
        user_info_html = f"<h2>Hello {username}!</h2>"
        user_info_html += "<h3>Authentication successful via SAML</h3>"
        
        # Django User Model Information
        if request.user.is_authenticated:
            user_info_html += "<h4>Django User Information:</h4><ul>"
            user_info_html += f"<li><strong>Username:</strong> {request.user.username}</li>"
            user_info_html += f"<li><strong>Email:</strong> {request.user.email or 'Not provided'}</li>"
            user_info_html += f"<li><strong>First Name:</strong> {request.user.first_name or 'Not provided'}</li>"
            user_info_html += f"<li><strong>Last Name:</strong> {request.user.last_name or 'Not provided'}</li>"
            user_info_html += f"<li><strong>Is Active:</strong> {request.user.is_active}</li>"
            user_info_html += f"<li><strong>Is Staff:</strong> {request.user.is_staff}</li>"
            user_info_html += f"<li><strong>Is Superuser:</strong> {request.user.is_superuser}</li>"
            user_info_html += f"<li><strong>Date Joined:</strong> {request.user.date_joined}</li>"
            user_info_html += f"<li><strong>Last Login:</strong> {request.user.last_login or 'Never'}</li>"
            
            # User groups
            groups = request.user.groups.all()
            if groups:
                group_names = [group.name for group in groups]
                user_info_html += f"<li><strong>Groups:</strong> {', '.join(group_names)}</li>"
            else:
                user_info_html += "<li><strong>Groups:</strong> None</li>"
                
            user_info_html += "</ul>"
        
        # SAML Session Information - check multiple possible keys
        saml_data = None
        
        # Try different session keys that djangosaml2 might use
        session_keys_to_try = ['samlUserdata', 'saml_session', '_saml_session', 'saml2_session']
        
        for key in session_keys_to_try:
            if request.session.get(key):
                saml_data = request.session.get(key)
                break
        
        # Debug: show all session keys
        debug_info = f"<p><strong>Debug - Session keys:</strong> {list(request.session.keys())}</p>"
        
        if saml_data:
            user_info_html += "<h4>SAML Attributes Received:</h4><ul>"
            
            for attr_name, attr_values in saml_data.items():
                # Handle both single values and lists
                if isinstance(attr_values, list):
                    display_value = ', '.join(str(v) for v in attr_values)
                else:
                    display_value = str(attr_values)
                user_info_html += f"<li><strong>{attr_name}:</strong> {display_value}</li>"
            
            user_info_html += "</ul>"
        else:
            user_info_html += f"<h4>SAML Attributes:</h4><p>No SAML session data available</p>{debug_info}"
        
        # SAML Name ID if available
        if hasattr(request.session, 'get') and request.session.get('samlNameId'):
            name_id = request.session.get('samlNameId')
            user_info_html += f"<h4>SAML Name ID:</h4><p>{name_id}</p>"
        
        # Session expiration info
        if hasattr(request.session, 'get') and request.session.get('samlSessionIndex'):
            session_index = request.session.get('samlSessionIndex')
            user_info_html += f"<h4>SAML Session Index:</h4><p>{session_index}</p>"
        
        # Add styling for better presentation
        styled_html = f"""
        <html>
        <head>
            <title>SAML User Information</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h2 {{ color: #2c3e50; }}
                h3 {{ color: #27ae60; }}
                h4 {{ color: #3498db; margin-top: 30px; }}
                ul {{ background-color: #f8f9fa; padding: 20px; border-left: 4px solid #3498db; }}
                li {{ margin: 5px 0; }}
                strong {{ color: #2c3e50; }}
            </style>
        </head>
        <body>
            {user_info_html}
            <h4>Navigation:</h4>
            <p><a href="/">Home</a> | <a href="/admin/">Admin</a> | <a href="/api/user-profile/">API</a> | <a href="/logout/">Logout</a></p>
        </body>
        </html>
        """
        
        return HttpResponse(styled_html)
        
    except Exception as e:
        logger.error(f"Error in SP protected view: {str(e)}\n{traceback.format_exc()}")
        return HttpResponse("Authentication error occurred", status=500)

def get_user_attribute_value(request, attribute_name):
    """
    Utility function to get a specific SAML attribute value.
    
    Args:
        request: Django request object
        attribute_name: Name of the SAML attribute to retrieve
        
    Returns:
        The attribute value(s) or None if not found
    """
    if not hasattr(request.session, 'get'):
        return None
    
    # Try different session keys that djangosaml2 might use
    session_keys_to_try = ['samlUserdata', 'saml_session', '_saml_session', 'saml2_session']
    
    for key in session_keys_to_try:
        saml_data = request.session.get(key, {})
        if saml_data and attribute_name in saml_data:
            return saml_data.get(attribute_name)
    
    return None

def get_all_user_attributes(request):
    """
    Utility function to get all SAML attributes as a dictionary.
    
    Args:
        request: Django request object
        
    Returns:
        Dictionary of all SAML attributes or empty dict if none
    """
    if not hasattr(request.session, 'get'):
        return {}
    
    # Try different session keys that djangosaml2 might use
    session_keys_to_try = ['samlUserdata', 'saml_session', '_saml_session', 'saml2_session']
    
    for key in session_keys_to_try:
        saml_data = request.session.get(key, {})
        if saml_data:
            return saml_data
    
    return {}

@login_required 
def user_profile_api(request):
    """
    API endpoint to get user profile information in JSON format.
    This demonstrates how to access user attributes programmatically.
    """
    try:
        user_data = {
            'django_user': {
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_active': request.user.is_active,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
                'date_joined': request.user.date_joined.isoformat() if request.user.date_joined else None,
                'last_login': request.user.last_login.isoformat() if request.user.last_login else None,
                'groups': [group.name for group in request.user.groups.all()],
            },
            'saml_attributes': get_all_user_attributes(request),
            'saml_name_id': request.session.get('samlNameId'),
            'saml_session_index': request.session.get('samlSessionIndex'),
        }
        
        # Example of accessing specific attributes
        department = get_user_attribute_value(request, 'department')
        if department:
            user_data['department'] = department
            
        account_status = get_user_attribute_value(request, 'accountStatus')
        if account_status:
            user_data['account_status'] = account_status
            
        logger.info(f"User profile API accessed by: {request.user.username}")
        return JsonResponse(user_data, indent=2)
        
    except Exception as e:
        logger.error(f"Error in user profile API: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({'error': 'Failed to retrieve user profile'}, status=500)

@login_required
def simple_logout(request):
    """Simple logout view that doesn't use SAML logout to avoid session issues"""
    try:
        from django.contrib.auth import logout
        logout(request)
        logger.info(f"User logged out successfully")
        return HttpResponse("""
        <html>
        <head><title>Logged Out</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h2>Successfully Logged Out</h2>
            <p>You have been logged out successfully.</p>
            <p><a href="/">Return to Home</a> | <a href="/protected/">Login Again</a></p>
        </body>
        </html>
        """)
    except Exception as e:
        logger.error(f"Error in simple logout: {str(e)}\n{traceback.format_exc()}")
        return HttpResponse("Logout error occurred", status=500)

@csrf_exempt  
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Basic health checks
        from django.db import connections
        
        # Check database connection
        db_conn = connections['default']
        db_conn.cursor()
        
        health_status = {
            "status": "healthy",
            "service": "SAML SP",
            "database": "connected",
            "saml_metadata": "http://localhost:8000/saml2/metadata/",
            "timestamp": str(request.META.get('HTTP_DATE', 'unknown'))
        }
        
        logger.debug("Health check performed successfully")
        return JsonResponse(health_status)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({
            "status": "unhealthy", 
            "error": "Service check failed"
        }, status=503) 