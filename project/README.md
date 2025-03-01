# Token Dispenser System

A modern token dispenser system for arcade management, running on a Raspberry Pi 5.

## Overview

This project provides a complete solution for managing an arcade token dispenser, including:

- Modern React-based web interface
- Python backend for hardware control
- GPIO integration for Raspberry Pi
- Token and promotion management
- Daily reporting and statistics

## System Architecture

The system consists of three main components:

1. **Frontend**: A React application providing the user interface
2. **Backend API**: A Flask-based Python API that handles business logic
3. **Hardware Interface**: GPIO control for the Raspberry Pi to interact with physical components

## Hardware Requirements

- Raspberry Pi 5
- Token dispenser mechanism
- Bill acceptor
- Barrier sensor
- Buttons and other input devices

## Setup Instructions

### 1. Install Dependencies

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip3 install -r requirements.txt
```

### 2. Configure GPIO Pins

The system is pre-configured with the following GPIO pin assignments:

- ECOIN: 35
- SALIDA: 13
- AC: 16
- BOTON_ENTREGA: 26
- TEST: 4
- TEST1: 34
- TEST2: 35
- ENTHOPER: 32
- SALHOPER: 12
- BOTON: 36
- SAL1: 0
- BARRERA: 34

You can modify these assignments in the `backend/app.py` file if needed.

### 3. Start the System

```bash
# Start the backend API
cd backend
./run.sh

# In a separate terminal, start the frontend
npm run dev
```

## Features

- **Token Management**: Track and dispense tokens
- **Promotion System**: Configure and use different promotions
- **Daily Operations**: Open and close day with reporting
- **Hardware Simulation**: Test without physical hardware
- **Responsive UI**: Works on various screen sizes

## Development

### Simulation Mode

When not running on a Raspberry Pi, the system automatically uses a GPIO simulation module (`gpio_sim.py`) to allow development and testing on any computer.

### API Endpoints

The backend provides the following API endpoints:

- `/api/gpio/*`: GPIO control endpoints
- `/api/tokens/config`: Get/update token configuration
- `/api/tokens/stats`: Get token statistics
- `/api/tokens/dispense`: Dispense tokens
- `/api/tokens/promotion`: Use a promotion
- `/api/tokens/open-day`: Open a new day
- `/api/tokens/close-day`: Close the current day

## Production Deployment

For production deployment on a Raspberry Pi:

1. Clone this repository to the Raspberry Pi
2. Install dependencies
3. Set up the system to start automatically on boot
4. Configure the frontend to connect to the backend API

## License

This project is licensed under the MIT License - see the LICENSE file for details.