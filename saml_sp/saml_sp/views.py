from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    """Simple home view for testing"""
    return HttpResponse("SAML SP is running successfully!")

@login_required
def protected(request):
    """Protected view to test authentication"""
    return HttpResponse(f"Hello {request.user.username}! You are authenticated via SAML.") 