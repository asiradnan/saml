#!/bin/bash

# Generate certificates for SAML IdP and SP
echo "Generating SSL certificates for SAML implementation..."

# Create directories if they don't exist
mkdir -p saml_idp/certs
mkdir -p saml_sp/certificates

# Generate IdP private key and certificate
echo "Generating IdP certificates..."
openssl req -x509 -newkey rsa:2048 -keyout saml_idp/certs/mykey.pem -out saml_idp/certs/mycert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"

# Generate SP private key and certificate
echo "Generating SP certificates..."
openssl req -x509 -newkey rsa:2048 -keyout saml_sp/certificates/sp_private_key.pem -out saml_sp/certificates/sp_certificate.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"

# Set proper permissions
chmod 600 saml_idp/certs/mykey.pem
chmod 600 saml_sp/certificates/sp_private_key.pem
chmod 644 saml_idp/certs/mycert.pem
chmod 644 saml_sp/certificates/sp_certificate.pem

echo "Certificates generated successfully!"
echo "IdP certificates: saml_idp/certs/"
echo "SP certificates: saml_sp/certificates/" 