#!/bin/bash

echo "Starting SAML services..."
echo "Make sure you have the required packages installed:"
echo "  - For IdP: pip install -r saml_idp/requirements.txt"
echo "  - For SP: pip install -r saml_sp/requirements.txt"
echo ""

# Start IdP on port 8001
echo "Starting IdP on port 8001..."
cd saml_idp
python3 manage.py runserver 8001 &
IDP_PID=$!
cd ..

# Wait a moment for IdP to start
sleep 3

# Start SP on port 8000
echo "Starting SP on port 8000..."
cd saml_sp
python3 manage.py runserver 8000 &
SP_PID=$!
cd ..

echo ""
echo "Services started!"
echo "IdP: http://localhost:8001"
echo "SP: http://localhost:8000"
echo ""
echo "To test SAML flow:"
echo "1. Visit http://localhost:8000/protected/ (this will redirect to IdP)"
echo "2. Login at IdP"
echo "3. You should be redirected back to SP with SAML assertion"
echo ""
echo "To stop services, press Ctrl+C"

# Wait for user to stop
trap "echo 'Stopping services...'; kill $IDP_PID $SP_PID; exit" INT
wait 