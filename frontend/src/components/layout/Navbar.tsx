import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { HardHat, ShieldCheck, UserCheck, Bell, LogOut, CheckCircle2 } from 'lucide-react';
import { UserRole } from '../../types';

export const Navbar: React.FC = () => {
  const { user, role, quickSwitch, logout } = useAuth();

  const handleRoleSwitch = async (targetRole: UserRole) => {
    if (role === targetRole) return;
    try {
      await quickSwitch(targetRole);
    } catch (e) {
      console.error('Failed to switch role:', e);
    }
  };

  return (
    <header className="top-navbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-dim)', fontWeight: 500 }}>
          PROJECT: <strong style={{ color: '#fff' }}>SITEFLOW-5M</strong> (5 Marla Model)
        </span>
      </div>

      {/* Demo Quick Switcher Bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div className="role-switcher-bar">
          <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, paddingLeft: '6px' }}>
            DEMO ROLE:
          </span>
          <button
            type="button"
            className={`role-badge-btn ${role === 'CONTRACTOR' ? 'active-contractor' : ''}`}
            onClick={() => handleRoleSwitch('CONTRACTOR')}
            title="Switch session to Contractor (Tariq Mahmood)"
          >
            <HardHat size={14} />
            Contractor
          </button>
          <button
            type="button"
            className={`role-badge-btn ${role === 'RE' ? 'active-re' : ''}`}
            onClick={() => handleRoleSwitch('RE')}
            title="Switch session to Resident Engineer (Engr. Bilal Khan)"
          >
            <ShieldCheck size={14} />
            RE (Engineer)
          </button>
          <button
            type="button"
            className={`role-badge-btn ${role === 'CLIENT' ? 'active-client' : ''}`}
            onClick={() => handleRoleSwitch('CLIENT')}
            title="Switch session to Client (Malik Zafar)"
          >
            <UserCheck size={14} />
            Client
          </button>
        </div>

        {/* User Info & Logout */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', paddingLeft: '8px', borderLeft: '1px solid var(--border-color)' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#fff' }}>{user?.full_name}</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{user?.email}</div>
          </div>
          <button
            onClick={logout}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-dim)',
              cursor: 'pointer',
              padding: '6px',
              borderRadius: 'var(--radius-sm)'
            }}
            title="Sign out"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </header>
  );
};
