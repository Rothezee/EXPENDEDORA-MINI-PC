#!/bin/bash

# This script starts the token dispenser backend API

# Check if running on a Raspberry Pi
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$PRETTY_NAME" == *"Raspberry Pi"* ]]; then
        echo "Running on Raspberry Pi"
        # Install required packages if not already installed
        if ! pip3 list | grep -q "Flask"; then
            echo "Installing required packages..."
            pip3 install -r requirements.txt
        fi
    else
        echo "Not running on Raspberry Pi, using simulation mode"
        # Install required packages if not already installed
        if ! pip3 list | grep -q "Flask"; then
            echo "Installing required packages..."
            pip3 install -r requirements.txt
        fi
    fi
fi

# Make the script executable
chmod +x app.py

# Start the backend API
echo "Starting token dispenser backend API..."
python3 app.py