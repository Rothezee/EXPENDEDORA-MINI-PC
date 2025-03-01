/**
 * Token Service API
 * 
 * This module provides an interface to interact with the token dispenser
 * business logic through a backend API.
 */

import GPIO from './gpio';

// Token service configuration
export interface TokenConfig {
  tokenValue: number;
  promotions: {
    promo1: { price: number; tokens: number; };
    promo2: { price: number; tokens: number; };
    promo3: { price: number; tokens: number; };
  };
}

// Token service statistics
export interface TokenStats {
  tokensDispensed: number;
  moneyReceived: number;
  promo1Used: number;
  promo2Used: number;
  promo3Used: number;
  tokensRemaining: number;
}

// Mock implementation for development/testing
class TokenServiceMock {
  private config: TokenConfig = {
    tokenValue: 1.0,
    promotions: {
      promo1: { price: 10, tokens: 12 },
      promo2: { price: 20, tokens: 25 },
      promo3: { price: 30, tokens: 40 }
    }
  };

  private stats: TokenStats = {
    tokensDispensed: 0,
    moneyReceived: 0,
    promo1Used: 0,
    promo2Used: 0,
    promo3Used: 0,
    tokensRemaining: 100
  };

  // Get current configuration
  async getConfig(): Promise<TokenConfig> {
    return this.config;
  }

  // Update configuration
  async updateConfig(newConfig: Partial<TokenConfig>): Promise<TokenConfig> {
    this.config = { ...this.config, ...newConfig };
    return this.config;
  }

  // Get current statistics
  async getStats(): Promise<TokenStats> {
    return this.stats;
  }

  // Dispense tokens
  async dispenseTokens(count: number): Promise<boolean> {
    if (count <= 0 || count > this.stats.tokensRemaining) {
      return false;
    }

    // Update stats
    this.stats.tokensDispensed += count;
    this.stats.tokensRemaining -= count;
    this.stats.moneyReceived += count * this.config.tokenValue;

    // Trigger GPIO to dispense tokens
    await GPIO.dispenseTokens(count);

    return true;
  }

  // Use a promotion
  async usePromotion(promoKey: 'promo1' | 'promo2' | 'promo3'): Promise<boolean> {
    const promo = this.config.promotions[promoKey];
    
    if (!promo || promo.tokens > this.stats.tokensRemaining) {
      return false;
    }

    // Update stats
    this.stats[`${promoKey}Used`]++;
    this.stats.tokensDispensed += promo.tokens;
    this.stats.tokensRemaining -= promo.tokens;
    this.stats.moneyReceived += promo.price;

    // Trigger GPIO to dispense tokens
    await GPIO.dispenseTokens(promo.tokens);

    return true;
  }

  // Open day (reset daily counters)
  async openDay(): Promise<boolean> {
    this.stats = {
      ...this.stats,
      tokensDispensed: 0,
      moneyReceived: 0,
      promo1Used: 0,
      promo2Used: 0,
      promo3Used: 0
    };
    return true;
  }

  // Close day and get report
  async closeDay(): Promise<TokenStats> {
    const report = { ...this.stats };
    
    // Reset daily counters but keep tokens remaining
    this.stats = {
      ...this.stats,
      tokensDispensed: 0,
      moneyReceived: 0,
      promo1Used: 0,
      promo2Used: 0,
      promo3Used: 0
    };
    
    return report;
  }
}

// Production implementation that communicates with the Python backend
class TokenServiceProduction {
  private apiBase: string;

  constructor(apiBase: string = '/api/tokens') {
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
      throw new Error(`Token Service API error: ${response.statusText}`);
    }

    return response.json();
  }

  async getConfig(): Promise<TokenConfig> {
    return this.apiCall('config');
  }

  async updateConfig(newConfig: Partial<TokenConfig>): Promise<TokenConfig> {
    return this.apiCall('config', 'POST', newConfig);
  }

  async getStats(): Promise<TokenStats> {
    return this.apiCall('stats');
  }

  async dispenseTokens(count: number): Promise<boolean> {
    const result = await this.apiCall('dispense', 'POST', { count });
    return result.success;
  }

  async usePromotion(promoKey: 'promo1' | 'promo2' | 'promo3'): Promise<boolean> {
    const result = await this.apiCall('promotion', 'POST', { promotion: promoKey });
    return result.success;
  }

  async openDay(): Promise<boolean> {
    const result = await this.apiCall('open-day', 'POST');
    return result.success;
  }

  async closeDay(): Promise<TokenStats> {
    return this.apiCall('close-day', 'POST');
  }
}

// Export the appropriate implementation based on environment
const isProduction = false; // Set to true when deploying to Raspberry Pi

export const TokenService = isProduction 
  ? new TokenServiceProduction() 
  : new TokenServiceMock();

export default TokenService;