import React, { useState, useEffect } from 'react';
import { Settings, Home, BarChart2, Activity, Power } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [stats, setStats] = useState({
    tokensDispensed: 0,
    moneyReceived: 0,
    promo1Used: 0,
    promo2Used: 0,
    promo3Used: 0,
    tokensRemaining: 0
  });
  const [promos, setPromos] = useState({
    promo1: { price: 0, tokens: 0 },
    promo2: { price: 0, tokens: 0 },
    promo3: { price: 0, tokens: 0 }
  });
  const [tokenValue, setTokenValue] = useState(1.0);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate loading data from backend
  useEffect(() => {
    // In a real implementation, this would fetch from your Python backend
    setTimeout(() => {
      setPromos({
        promo1: { price: 10, tokens: 12 },
        promo2: { price: 20, tokens: 25 },
        promo3: { price: 30, tokens: 40 }
      });
      setStats({
        tokensDispensed: 120,
        moneyReceived: 150,
        promo1Used: 5,
        promo2Used: 3,
        promo3Used: 2,
        tokensRemaining: 45
      });
      setTokenValue(1.5);
      setIsLoading(false);
    }, 1000);
  }, []);

  // Simulate dispensing tokens
  const dispenseTokens = (amount) => {
    if (amount > 0) {
      setStats(prev => ({
        ...prev,
        tokensDispensed: prev.tokensDispensed + amount,
        tokensRemaining: prev.tokensRemaining - amount
      }));
      // In a real implementation, this would call your Python backend
      console.log(`Dispensing ${amount} tokens`);
    }
  };

  // Simulate using a promotion
  const usePromotion = (promo) => {
    const promoData = promos[promo];
    setStats(prev => ({
      ...prev,
      [`${promo}Used`]: prev[`${promo}Used`] + 1,
      moneyReceived: prev.moneyReceived + promoData.price,
      tokensRemaining: prev.tokensRemaining - promoData.tokens
    }));
    // In a real implementation, this would call your Python backend
    console.log(`Using ${promo} - Price: ${promoData.price}, Tokens: ${promoData.tokens}`);
  };

  // Simulate opening day
  const openDay = () => {
    setStats({
      tokensDispensed: 0,
      moneyReceived: 0,
      promo1Used: 0,
      promo2Used: 0,
      promo3Used: 0,
      tokensRemaining: stats.tokensRemaining
    });
    // In a real implementation, this would call your Python backend
    console.log('Opening day');
  };

  // Simulate closing day
  const closeDay = () => {
    // In a real implementation, this would call your Python backend and generate a report
    console.log('Closing day with stats:', stats);
    alert(`Day closed with:\n- Tokens dispensed: ${stats.tokensDispensed}\n- Money received: $${stats.moneyReceived}`);
  };

  // Render loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl font-semibold">Loading token dispenser system...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Token Dispenser System</h1>
          <div className="flex items-center space-x-2">
            <span className="text-sm">Arcade Manager</span>
            <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold">AM</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-64 bg-gray-800 text-white">
          <nav className="p-4">
            <ul className="space-y-2">
              <li>
                <button 
                  onClick={() => setActiveTab('home')}
                  className={`flex items-center space-x-2 w-full p-3 rounded-lg ${activeTab === 'home' ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
                >
                  <Home size={20} />
                  <span>Dashboard</span>
                </button>
              </li>
              <li>
                <button 
                  onClick={() => setActiveTab('settings')}
                  className={`flex items-center space-x-2 w-full p-3 rounded-lg ${activeTab === 'settings' ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
                >
                  <Settings size={20} />
                  <span>Settings</span>
                </button>
              </li>
              <li>
                <button 
                  onClick={() => setActiveTab('reports')}
                  className={`flex items-center space-x-2 w-full p-3 rounded-lg ${activeTab === 'reports' ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
                >
                  <BarChart2 size={20} />
                  <span>Reports</span>
                </button>
              </li>
              <li>
                <button 
                  onClick={() => setActiveTab('simulation')}
                  className={`flex items-center space-x-2 w-full p-3 rounded-lg ${activeTab === 'simulation' ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
                >
                  <Activity size={20} />
                  <span>Simulation</span>
                </button>
              </li>
            </ul>

            <div className="mt-8 pt-4 border-t border-gray-700">
              <button className="flex items-center space-x-2 w-full p-3 rounded-lg text-red-400 hover:bg-gray-700">
                <Power size={20} />
                <span>Shutdown</span>
              </button>
            </div>
          </nav>
        </aside>

        {/* Content area */}
        <main className="flex-1 p-6 overflow-auto">
          {activeTab === 'home' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-800">Dashboard</h2>
              
              {/* Stats cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-gray-500 text-sm font-medium">Tokens Dispensed</h3>
                  <p className="text-3xl font-bold text-gray-800 mt-2">{stats.tokensDispensed}</p>
                </div>
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-gray-500 text-sm font-medium">Money Received</h3>
                  <p className="text-3xl font-bold text-gray-800 mt-2">${stats.moneyReceived.toFixed(2)}</p>
                </div>
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-gray-500 text-sm font-medium">Tokens Remaining</h3>
                  <p className="text-3xl font-bold text-gray-800 mt-2">{stats.tokensRemaining}</p>
                </div>
              </div>

              {/* Promotions usage */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Promotions Usage</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="border rounded-lg p-4">
                    <h4 className="font-medium">Promo 1</h4>
                    <p className="text-2xl font-bold mt-2">{stats.promo1Used}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      ${promos.promo1.price} for {promos.promo1.tokens} tokens
                    </p>
                  </div>
                  <div className="border rounded-lg p-4">
                    <h4 className="font-medium">Promo 2</h4>
                    <p className="text-2xl font-bold mt-2">{stats.promo2Used}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      ${promos.promo2.price} for {promos.promo2.tokens} tokens
                    </p>
                  </div>
                  <div className="border rounded-lg p-4">
                    <h4 className="font-medium">Promo 3</h4>
                    <p className="text-2xl font-bold mt-2">{stats.promo3Used}</p>
                    <p className="text-sm text-gray-500 mt-1">
                      ${promos.promo3.price} for {promos.promo3.tokens} tokens
                    </p>
                  </div>
                </div>
              </div>

              {/* Quick actions */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h3>
                <div className="flex flex-wrap gap-4">
                  <button 
                    onClick={() => dispenseTokens(1)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Dispense 1 Token
                  </button>
                  <button 
                    onClick={() => usePromotion('promo1')}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Use Promo 1
                  </button>
                  <button 
                    onClick={() => usePromotion('promo2')}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Use Promo 2
                  </button>
                  <button 
                    onClick={() => usePromotion('promo3')}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Use Promo 3
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-800">Settings</h2>
              
              {/* Token value setting */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Token Value</h3>
                <div className="flex items-center space-x-4">
                  <input 
                    type="number" 
                    value={tokenValue}
                    onChange={(e) => setTokenValue(parseFloat(e.target.value) || 0)}
                    className="border rounded-lg px-4 py-2 w-32"
                    step="0.01"
                    min="0"
                  />
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Save
                  </button>
                </div>
              </div>

              {/* Promotions settings */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Promotions</h3>
                
                {/* Promo 1 */}
                <div className="mb-6 p-4 border rounded-lg">
                  <h4 className="font-medium mb-3">Promo 1</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
                      <input 
                        type="number" 
                        value={promos.promo1.price}
                        onChange={(e) => setPromos({
                          ...promos,
                          promo1: {
                            ...promos.promo1,
                            price: parseFloat(e.target.value) || 0
                          }
                        })}
                        className="border rounded-lg px-4 py-2 w-full"
                        step="0.01"
                        min="0"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tokens</label>
                      <input 
                        type="number" 
                        value={promos.promo1.tokens}
                        onChange={(e) => setPromos({
                          ...promos,
                          promo1: {
                            ...promos.promo1,
                            tokens: parseInt(e.target.value) || 0
                          }
                        })}
                        className="border rounded-lg px-4 py-2 w-full"
                        min="0"
                      />
                    </div>
                  </div>
                </div>

                {/* Promo 2 */}
                <div className="mb-6 p-4 border rounded-lg">
                  <h4 className="font-medium mb-3">Promo 2</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
                      <input 
                        type="number" 
                        value={promos.promo2.price}
                        onChange={(e) => setPromos({
                          ...promos,
                          promo2: {
                            ...promos.promo2,
                            price: parseFloat(e.target.value) || 0
                          }
                        })}
                        className="border rounded-lg px-4 py-2 w-full"
                        step="0.01"
                        min="0"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tokens</label>
                      <input 
                        type="number" 
                        value={promos.promo2.tokens}
                        onChange={(e) => setPromos({
                          ...promos,
                          promo2: {
                            ...promos.promo2,
                            tokens: parseInt(e.target.value) || 0
                          }
                        })}
                        className="border rounded-lg px-4 py-2 w-full"
                        min="0"
                      />
                    </div>
                  </div>
                </div>

                {/* Promo 3 */}
                <div className="p-4 border rounded-lg">
                  <h4 className="font-medium mb-3">Promo 3</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
                      <input 
                        type="number" 
                        value={promos.promo3.price}
                        onChange={(e) => setPromos({
                          ...promos,
                          promo3: {
                            ...promos.promo3,
                            price: parseFloat(e.target.value) || 0
                          }
                        })}
                        className="border rounded-lg px-4 py-2 w-full"
                        step="0.01"
                        min="0"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tokens</label>
                      <input 
                        type="number" 
                        value={promos.promo3.tokens}
                        onChange={(e) => setPromos({
                          ...promos,
                          promo3: {
                            ...promos.promo3,
                            tokens: parseInt(e.target.value) || 0
                          }
                        })}
                        className="border rounded-lg px-4 py-2 w-full"
                        min="0"
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Save All Promotions
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-800">Reports & Day Management</h2>
              
              {/* Day management */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Day Management</h3>
                <div className="flex flex-wrap gap-4">
                  <button 
                    onClick={openDay}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Open Day
                  </button>
                  <button 
                    onClick={closeDay}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                  >
                    Close Day
                  </button>
                </div>
              </div>

              {/* Daily summary */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Daily Summary</h3>
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Metric</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Tokens Dispensed</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{stats.tokensDispensed}</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Money Received</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${stats.moneyReceived.toFixed(2)}</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Promo 1 Used</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{stats.promo1Used}</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Promo 2 Used</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{stats.promo2Used}</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Promo 3 Used</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{stats.promo3Used}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Export options */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Export Data</h3>
                <div className="flex flex-wrap gap-4">
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Export to CSV
                  </button>
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Print Report
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'simulation' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-800">Hardware Simulation</h2>
              
              {/* Input simulation */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Input Simulation</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium mb-3">Bill Acceptor</h4>
                    <div className="space-y-2">
                      <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 w-full">
                        Insert $1
                      </button>
                      <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 w-full">
                        Insert $5
                      </button>
                      <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 w-full">
                        Insert $10
                      </button>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium mb-3">Barrier Sensor</h4>
                    <button className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 w-full">
                      Trigger Barrier Sensor
                    </button>
                  </div>
                </div>
              </div>

              {/* Output simulation */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">Output Simulation</h3>
                <div className="space-y-4">
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 w-full">
                    Dispense Token
                  </button>
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-medium mb-2">GPIO Status</h4>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                        <span>SALIDA: Active</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full bg-red-500"></div>
                        <span>SALHOPER: Inactive</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full bg-red-500"></div>
                        <span>SAL1: Inactive</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full bg-green-500"></div>
                        <span>ECOIN: Active</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <p>© 2025 Token Dispenser System</p>
          <p className="text-sm">{new Date().toLocaleString()}</p>
        </div>
      </footer>
    </div>
  );
}

export default App;