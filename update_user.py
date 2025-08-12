#!/usr/bin/env python3

import os
import sys
import django

# Setup Django
sys.path.append('/home/shelby70/Downloads/saml/saml_sp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saml_sp.settings')
django.setup()

from django.contrib.auth.models import User

def update_user():
    try:
        user = User.objects.get(username='hayremanush')
        print(f'Found user: {user.username}')
        print(f'Current info - Email: {user.email}, First: {user.first_name}, Last: {user.last_name}')
        
        # Update user information to match what SAML is sending
        user.first_name = 'Dom'
        user.last_name = 'Furaile Thush'
        user.email = 'finaldestination@gmail.com'
        user.save()
        
        print(f'Updated info - Email: {user.email}, First: {user.first_name}, Last: {user.last_name}')
        print('User information updated successfully!')
        
    except User.DoesNotExist:
        print('User hayremanush not found')
        print('Available users:')
        for u in User.objects.all():
            print(f'  - {u.username} ({u.email})')

if __name__ == '__main__':
    update_user()
