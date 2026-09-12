import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Building2, HardHat, ShieldCheck, UserCheck, ArrowRight } from 'lucide-react';
import { UserRole } from '../types';

export const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, quickSwitch, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleManualLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login(email, password);
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Login failed');
    }
  };

  const handleQuickRole = async (role: UserRole) => {
    setError('');
    try {
      await quickSwitch(role);
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Quick login failed');
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(ellipse at 50% 30%, #172554 0%, #090d16 70%)',
      padding: '24px'
    }}>
      <div style={{
        maxWidth: '460px',
        width: '100%',
        background: 'var(--bg-card)',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '36px',
        boxShadow: 'var(--shadow-lg)'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Building2 color="#38bdf8" size={32} />
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>SiteFlow <span style={{ color: 'var(--primary)' }}>AI</span></h1>
          </div>
          <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
            Construction Inspection, Approval & IPC Management
          </p>
        </div>

        {error && (
          <div style={{
            background: 'var(--accent-rose-bg)',
            border: '1px solid rgba(244, 63, 94, 0.4)',
            color: '#fb7185',
            padding: '10px 14px',
            borderRadius: 'var(--radius-md)',
            fontSize: '0.82rem',
            marginBottom: '18px'
          }}>
            {error}
          </div>
        )}

        {/* 1-Click Demo Logins */}
        <div style={{ marginBottom: '24px' }}>
          <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '10px', textAlign: 'center' }}>
            1-Click Demo Authentication (Hackathon)
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <button
              type="button"
              className="btn btn-secondary"
              style={{ justifyContent: 'flex-start', padding: '10px 14px' }}
              onClick={() => handleQuickRole('CONTRACTOR')}
            >
              <HardHat color="#fbbf24" size={18} />
              <div style={{ textAlign: 'left', flex: 1 }}>
                <div style={{ fontSize: '0.84rem', fontWeight: 600, color: '#fff' }}>Contractor (Tariq Mahmood)</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Creates check requests & submits actual quantities</div>
              </div>
              <ArrowRight size={14} color="var(--text-dim)" />
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              style={{ justifyContent: 'flex-start', padding: '10px 14px' }}
              onClick={() => handleQuickRole('RE')}
            >
              <ShieldCheck color="#38bdf8" size={18} />
              <div style={{ textAlign: 'left', flex: 1 }}>
                <div style={{ fontSize: '0.84rem', fontWeight: 600, color: '#fff' }}>Resident Engineer (Engr. Bilal Khan)</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Conducts site inspections & approves quantities</div>
              </div>
              <ArrowRight size={14} color="var(--text-dim)" />
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              style={{ justifyContent: 'flex-start', padding: '10px 14px' }}
              onClick={() => handleQuickRole('CLIENT')}
            >
              <UserCheck color="#34d399" size={18} />
              <div style={{ textAlign: 'left', flex: 1 }}>
                <div style={{ fontSize: '0.84rem', fontWeight: 600, color: '#fff' }}>Client (Malik Zafar)</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Independent client approval & IPC certificate generation</div>
              </div>
              <ArrowRight size={14} color="var(--text-dim)" />
            </button>
          </div>
        </div>

        <div style={{ position: 'relative', textAlign: 'center', margin: '20px 0' }}>
          <hr style={{ borderColor: 'var(--border-color)' }} />
          <span style={{ position: 'absolute', top: '-10px', left: '50%', transform: 'translateX(-50%)', background: 'var(--bg-card)', padding: '0 10px', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
            or sign in with password
          </span>
        </div>

        <form onSubmit={handleManualLogin}>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="contractor@example.com"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '8px' }} disabled={isLoading}>
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
};
