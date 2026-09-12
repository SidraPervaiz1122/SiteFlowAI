import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileSpreadsheet,
  ClipboardCheck,
  Search,
  CheckSquare,
  FileText,
  FolderArchive,
  Bot,
  History,
  Building2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const Sidebar: React.FC = () => {
  const { role } = useAuth();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <Building2 color="#38bdf8" size={24} />
        <div>
          Site<span>Flow</span> <span style={{ fontSize: '0.65rem', color: '#c084fc', border: '1px solid rgba(192, 132, 252, 0.3)', padding: '1px 5px', borderRadius: '4px' }}>AI</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <LayoutDashboard />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/boq" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <FileSpreadsheet />
          <span>BOQ Master</span>
        </NavLink>

        <NavLink to="/check-requests" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <ClipboardCheck />
          <span>Check Requests</span>
        </NavLink>

        <NavLink to="/inspections" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Search />
          <span>Inspections</span>
        </NavLink>

        <NavLink to="/approvals" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <CheckSquare />
          <span>Approvals</span>
        </NavLink>

        <NavLink to="/ipc" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <FileText />
          <span>IPC Certificates</span>
        </NavLink>

        <NavLink to="/documents" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <FolderArchive />
          <span>Documents</span>
        </NavLink>

        <NavLink to="/ai" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Bot />
          <span>AI Assistant</span>
        </NavLink>

        <NavLink to="/activity" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <History />
          <span>Audit Trail</span>
        </NavLink>
      </nav>

      {/* Role Footer Status */}
      <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border-color)', fontSize: '0.75rem' }}>
        <div style={{ color: 'var(--text-dim)', marginBottom: '4px' }}>Active Access Level</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600, color: '#fff' }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: role === 'CONTRACTOR' ? '#fbbf24' : (role === 'RE' ? '#38bdf8' : '#34d399') }}></span>
          {role}
        </div>
      </div>
    </aside>
  );
};
