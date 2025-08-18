from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def idp_info(request):
    """Display basic IdP information"""
    context = {
        'entity_id': 'http://localhost:9000/idp/metadata',
        'sso_url_post': 'http://localhost:9000/idp/sso/post/',
        'sso_url_redirect': 'http://localhost:9000/idp/sso/redirect/',
        'slo_url_post': 'http://localhost:9000/idp/slo/post/',
        'slo_url_redirect': 'http://localhost:9000/idp/slo/redirect/',
        'metadata_url': 'http://localhost:9000/idp/metadata/',
    }
    return render(request, 'idp_info.html', context)


@login_required
def user_info(request):
    """Display current user information"""
    context = {
        'user': request.user,
    }
    return render(request, 'user_info.html', context)
