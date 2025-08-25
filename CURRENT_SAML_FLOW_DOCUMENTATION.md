# Current SAML Project Flow Documentation

## Architecture Overview

Your project implements a **Multi-SP SAML SSO System** with the following components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Identity      │    │   Service       │    │   Service       │
│   Provider      │    │   Provider 1    │    │   Provider 2    │
│   (IdP)         │    │   (SP1)         │    │   (SP2)         │
│                 │    │                 │    │                 │
│ idp.asiradnan   │◄──►│ istiaque.me     │    │ asiradnan.me    │
│    .com         │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Current Authentication Flow - ACTUAL BEHAVIOR

### What Actually Happens Now:

```
┌─────────────────────────────────────────────────────────────┐
│                    ACTUAL CURRENT FLOW                     │
│                  (Not True SSO/SLO)                        │
└─────────────────────────────────────────────────────────────┘

User Journey:
1. Visit SP1 (istiaque.me) → NOT logged in → Must click "Login"
2. Login to SP1 → Credentials required → Logged into SP1 ✓
3. Visit SP2 (asiradnan.me) → NOT logged in → Must click "Login" AGAIN
4. Login to SP2 → NO credentials required (IdP remembers) → Logged into SP2 ✓
5. Logout from SP1 → Only SP1 logged out → SP2 still logged in ❌
```

### Flow 1: User Accesses SP1 (istiaque.me)

```
1. User visits: https://istiaque.me/
   └── SP1 checks local session: user.is_authenticated = False
   └── Shows login page (not automatically redirected)

2. User manually clicks "Login" → /saml2/login/

3. SP1 generates SAML AuthnRequest
   ├── Entity ID: https://istiaque.me/saml2/metadata/
   └── Redirects to IdP

4. IdP receives request → User must enter credentials
   └── Creates IdP session at idp.asiradnan.com

5. IdP sends SAML Response back to SP1

6. SP1 creates LOCAL session
   ├── Database: sp/db.sqlite3
   ├── Cookie domain: istiaque.me
   └── User logged into SP1 ✓
```

### Flow 2: Same User Accesses SP2 (asiradnan.me)

```
1. User visits: https://asiradnan.me/
   └── SP2 checks local session: user.is_authenticated = False
   └── Reason: NO session cookie for asiradnan.me domain
   └── Shows login page (not automatically logged in)

2. User must manually click "Login" AGAIN → /saml2/login/

3. SP2 generates SAML AuthnRequest
   ├── Entity ID: https://asiradnan.me/saml2/metadata/
   └── Redirects to IdP

4. IdP receives request
   ├── IdP session exists ✓
   ├── Skips credential prompt ✓
   └── Immediately generates SAML Response

5. IdP sends SAML Response back to SP2

6. SP2 creates SEPARATE session
   ├── Database: sp2/db.sqlite3 (different database)
   ├── Cookie domain: asiradnan.me (different domain)
   └── User logged into SP2 ✓

Result: User logged into BOTH SPs but with INDEPENDENT sessions
```

### Flow 3: User Logs Out from SP1

```
1. User clicks logout on SP1

2. SP1 logout process:
   ├── Calls Django logout() function
   ├── Clears SP1 session from sp/db.sqlite3
   ├── Deletes istiaque.me session cookie
   └── User logged out from SP1 ✓

3. What DOESN'T happen:
   ├── IdP session remains active
   ├── SP2 session remains active
   └── SP2 cookie remains valid

4. Result: User still logged into SP2 ❌
```

## Key Components Breakdown

### 1. Identity Provider (IdP) - `idp.asiradnan.com`

**Location**: `/home/shelby70/Downloads/saml/idp/idp/`

**Key Files**:

- `settings.py` - IdP configuration
- `idp_app/processors.py` - Custom attribute processor
- `certificates/` - IdP signing certificates
- `db.sqlite3` - User accounts & SP registrations

**Responsibilities**:

- **Authentication**: Verify user credentials
- **Session Management**: Maintain IdP session
- **SP Registration**: Track registered Service Providers
- **Assertion Generation**: Create signed SAML responses
- **Attribute Mapping**: Convert user data to SAML attributes

**Database Tables**:

```sql
-- User accounts
auth_user (username, email, password, etc.)

-- Registered Service Providers
djangosaml2idp_serviceprovider (
    id=2, entity_id='https://istiaque.me/saml2/metadata/', active=True
    id=3, entity_id='https://asiradnan.me/saml2/metadata/', active=True
)
```

### 2. Service Provider 1 (SP1) - `istiaque.me`

**Location**: `/home/shelby70/Downloads/saml/sp/sp/`

**Key Files**:

- `settings.py` - SP1 SAML configuration
- `certificates/` - SP1 certificates + IdP public cert
- `idp_metadata.xml` - IdP metadata for validation
- `db.sqlite3` - Local user sessions

**Responsibilities**:

