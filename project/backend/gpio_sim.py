"""
GPIO Simulation Module

This module provides a simulation of the Raspberry Pi GPIO module for
development and testing on non-Raspberry Pi systems.
"""

import time
import threading

class GPIO:
    """Simulated GPIO class that mimics RPi.GPIO functionality"""
    
    # GPIO modes
    BCM = "BCM"
    BOARD = "BOARD"
    
    # Pin directions
    IN = "IN"
    OUT = "OUT"
    
    # Pull up/down resistors
    PUD_UP = "PULL_UP"
    PUD_DOWN = "PULL_DOWN"
    PUD_OFF = "PULL_OFF"
    
    # Pin states
    HIGH = 1
    LOW = 0
    
    # Store pin states
    _pins = {}
    _mode = None
    _event_callbacks = {}
    _event_threads = {}
    
    @classmethod
    def setmode(cls, mode):
        """Set the pin numbering mode"""
        cls._mode = mode
        print(f"GPIO mode set to {mode}")
    
    @classmethod
    def setup(cls, pin, direction, pull_up_down=None, initial=None):
        """Set up a GPIO pin"""
        cls._pins[pin] = cls.LOW if initial is None else initial
        pull_str = f" with pull {'up' if pull_up_down == cls.PUD_UP else 'down' if pull_up_down == cls.PUD_DOWN else 'off'}" if pull_up_down else ""
        print(f"GPIO pin {pin} set up as {'input' if direction == cls.IN else 'output'}{pull_str}")
    
    @classmethod
    def input(cls, pin):
        """Read the state of a GPIO pin"""
        state = cls._pins.get(pin, cls.LOW)
        print(f"Reading GPIO pin {pin}: {'HIGH' if state else 'LOW'}")
        return state
    
    @classmethod
    def output(cls, pin, state):
        """Set the state of a GPIO pin"""
        cls._pins[pin] = state
        print(f"Setting GPIO pin {pin} to {'HIGH' if state else 'LOW'}")
        
        # Trigger any registered event callbacks
        if pin in cls._event_callbacks:
            for callback in cls._event_callbacks[pin]:
                callback(pin)
    
    @classmethod
    def cleanup(cls, pin=None):
        """Clean up GPIO pins"""
        if pin is None:
            cls._pins.clear()
            cls._event_callbacks.clear()
            for thread in cls._event_threads.values():
                thread.stop()
            cls._event_threads.clear()
            print("All GPIO pins cleaned up")
        else:
            if pin in cls._pins:
                del cls._pins[pin]
            if pin in cls._event_callbacks:
                del cls._event_callbacks[pin]
            if pin in cls._event_threads:
                cls._event_threads[pin].stop()
                del cls._event_threads[pin]
            print(f"GPIO pin {pin} cleaned up")
    
    @classmethod
    def add_event_detect(cls, pin, edge, callback=None, bouncetime=None):
        """Add event detection to a GPIO pin"""
        if pin not in cls._event_callbacks:
            cls._event_callbacks[pin] = []
        
        if callback:
            cls._event_callbacks[pin].append(callback)
        
        edge_type = "rising" if edge == cls.RISING else "falling" if edge == cls.FALLING else "both"
        print(f"Added {edge_type} edge detection on GPIO pin {pin}")
    
    @classmethod
    def add_event_callback(cls, pin, callback):
        """Add a callback for an event already defined"""
        if pin not in cls._event_callbacks:
            cls._event_callbacks[pin] = []
        
        cls._event_callbacks[pin].append(callback)
        print(f"Added callback for GPIO pin {pin}")
    
    @classmethod
    def remove_event_detect(cls, pin):
        """Remove event detection for a GPIO pin"""
        if pin in cls._event_callbacks:
            del cls._event_callbacks[pin]
        if pin in cls._event_threads:
            cls._event_threads[pin].stop()
            del cls._event_threads[pin]
        print(f"Removed event detection from GPIO pin {pin}")
    
    # Additional constants for edge detection
    RISING = "RISING"
    FALLING = "FALLING"
    BOTH = "BOTH"
    
    # PWM simulation
    class PWM:
        """Simulated PWM class"""
        
        def __init__(self, pin, frequency):
            self.pin = pin
            self.frequency = frequency
            self.duty_cycle = 0
            self.running = False
            self._thread = None
            print(f"PWM initialized on GPIO pin {pin} at {frequency} Hz")
        
        def start(self, duty_cycle):
            """Start PWM with the specified duty cycle"""
            self.duty_cycle = duty_cycle
            self.running = True
            self._thread = threading.Thread(target=self._pwm_loop)
            self._thread.daemon = True
            self._thread.start()
            print(f"PWM started on GPIO pin {self.pin} with {duty_cycle}% duty cycle")
        
        def stop(self):
            """Stop PWM"""
            self.running = False
            if self._thread:
                self._thread.join(1)
                self._thread = None
            print(f"PWM stopped on GPIO pin {self.pin}")
        
        def ChangeDutyCycle(self, duty_cycle):
            """Change the duty cycle"""
            self.duty_cycle = duty_cycle
            print(f"PWM duty cycle changed to {duty_cycle}% on GPIO pin {self.pin}")
        
        def ChangeFrequency(self, frequency):
            """Change the frequency"""
            self.frequency = frequency
            print(f"PWM frequency changed to {frequency} Hz on GPIO pin {self.pin}")
        
        def _pwm_loop(self):
            """PWM simulation loop"""
            while self.running:
                if self.duty_cycle > 0:
                    GPIO.output(self.pin, GPIO.HIGH)
                    time.sleep((self.duty_cycle / 100) / self.frequency)
                
                if self.duty_cycle < 100:
                    GPIO.output(self.pin, GPIO.LOW)
                    time.sleep((1 - (self.duty_cycle / 100)) / self.frequency)

# For testing the simulation
if __name__ == "__main__":
    try:
        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Test output
        GPIO.output(18, GPIO.HIGH)
        print(f"Pin 18 state: {GPIO.input(18)}")
        GPIO.output(18, GPIO.LOW)
        print(f"Pin 18 state: {GPIO.input(18)}")
        
        # Test PWM
        pwm = GPIO.PWM(18, 100)
        pwm.start(50)
        time.sleep(1)
        pwm.ChangeDutyCycle(75)
        time.sleep(1)
        pwm.stop()
        
        # Test event detection
        def button_callback(channel):
            print(f"Button pressed on channel {channel}")
        
        GPIO.add_event_detect(23, GPIO.FALLING, callback=button_callback, bouncetime=200)
        
        # Simulate button press
        GPIO.output(23, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(23, GPIO.HIGH)
        
        time.sleep(1)
    finally:
        GPIO.cleanup()