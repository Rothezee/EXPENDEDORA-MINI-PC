/**
 * GPIO API Interface
 * 
 * This module provides an interface to interact with the Raspberry Pi GPIO
 * through a backend API. In production, this will communicate with the Python backend.
 */

// Define GPIO pin numbers (matching your Python configuration)
export const PINS = {
  ECOIN: 35,
  SALIDA: 13,
  AC: 16,
  BOTON_ENTREGA: 26,
  TEST: 4,
  TEST1: 34,
  TEST2: 35,
  ENTHOPER: 32,
  SALHOPER: 12,
  BOTON: 36,
  SAL1: 0,
  BARRERA: 34
};

// GPIO pin states
export const PIN_STATE = {
  HIGH: 1,
  LOW: 0
};

// Mock implementation for development/testing
class GPIOMock {
  private pinStates: Record<number, number> = {};

  constructor() {
    // Initialize all pins to LOW
    Object.values(PINS).forEach(pin => {
      this.pinStates[pin] = PIN_STATE.LOW;
    });
  }

  // Set pin output
  async setPin(pin: number, state: number): Promise<boolean> {
    console.log(`Setting pin ${pin} to ${state === PIN_STATE.HIGH ? 'HIGH' : 'LOW'}`);
    this.pinStates[pin] = state;
    return true;
  }

  // Get pin state
  async getPin(pin: number): Promise<number> {
    return this.pinStates[pin] || PIN_STATE.LOW;
  }

  // Pulse a pin (set HIGH then LOW after delay)
  async pulsePin(pin: number, durationMs: number = 200): Promise<boolean> {
    await this.setPin(pin, PIN_STATE.HIGH);
    
    return new Promise((resolve) => {
      setTimeout(async () => {
        await this.setPin(pin, PIN_STATE.LOW);
        resolve(true);
      }, durationMs);
    });
  }

  // Simulate dispensing tokens
  async dispenseTokens(count: number): Promise<boolean> {
    console.log(`Dispensing ${count} tokens`);
    
    for (let i = 0; i < count; i++) {
      await this.pulsePin(PINS.SALIDA);
      // Add delay between tokens
      if (i < count - 1) {
        await new Promise(resolve => setTimeout(resolve, 400));
      }
    }
    
    return true;
  }
}

// Production implementation that communicates with the Python backend
class GPIOProduction {
  private apiBase: string;

  constructor(apiBase: string = '/api/gpio') {
    this.apiBase = apiBase;
  }

  private async apiCall(endpoint: string, method: string = 'GET', data?: any): Promise<any> {
    const response = await fetch(`${this.apiBase}/${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) {
      throw new Error(`GPIO API error: ${response.statusText}`);
    }

    return response.json();
  }

  async setPin(pin: number, state: number): Promise<boolean> {
    const result = await this.apiCall('set-pin', 'POST', { pin, state });
    return result.success;
  }

  async getPin(pin: number): Promise<number> {
    const result = await this.apiCall(`get-pin/${pin}`);
    return result.state;
  }

  async pulsePin(pin: number, durationMs: number = 200): Promise<boolean> {
    const result = await this.apiCall('pulse-pin', 'POST', { pin, duration: durationMs });
    return result.success;
  }

  async dispenseTokens(count: number): Promise<boolean> {
    const result = await this.apiCall('dispense-tokens', 'POST', { count });
    return result.success;
  }
}

// Export the appropriate implementation based on environment
// In a real implementation, you would check if running on a Raspberry Pi
const isProduction = false; // Set to true when deploying to Raspberry Pi

export const GPIO = isProduction 
  ? new GPIOProduction() 
  : new GPIOMock();

export default GPIO;