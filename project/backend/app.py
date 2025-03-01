#!/usr/bin/env python3
"""
Token Dispenser Backend API

This module provides a Flask API to control the token dispenser hardware
and manage the token dispenser business logic.
"""

import os
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# In production, use the real GPIO module
try:
    import RPi.GPIO as GPIO
    IS_RASPBERRY_PI = True
except ImportError:
    # If not on a Raspberry Pi, use the simulation module
    from gpio_sim import GPIO
    IS_RASPBERRY_PI = False

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- CONFIGURATION FILES ---
CONFIG_FILE = "config.json"
REGISTRO_FILE = "registro.json"

# --- GPIO PIN CONFIGURATION ---
PINS = {
    "ECOIN": 35,
    "SALIDA": 13,
    "AC": 16,
    "BOTON_ENTREGA": 26,
    "TEST": 4,
    "TEST1": 34,
    "TEST2": 35,
    "ENTHOPER": 32,
    "SALHOPER": 12,
    "BOTON": 36,
    "SAL1": 0,
    "BARRERA": 34
}

# --- INITIALIZE GPIO ---
def init_gpio():
    """Initialize GPIO pins"""
    GPIO.setmode(GPIO.BCM)
    
    # Setup input pins
    for pin in [PINS["ECOIN"], PINS["AC"], PINS["TEST"], PINS["TEST1"], 
                PINS["TEST2"], PINS["BOTON"], PINS["BARRERA"], PINS["ENTHOPER"]]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Setup output pins
    for pin in [PINS["SALIDA"], PINS["SALHOPER"], PINS["SAL1"]]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# --- CONFIGURATION MANAGEMENT ---
def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        config = {
            "token_value": 1.0,
            "promotions": {
                "promo1": {"price": 10, "tokens": 12},
                "promo2": {"price": 20, "tokens": 25},
                "promo3": {"price": 30, "tokens": 40}
            },
            "stats": {
                "tokens_dispensed": 0,
                "money_received": 0,
                "promo1_used": 0,
                "promo2_used": 0,
                "promo3_used": 0,
                "tokens_remaining": 100
            }
        }
        save_config(config)
        return config

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# --- REGISTRO MANAGEMENT ---
def load_registro():
    """Load registro from file"""
    if os.path.exists(REGISTRO_FILE):
        with open(REGISTRO_FILE, 'r') as f:
            return json.load(f)
    else:
        # Default registro
        registro = {
            "apertura": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "fichas_expendidas": 0,
            "dinero_ingresado": 0,
            "promociones_usadas": {
                "Promo 1": 0,
                "Promo 2": 0,
                "Promo 3": 0
            }
        }
        save_registro(registro)
        return registro

def save_registro(registro):
    """Save registro to file"""
    with open(REGISTRO_FILE, 'w') as f:
        json.dump(registro, f, indent=4)

