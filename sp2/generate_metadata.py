#!/usr/bin/env python3
import os
import sys
import django

# Set up Django environment
sys.path.insert(0, '/home/shelby70/Downloads/saml/sp2/sp')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sp.settings')
django.setup()

from saml2.config import Config as Saml2Config
from saml2.metadata import entity_descriptor

# Import settings
from django.conf import settings

# Create SAML config
config = Saml2Config()
config.load(settings.SAML_CONFIG)

# Generate metadata
metadata = entity_descriptor(config)

# Print the metadata
print(metadata.to_string().decode('utf-8'))
