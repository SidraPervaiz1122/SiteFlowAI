import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import { ProjectSummary, CheckRequest, AuditLog } from '../types';
import { Link } from 'react-router-dom';
import {
  TrendingUp,
  DollarSign,
  ClipboardList,
  CheckCircle,
  AlertTriangle,
  FileCheck,
  ArrowRight,
  ShieldCheck,
  Building,
  Clock,
  Sparkles
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { user, role } = useAuth();
  const [summary, setSummary] = useState<ProjectSummary | null>(null);
  const [recentCrs, setRecentCrs] = useState<CheckRequest[]>([]);
  const [recentAudit, setRecentAudit] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [sumData, crsData, auditData] = await Promise.all([
        api.getProgressSummary(),
        api.getCheckRequests(),
        api.getAuditTrail(undefined, undefined)
      ]);
      setSummary(sumData);
      setRecentCrs(crsData.slice(0, 5));
      setRecentAudit(auditData.slice(0, 6));
    } catch (e) {
      console.error('Failed to load dashboard data:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, [role]);

  const formatPKR = (val?: string | number) => {
    if (!val) return 'PKR 0.00';
    const num = Number(val);
    return `PKR ${num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  return (
    <div>
      {/* Top Banner Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>
            {role === 'CONTRACTOR' && 'Contractor Operations Hub'}
            {role === 'RE' && 'Resident Engineer Control Center'}
            {role === 'CLIENT' && 'Project Executive Overview'}
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
            5 Marla Model Residence (750 sq.ft. covered area) — Deterministic Quality & Financial Control
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          {role === 'CONTRACTOR' && (
            <Link to="/check-requests" className="btn btn-primary">
              <ClipboardList size={16} /> Create Check Request
            </Link>
          )}
          {role === 'RE' && (
            <Link to="/inspections" className="btn btn-primary">
              <ShieldCheck size={16} /> Inspect Pending Work
            </Link>
          )}
          {role === 'CLIENT' && (
            <Link to="/ipc" className="btn btn-primary">
              <FileCheck size={16} /> Review IPC Certificates
            </Link>
          )}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <span className="metric-label">Contract BOQ Total</span>
          <span className="metric-value">{formatPKR(summary?.contract_value_pkr)}</span>
          <span className="metric-subtext">Immutable Tender Baseline (24 Items)</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Approved Work Value</span>
          <span className="metric-value" style={{ color: '#34d399' }}>
            {formatPKR(summary?.approved_value_pkr)}
          </span>
          <span className="metric-subtext">{summary?.financial_progress_pct}% of total contract</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Remaining Balance</span>
          <span className="metric-value" style={{ color: '#38bdf8' }}>
            {formatPKR(summary?.remaining_value_pkr)}
          </span>
          <span className="metric-subtext">Uncertified Contract Volume</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Active IPC Certified</span>
          <span className="metric-value" style={{ color: '#fbbf24' }}>
            {formatPKR(summary?.ipc_cumulative_value_pkr)}
          </span>
          <span className="metric-subtext">Authoritative Payment Certificates</span>
        </div>
      </div>

      {/* Role Action Cards Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9))',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '20px 24px',
        marginBottom: '28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '20px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(56, 189, 248, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Sparkles color="#38bdf8" size={24} />
          </div>
          <div>
            <div style={{ fontWeight: 600, fontSize: '0.98rem', color: '#fff' }}>
              {role === 'CONTRACTOR' && 'Inspection Readiness & Advisory AI Active'}
              {role === 'RE' && 'AI-Assisted Defect Observation & Quantity Validation'}
              {role === 'CLIENT' && 'Independent Payment Certification & Audit Protocol'}
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
              {role === 'CONTRACTOR' && 'Attach evidence to Check Requests to trigger automated advisory pre-review.'}
              {role === 'RE' && 'Pending inspections: ' + (summary?.pending_inspections || 0) + ' | Pending approvals: ' + (summary?.pending_re_approvals || 0)}
              {role === 'CLIENT' && 'Pending client reviews: ' + (summary?.pending_client_approvals || 0) + ' | Ready for IPC: ' + (summary?.pending_client_approvals === 0 ? 'Up to date' : 'Action required')}
            </div>
          </div>
        </div>

        <Link to="/approvals" className="btn btn-secondary btn-sm">
          View Approvals Workspace <ArrowRight size={14} />
        </Link>
      </div>

      {/* Split Section: Recent Check Requests & Activity Audit */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '24px' }}>
        {/* Check Requests Column */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Recent Check Requests</h2>
            <Link to="/check-requests" style={{ fontSize: '0.82rem', color: 'var(--primary)', textDecoration: 'none' }}>
              View all
            </Link>
          </div>

          {recentCrs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '36px 0', color: 'var(--text-dim)' }}>
              No check requests created yet.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {recentCrs.map((cr) => (
                <Link
                  key={cr.id}
                  to={`/check-requests/${cr.id}`}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 16px',
                    background: '#131c2e',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    textDecoration: 'none',
                    color: 'inherit',
                    transition: 'background 0.15s ease'
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--primary)', fontSize: '0.85rem' }}>
                        {cr.cr_number}
                      </span>
                      <span style={{ fontWeight: 600, fontSize: '0.88rem' }}>{cr.title}</span>
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '2px' }}>
                      {cr.boq_item_category} • {cr.proposed_qty} {cr.unit}
                    </div>
                  </div>
                  <div>
                    <span className={`status-pill ${
                      cr.status.includes('ACCEPTED') || cr.status.includes('APPROVED') ? 'status-emerald' :
                      cr.status.includes('REJECTED') ? 'status-rose' : 'status-amber'
                    }`}>
                      {cr.status}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Audit Activity Column */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Live Audit Trail</h2>
            <Link to="/activity" style={{ fontSize: '0.82rem', color: 'var(--primary)', textDecoration: 'none' }}>
              Full timeline
            </Link>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {recentAudit.map((log) => (
              <div key={log.id} style={{ display: 'flex', gap: '12px', fontSize: '0.82rem' }}>
                <div style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: log.actor_role === 'CONTRACTOR' ? '#fbbf24' : (log.actor_role === 'RE' ? '#38bdf8' : '#34d399'),
                  marginTop: '6px',
                  flexShrink: 0
                }} />
                <div style={{ flex: 1 }}>
                  <div>
                    <strong style={{ color: '#fff' }}>{log.actor_name}</strong>
                    <span style={{ color: 'var(--text-dim)', marginLeft: '6px' }}>({log.actor_role})</span>
                  </div>
                  <div style={{ color: 'var(--text-muted)', marginTop: '1px' }}>
                    {log.action} on <code style={{ color: 'var(--primary)' }}>{log.entity_id}</code>
                  </div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '2px' }}>
                    {new Date(log.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
