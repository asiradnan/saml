#!/bin/bash

# Multi-SP SAML Start Script
# This script starts both Service Providers for testing

echo "=== Multi-SP SAML Start Script ==="

# Function to start SP1
start_sp1() {
    echo "Starting SP1 (istiaque.me) on port 8000..."
    cd /home/shelby70/Downloads/saml/sp
    source env/bin/activate
    cd sp
    python3 manage.py runserver 127.0.0.1:8000 &
    SP1_PID=$!
    echo "SP1 started with PID: $SP1_PID"
}

# Function to start SP2
start_sp2() {
    echo "Starting SP2 (asiradnan.me) on port 8001..."
    cd /home/shelby70/Downloads/saml/sp2
    source env/bin/activate
    cd sp
    python3 manage.py runserver 127.0.0.1:8001 &
    SP2_PID=$!
    echo "SP2 started with PID: $SP2_PID"
}

# Function to stop all services
stop_services() {
    echo "Stopping services..."
    if [ ! -z "$SP1_PID" ]; then
        kill $SP1_PID 2>/dev/null
        echo "Stopped SP1 (PID: $SP1_PID)"
    fi
    if [ ! -z "$SP2_PID" ]; then
        kill $SP2_PID 2>/dev/null
        echo "Stopped SP2 (PID: $SP2_PID)"
    fi
    exit 0
}

# Trap Ctrl+C to stop services
trap stop_services INT

# Start both services
start_sp1
sleep 2
start_sp2

echo ""
echo "=== Services Started ==="
echo "SP1 (istiaque.me): http://127.0.0.1:8000/"
echo "SP2 (asiradnan.me): http://127.0.0.1:8001/"
echo ""
echo "Test URLs:"
echo "SP1 Login: http://127.0.0.1:8000/saml2/login/"
echo "SP2 Login: http://127.0.0.1:8001/saml2/login/"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for services to run
wait