# --- TOKEN DISPENSER FUNCTIONS ---
def dispense_tokens(count):
    """Dispense tokens using GPIO"""
    config = load_config()
    
    # Check if we have enough tokens
    if count <= 0 or count > config["stats"]["tokens_remaining"]:
        return False
    
    # Update stats
    config["stats"]["tokens_dispensed"] += count
    config["stats"]["tokens_remaining"] -= count
    config["stats"]["money_received"] += count * config["token_value"]
    save_config(config)
    
    # Dispense tokens using GPIO
    for _ in range(count):
        GPIO.output(PINS["SALIDA"], GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(PINS["SALIDA"], GPIO.LOW)
        time.sleep(0.4)
    
    return True

def use_promotion(promo_key):
    """Use a promotion"""
    config = load_config()
    
    # Map promo_key to config key
    promo_map = {
        "promo1": "promo1",
        "promo2": "promo2",
        "promo3": "promo3"
    }
    
    stats_map = {
        "promo1": "promo1_used",
        "promo2": "promo2_used",
        "promo3": "promo3_used"
    }
    
    if promo_key not in promo_map:
        return False
    
    config_key = promo_map[promo_key]
    stats_key = stats_map[promo_key]
    
    promo = config["promotions"][config_key]
    
    # Check if we have enough tokens
    if promo["tokens"] > config["stats"]["tokens_remaining"]:
        return False
    
    # Update stats
    config["stats"][stats_key] += 1
    config["stats"]["tokens_dispensed"] += promo["tokens"]
    config["stats"]["tokens_remaining"] -= promo["tokens"]
    config["stats"]["money_received"] += promo["price"]
    save_config(config)
    
    # Dispense tokens using GPIO
    for _ in range(promo["tokens"]):
        GPIO.output(PINS["SALIDA"], GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(PINS["SALIDA"], GPIO.LOW)
        time.sleep(0.4)
    
    return True

# --- API ROUTES ---

# GPIO API
@app.route('/api/gpio/set-pin', methods=['POST'])
def set_pin():
    """Set a GPIO pin state"""
    data = request.json
    pin = data.get('pin')
    state = data.get('state')
    
    if pin is None or state is None:
        return jsonify({"error": "Missing pin or state"}), 400
    
    try:
        GPIO.output(pin, state)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gpio/get-pin/<int:pin>', methods=['GET'])
def get_pin(pin):
    """Get a GPIO pin state"""
    try:
        state = GPIO.input(pin)
        return jsonify({"state": state})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gpio/pulse-pin', methods=['POST'])
def pulse_pin():
    """Pulse a GPIO pin (set HIGH then LOW after delay)"""
    data = request.json
    pin = data.get('pin')
    duration = data.get('duration', 200)
    
    if pin is None:
        return jsonify({"error": "Missing pin"}), 400
    
    try:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(duration / 1000)
        GPIO.output(pin, GPIO.LOW)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/gpio/dispense-tokens', methods=['POST'])
def api_dispense_tokens():
    """Dispense tokens using GPIO"""
    data = request.json
    count = data.get('count')
    
    if count is None:
        return jsonify({"error": "Missing count"}), 400
    
    try:
        success = dispense_tokens(count)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Token Service API
@app.route('/api/tokens/config', methods=['GET'])
def get_config():
    """Get token service configuration"""
    config = load_config()
    return jsonify({
        "tokenValue": config["token_value"],
        "promotions": {
            "promo1": config["promotions"]["promo1"],
            "promo2": config["promotions"]["promo2"],
            "promo3": config["promotions"]["promo3"]
        }
    })

@app.route('/api/tokens/config', methods=['POST'])
def update_config():
    """Update token service configuration"""
    data = request.json
    config = load_config()
    
    if "tokenValue" in data:
        config["token_value"] = data["tokenValue"]
    
    if "promotions" in data:
        promotions = data["promotions"]
        if "promo1" in promotions:
            config["promotions"]["promo1"] = promotions["promo1"]
        if "promo2" in promotions:
            config["promotions"]["promo2"] = promotions["promo2"]
        if "promo3" in promotions:
            config["promotions"]["promo3"] = promotions["promo3"]
    
    save_config(config)
    
    return jsonify({
        "tokenValue": config["token_value"],
        "promotions": {
            "promo1": config["promotions"]["promo1"],
            "promo2": config["promotions"]["promo2"],
            "promo3": config["promotions"]["promo3"]
        }
    })

@app.route('/api/tokens/stats', methods=['GET'])
def get_stats():
    """Get token service statistics"""
    config = load_config()
    return jsonify({
        "tokensDispensed": config["stats"]["tokens_dispensed"],
        "moneyReceived": config["stats"]["money_received"],
        "promo1Used": config["stats"]["promo1_used"],
        "promo2Used": config["stats"]["promo2_used"],
        "promo3Used": config["stats"]["promo3_used"],
        "tokensRemaining": config["stats"]["tokens_remaining"]
    })

@app.route('/api/tokens/dispense', methods=['POST'])
def api_tokens_dispense():
    """Dispense tokens"""
    data = request.json
    count = data.get('count')
    
    if count is None:
        return jsonify({"error": "Missing count"}), 400
    
    success = dispense_tokens(count)
    return jsonify({"success": success})

@app.route('/api/tokens/promotion', methods=['POST'])
def api_use_promotion():
    """Use a promotion"""
    data = request.json
    promotion = data.get('promotion')
    
    if promotion is None:
        return jsonify({"error": "Missing promotion"}), 400
    
    success = use_promotion(promotion)
    return jsonify({"success": success})

@app.route('/api/tokens/open-day', methods=['POST'])
def api_open_day():
    """Open day (reset daily counters)"""
    config = load_config()
    
    # Reset daily counters but keep tokens remaining
    config["stats"]["tokens_dispensed"] = 0
    config["stats"]["money_received"] = 0
    config["stats"]["promo1_used"] = 0
    config["stats"]["promo2_used"] = 0
    config["stats"]["promo3_used"] = 0
    
    save_config(config)
    
    # Create new registro
    registro = {
        "apertura": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "fichas_expendidas": 0,
        "dinero_ingresado": 0,
        "promociones_usadas": {
            "Promo 1": 0,
            "Promo 2": 0,
            "Promo 3": 0
        }
    }
    save_registro(registro)
    
    return jsonify({"success": True})

@app.route('/api/tokens/close-day', methods=['POST'])
def api_close_day():
    """Close day and get report"""
    config = load_config()
    registro = load_registro()
    
    # Update registro with closing time
    registro["cierre"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_registro(registro)
    
    # Get report
    report = {
        "tokensDispensed": config["stats"]["tokens_dispensed"],
        "moneyReceived": config["stats"]["money_received"],
        "promo1Used": config["stats"]["promo1_used"],
        "promo2Used": config["stats"]["promo2_used"],
        "promo3Used": config["stats"]["promo3_used"],
        "tokensRemaining": config["stats"]["tokens_remaining"]
    }
    
    # Reset daily counters but keep tokens remaining
    config["stats"]["tokens_dispensed"] = 0
    config["stats"]["money_received"] = 0
    config["stats"]["promo1_used"] = 0
    config["stats"]["promo2_used"] = 0
    config["stats"]["promo3_used"] = 0
    
    save_config(config)
    
    return jsonify(report)

# --- MAIN ENTRY POINT ---
if __name__ == '__main__':
    try:
        init_gpio()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()