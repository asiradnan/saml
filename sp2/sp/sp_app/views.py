from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def home(request):
    """Home page with SP information and login options"""
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'sp_entity_id': 'http://localhost:8000/saml2/metadata/',
        'login_url': '/saml2/login/',
        'metadata_url': '/saml2/metadata/',
    }
    return render(request, 'home.html', context)


@login_required
def profile(request):
    """User profile page showing SAML attributes"""
    context = {
        'user': request.user,
        'saml_session': getattr(request, 'saml', {}),
    }
    return render(request, 'profile.html', context)


def logout_view(request):
    """Custom logout view"""
    logout(request)
    return redirect('home')
