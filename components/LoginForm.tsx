'use client';

import { useState } from 'react';
import { useStore } from '@/lib/store';
import { kalshiAPI } from '@/lib/kalshi-api';
import { Lock, Mail, TrendingUp, Key } from 'lucide-react';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [useApiKey, setUseApiKey] = useState(true); // Default to API key for OAuth users

  const { setAuthenticated, setCredentials } = useStore();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      let success = false;
      
      if (useApiKey && apiKey) {
        // Use API key authentication
        success = await kalshiAPI.loginWithApiKey(apiKey);
        if (success) {
          setCredentials({ email: '', password: '', apiKey });
          setAuthenticated(true);
        } else {
          setError('Invalid API key. Please check that you copied it correctly from Kalshi settings.');
        }
      } else {
        // Use email/password
        success = await kalshiAPI.login({ email, password });
        if (success) {
          setCredentials({ email, password });
          setAuthenticated(true);
        } else {
          setError('Invalid email or password. Please try again.');
        }
      }
    } catch (err) {
      setError('Login failed. Please try again.');
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-500/10 rounded-2xl mb-4">
            <TrendingUp className="w-8 h-8 text-blue-400" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-2">
            Kalshi Trading Platform
          </h1>
          <p className="text-slate-400 text-sm">
            Advanced Market Analysis & Automated Trading
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-slate-800/50 backdrop-blur-lg border border-slate-700 rounded-2xl p-8">
          <h2 className="text-xl font-bold text-white mb-6">Sign In</h2>
          
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="flex items-center justify-center gap-4 mb-4">
              <button
                type="button"
                onClick={() => setUseApiKey(true)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  useApiKey
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                API Key (Recommended)
              </button>
              <button
                type="button"
                onClick={() => setUseApiKey(false)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  !useApiKey
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                Email/Password
              </button>
            </div>

            {useApiKey ? (
              <div>
                <label htmlFor="apiKey" className="block text-sm font-medium text-slate-300 mb-2">
                  Kalshi API Key
                </label>
                <div className="relative">
                  <Key className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                  <input
                    id="apiKey"
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="w-full pl-11 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                    placeholder="Enter your Kalshi API key"
                    required
                  />
                </div>
                <p className="text-xs text-slate-400 mt-2">
                  Get your API key from your{' '}
                  <a
                    href="https://kalshi.com/settings/api"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 underline"
                  >
                    Kalshi account settings
                  </a>
                </p>
              </div>
            ) : (
              <>
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                    Email
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full pl-11 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                      placeholder="your@email.com"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      id="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full pl-11 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                      placeholder="••••••••"
                      required
                    />
                  </div>
                </div>
              </>
            )}

            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                <p className="text-sm text-red-400">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-700">
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-blue-400 mb-2">For Google OAuth Users</h3>
              <p className="text-xs text-slate-400 mb-3">
                If you sign in to Kalshi with Google, use <strong>API Key</strong> authentication:
              </p>
              <div className="space-y-1 text-xs text-slate-500">
                <p>1. Go to <a href="https://kalshi.com/settings/api" target="_blank" rel="noopener noreferrer" className="text-blue-400 underline">kalshi.com/settings/api</a></p>
                <p>2. Generate a new API key</p>
                <p>3. Copy and paste it above</p>
                <p className="pt-2 text-slate-400">• Credentials stored locally in browser only</p>
              </div>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="mt-8 grid grid-cols-3 gap-4">
          <Feature title="Smart Analysis" desc="AI-powered market insights" />
          <Feature title="Auto Trading" desc="Automated execution" />
          <Feature title="Risk Control" desc="Advanced risk management" />
        </div>

        {/* Disclaimer */}
        <div className="mt-8 text-center">
          <p className="text-xs text-slate-500">
            ⚠️ Trading involves risk. Past performance does not guarantee future results.
          </p>
        </div>
      </div>
    </div>
  );
}

function Feature({ title, desc }: { title: string; desc: string }) {
  return (
    <div className="text-center">
      <p className="text-sm font-semibold text-white mb-1">{title}</p>
      <p className="text-xs text-slate-400">{desc}</p>
    </div>
  );
}
