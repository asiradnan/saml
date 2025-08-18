# Attribute mapping for SAML2
MAP = {
    "identifier": "urn:oasis:names:tc:SAML:2.0:attrname-format:basic",
    "fro": {
        'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': 'email',
        'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname': 'first_name',
        'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname': 'last_name',
        'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': 'username',
        'uid': 'username',
        'mail': 'email',
        'cn': 'first_name',
        'sn': 'last_name',
    },
    "to": {
        'email': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
        'first_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname',
        'last_name': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname',
        'username': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name',
    }
}
