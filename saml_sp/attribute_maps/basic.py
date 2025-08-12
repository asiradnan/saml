MAP = {
    "identifier": "urn:oasis:names:tc:SAML:2.0:attrname-format:basic",
    "fro": {
        # Basic user information
        'uid': 'username',
        'mail': 'email',
        'cn': 'first_name',
        'sn': 'last_name',
        'givenName': 'first_name',
        'displayName': 'full_name',
        
        # User status attributes
        'accountStatus': 'account_status',
        'staffStatus': 'staff_status', 
        'adminStatus': 'admin_status',
        
        # Temporal attributes
        'memberSince': 'date_joined',
        'lastLogin': 'last_login',
        
        # Group and permission attributes
        'eduPersonAffiliation': 'groups',
        'memberOf': 'groups',
        'userPermissions': 'permissions',
        
        # Organization attributes
        'department': 'department',
        'title': 'title',
        'telephoneNumber': 'phone',
        'organization': 'organization',
    },
    "to": {
        # Basic user information
        'username': 'uid',
        'email': 'mail',
        'first_name': 'cn',
        'last_name': 'sn',
        'full_name': 'displayName',
        
        # User status attributes
        'account_status': 'accountStatus',
        'staff_status': 'staffStatus',
        'admin_status': 'adminStatus',
        
        # Temporal attributes
        'date_joined': 'memberSince',
        'last_login': 'lastLogin',
        
        # Group and permission attributes
        'groups': 'eduPersonAffiliation',
        'permissions': 'userPermissions',
        
        # Organization attributes
        'department': 'department',
        'title': 'title',
        'phone': 'telephoneNumber',
        'organization': 'organization',
    }
}