- **Request Generation**: Create SAML authentication requests
- **Response Processing**: Validate and consume SAML responses
- **Local Sessions**: Maintain SP1-specific user sessions
- **User Management**: Create/update local user accounts from SAML

### 3. Service Provider 2 (SP2) - `asiradnan.me`

**Location**: `/home/shelby70/Downloads/saml/sp2/sp/`

**Similar structure to SP1 but separate entity and sessions**

## Certificate & Signing Flow

### Signing Process:

```
1. IdP Signs SAML Response
   ├── Uses: idp/certificates/private.key
   ├── Public cert: idp/certificates/public.cert
   └── Ensures response authenticity

2. SP1 Validates IdP Signature
   ├── Uses: sp/certificates/idp_public.cert (copy of IdP cert)
   └── Verifies response came from trusted IdP

3. SP2 Validates IdP Signature
   ├── Uses: sp2/certificates/idp_public.cert (copy of IdP cert)
   └── Verifies response came from trusted IdP
```

### Certificate Chain:

```
IdP Certificate Authority
├── idp/certificates/public.cert (IdP signing cert)
├── sp/certificates/idp_public.cert (SP1 copy for validation)
└── sp2/certificates/idp_public.cert (SP2 copy for validation)
```

## Current Session Behavior

### What Happens Now:

```
User State After Full Flow:
├── IdP Session: ✓ Active (idp.asiradnan.com)
├── SP1 Session: ✓ Active (istiaque.me) - INDEPENDENT
└── SP2 Session: ✓ Active (asiradnan.me) - INDEPENDENT
```

### The Problem (Why No True SSO):

1. **Independent SP Sessions**: Each SP maintains its own session store
2. **No Session Sharing**: SP1 doesn't know about SP2 session state
3. **No Cross-SP Communication**: SPs don't communicate with each other
4. **Manual Logout**: Logging out of SP1 doesn't affect SP2

## Attribute Flow

### User Data Transformation:

```
Django User (IdP)           SAML Attributes            SP User Account
├── username: "john"    →   ├── uid: ["john"]       →  ├── username: "john"
├── email: "john@..."   →   ├── mail: ["john@..."]  →  ├── email: "john@..."
├── first_name: "John"  →   ├── cn: ["John"]        →  ├── first_name: "John"
└── last_name: "Doe"    →   └── sn: ["Doe"]         →  └── last_name: "Doe"
```

## URL Endpoints

### IdP Endpoints:

- **Metadata**: `https://idp.asiradnan.com/metadata`
- **SSO POST**: `https://idp.asiradnan.com/idp/sso/post/`
- **SSO Redirect**: `https://idp.asiradnan.com/idp/sso/redirect/`
- **SLO POST**: `https://idp.asiradnan.com/idp/slo/post/`
- **SLO Redirect**: `https://idp.asiradnan.com/idp/slo/redirect/`

### SP1 Endpoints:

- **Metadata**: `https://istiaque.me/saml2/metadata/`
- **Login**: `https://istiaque.me/saml2/login/`
- **ACS**: `https://istiaque.me/saml2/acs/`
- **SLO**: `https://istiaque.me/saml2/ls/`

### SP2 Endpoints:

- **Metadata**: `https://asiradnan.me/saml2/metadata/`
- **Login**: `https://asiradnan.me/saml2/login/`
- **ACS**: `https://asiradnan.me/saml2/acs/`
- **SLO**: `https://asiradnan.me/saml2/ls/`

## Current Limitations - ACTUAL PROBLEMS

### ❌ What DOESN'T Work (The Real Issues):

1. **Manual Login Required for Each SP**

   - User visits SP1 → Must manually click "Login"
   - User visits SP2 → Must manually click "Login" AGAIN
   - No automatic detection or redirect

2. **Completely Independent Sessions**

   - SP1 session: Database `sp/db.sqlite3`, Cookie domain `istiaque.me`
   - SP2 session: Database `sp2/db.sqlite3`, Cookie domain `asiradnan.me`
   - Sessions cannot communicate with each other

3. **No Single Logout**

   - Logout from SP1 → Only SP1 session cleared
   - SP2 remains logged in with active session
   - IdP session also remains active

4. **No Cross-Domain Session Sharing**
   - Different domains = Different cookies
   - Browser cannot share session between `istiaque.me` and `asiradnan.me`

### ✅ What DOES Work:

1. **Credential Reuse**

   - Login to SP1 → Creates IdP session
   - Login to SP2 → No password required (IdP remembers)

2. **Individual SAML Authentication**
   - Each SP authenticates successfully via SAML
   - User attributes properly mapped
   - SAML signatures validated correctly

### 🎯 Current User Experience:

```
EXPECTATION (True SSO):
Login SP1 → Visit SP2 → Automatically logged in → Logout SP1 → SP2 also logged out

REALITY (Partial SSO):
Login SP1 → Visit SP2 → Click "Login" (no password) → Logout SP1 → SP2 still logged in
```
