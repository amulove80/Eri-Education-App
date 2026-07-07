'use client';

import { useState } from 'react';
import { useStore } from '@/lib/store';
import { kalshiAPI } from '@/lib/kalshi-api';
import { Lock, Mail, TrendingUp, Key } from 'lucide-react';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [twoFactorCode, setTwoFactorCode] = useState('');
  const [apiKeyId, setApiKeyId] = useState('');
  const [privateKey, setPrivateKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [needsTwoFactor, setNeedsTwoFactor] = useState(false);
  const [useApiKey, setUseApiKey] = useState(false); // Default to email/password since API keys need backend

  const { setAuthenticated, setCredentials } = useStore();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      let success = false;
      
      if (useApiKey && apiKeyId && privateKey) {
        // Use API key authentication
        success = await kalshiAPI.loginWithApiKey(apiKeyId, privateKey);
        if (success) {
          setCredentials({ email: '', password: '', apiKey: `${apiKeyId}:${privateKey}` });
          setAuthenticated(true);
        } else {
          setError('Invalid API credentials. Please check your API Key ID and Private Key.');
        }
      } else {
        // Use email/password
        const result = await kalshiAPI.login({ email, password }, twoFactorCode);
        
        if (result === 'needs_2fa') {
          setNeedsTwoFactor(true);
          setError('');
          return;
        } else if (result === true) {
          setCredentials({ email, password });
          setAuthenticated(true);
        } else {
          setError(needsTwoFactor 
            ? 'Invalid 2FA code. Please try again.' 
            : 'Invalid email or password. Please try again.');
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
              <>
                <div>
                  <label htmlFor="apiKeyId" className="block text-sm font-medium text-slate-300 mb-2">
                    API Key ID
                  </label>
                  <div className="relative">
                    <Key className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      id="apiKeyId"
                      type="text"
                      value={apiKeyId}
                      onChange={(e) => setApiKeyId(e.target.value)}
                      className="w-full pl-11 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                      placeholder="Your API Key ID"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="privateKey" className="block text-sm font-medium text-slate-300 mb-2">
                    Private Key
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input
                      id="privateKey"
                      type="password"
                      value={privateKey}
                      onChange={(e) => setPrivateKey(e.target.value)}
                      className="w-full pl-11 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                      placeholder="Your Private Key"
                      required
                    />
                  </div>
                </div>

                <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                  <p className="text-xs text-red-400 font-semibold mb-2">
                    ⚠️ API Key authentication requires a backend server
                  </p>
                  <div className="space-y-1 text-xs text-slate-400">
                    <p>RSA private keys cannot be used securely in browser apps.</p>
                    <p className="pt-2 text-slate-300">
                      <strong>Please use Email/Password instead</strong> or set up a backend server.
                    </p>
                  </div>
                </div>
              </>
            ) : (
              <>
                {!needsTwoFactor ? (
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
                ) : (
                  <div>
                    <label htmlFor="twoFactorCode" className="block text-sm font-medium text-slate-300 mb-2">
                      Two-Factor Authentication Code
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                      <input
                        id="twoFactorCode"
                        type="text"
                        value={twoFactorCode}
                        onChange={(e) => setTwoFactorCode(e.target.value)}
                        className="w-full pl-11 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-center text-2xl tracking-widest"
                        placeholder="000000"
                        maxLength={6}
                        autoFocus
                        required
                      />
                    </div>
                    <p className="text-xs text-slate-400 mt-2 text-center">
                      Enter the code sent to your phone via SMS or from your authenticator app
                    </p>
                    <button
                      type="button"
                      onClick={() => {
                        setNeedsTwoFactor(false);
                        setTwoFactorCode('');
                        setError('');
                      }}
                      className="text-xs text-blue-400 hover:text-blue-300 mt-2 underline"
                    >
                      ← Back to login
                    </button>
                  </div>
                )}
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
              {isLoading ? 'Signing in...' : needsTwoFactor ? 'Verify Code' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-700">
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
              <h3 className="text-sm font-semibold text-yellow-400 mb-2">⚠️ Important Security Note</h3>
              <p className="text-xs text-slate-400 mb-3">
                <strong>For Google OAuth users:</strong> Unfortunately, Kalshi's API key system uses RSA private keys that cannot be safely used in browser apps.
              </p>
              <div className="space-y-1 text-xs text-slate-500">
                <p><strong>Options:</strong></p>
                <p>1. Create a Kalshi account with email/password (use that here)</p>
                <p>2. Set up a backend server to handle API key signing</p>
                <p>3. Use Kalshi directly for Google OAuth accounts</p>
                <p className="pt-2 text-red-400">
                  <strong>Never share your RSA private key with anyone!</strong>
                </p>
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
