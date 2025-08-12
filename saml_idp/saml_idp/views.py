from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import logging
import traceback

# Configure logger
logger = logging.getLogger(__name__)

def home(request):
    """Simple home view for testing"""
    try:
        logger.info(f"IdP home page accessed from {request.META.get('REMOTE_ADDR')}")
        return HttpResponse("SAML IdP is running successfully!")
    except Exception as e:
        logger.error(f"Error in IdP home view: {str(e)}\n{traceback.format_exc()}")
        return HttpResponse("Service temporarily unavailable", status=500)

@login_required
def protected(request):
    """Protected view to test authentication"""
    try:
        username = request.user.username if request.user.is_authenticated else "Anonymous"
        logger.info(f"Protected IdP view accessed by user: {username}")
        return HttpResponse(f"Hello {username}! You are authenticated.")
    except Exception as e:
        logger.error(f"Error in IdP protected view: {str(e)}\n{traceback.format_exc()}")
        return HttpResponse("Authentication error occurred", status=500)

@csrf_exempt
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Basic health checks
        from django.db import connections
        from django.core.cache import cache
        
        # Check database connection
        db_conn = connections['default']
        db_conn.cursor()
        
        health_status = {
            "status": "healthy",
            "service": "SAML IdP",
            "database": "connected",
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