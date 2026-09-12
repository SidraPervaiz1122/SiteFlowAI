import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Ipc } from '../types';
import { FileText, Plus, CheckCircle, ArrowRight, DollarSign, Calendar, Lock } from 'lucide-react';

export const IpcPage: React.FC = () => {
  const { role } = useAuth();
  const [ipcs, setIpcs] = useState<Ipc[]>([]);
  const [eligibility, setEligibility] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // Form states
  const [periodStart, setPeriodStart] = useState('2026-09-01');
  const [periodEnd, setPeriodEnd] = useState('2026-09-30');
  const [notes, setNotes] = useState('');
  const [generating, setGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [ipcsData, eligData] = await Promise.all([
        api.getIpcs(),
        api.getIpcEligibility()
      ]);
      setIpcs(ipcsData);
      setEligibility(eligData);
    } catch (e) {
      console.error('Failed to load IPC data:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [role]);

  const handleGenerateIpc = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);
    setErrorMsg('');
    try {
      await api.generateIpc({
        period_start: periodStart,
        period_end: periodEnd,
        notes
      });
      setShowModal(false);
      await loadData();
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to generate IPC');
    } finally {
      setGenerating(false);
    }
  };

  const formatPKR = (val?: string | number) => {
    if (!val) return 'PKR 0.00';
    return `PKR ${Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Interim Payment Certificates (IPC)</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            Authoritative progress payment certificates derived strictly from Client-approved quantities
          </p>
        </div>

        {(role === 'RE' || role === 'CLIENT') && (
          <button
            className="btn btn-primary"
            onClick={() => setShowModal(true)}
            disabled={!eligibility || eligibility.eligible_items_count === 0}
          >
            <Plus size={16} /> Generate IPC
          </button>
        )}
      </div>

      {/* IPC Eligibility Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(15, 23, 42, 0.9))',
        border: '1px solid rgba(16, 185, 129, 0.3)',
        borderRadius: 'var(--radius-lg)',
        padding: '22px 26px',
        marginBottom: '28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '20px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(16, 185, 129, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <DollarSign color="#34d399" size={26} />
          </div>
          <div>
            <div style={{ fontSize: '0.78rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>
              Current IPC Eligibility Pool
            </div>
            <div style={{ fontSize: '1.45rem', fontWeight: 700, color: '#fff' }}>
              {formatPKR(eligibility?.total_eligible_amount_pkr)}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px' }}>
              {eligibility?.eligible_items_count || 0} item(s) fully certified by Client and ready for payment certificate.
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            background: 'rgba(56, 189, 248, 0.1)',
            border: '1px solid rgba(56, 189, 248, 0.3)',
            color: '#38bdf8',
            padding: '6px 14px',
            borderRadius: 'var(--radius-full)',
            fontSize: '0.78rem',
            fontWeight: 600
          }}>
            <Lock size={13} />
            Deterministic Rate × Qty
          </div>
        </div>
      </div>

      {/* Generated IPCs Table */}
      <div className="table-wrapper">
        <table className="siteflow-table">
          <thead>
            <tr>
              <th style={{ width: '110px' }}>Certificate #</th>
              <th>Billing Period</th>
              <th>Items Included</th>
              <th style={{ textAlign: 'right' }}>Current Period Amount</th>
              <th style={{ textAlign: 'right' }}>Cumulative Contract Amount</th>
              <th>Status</th>
              <th style={{ width: '100px' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {ipcs.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No IPC certificates generated yet.
                </td>
              </tr>
            ) : (
              ipcs.map((ipc) => (
                <tr key={ipc.id}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--primary)' }}>
                    {ipc.ipc_number}
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.84rem' }}>
                      <Calendar size={13} color="var(--text-dim)" />
                      {ipc.period_start} to {ipc.period_end}
                    </div>
                  </td>
                  <td>{ipc.items?.length || 0} BOQ item(s)</td>
                  <td style={{ textAlign: 'right', fontWeight: 600, color: '#34d399' }} className="currency-cell">
                    {formatPKR(ipc.total_current_amount_pkr)}
                  </td>
                  <td style={{ textAlign: 'right', fontWeight: 700, color: '#38bdf8' }} className="currency-cell">
                    {formatPKR(ipc.cumulative_amount_pkr)}
                  </td>
                  <td>
                    <span className="status-pill status-emerald">{ipc.status}</span>
                  </td>
                  <td>
                    <Link to={`/ipc/${ipc.id}`} className="btn btn-secondary btn-sm">
                      View Certificate <ArrowRight size={12} />
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Generate IPC Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '16px' }}>
              Issue Interim Payment Certificate
            </h2>

            {errorMsg && (
              <div style={{
                background: 'var(--accent-rose-bg)',
                border: '1px solid rgba(244, 63, 94, 0.4)',
                color: '#fb7185',
                padding: '10px',
                borderRadius: 'var(--radius-md)',
                fontSize: '0.82rem',
                marginBottom: '16px'
              }}>
                {errorMsg}
              </div>
            )}

            <div style={{
              background: '#131c2e',
              padding: '12px 16px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-color)',
              marginBottom: '16px',
              fontSize: '0.85rem'
            }}>
              <div style={{ color: 'var(--text-dim)' }}>Eligible Payment Volume:</div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#34d399', marginTop: '2px' }}>
                {formatPKR(eligibility?.total_eligible_amount_pkr)}
              </div>
              <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {eligibility?.eligible_items_count} Client-approved measurement items will be locked into this certificate.
              </div>
            </div>

            <form onSubmit={handleGenerateIpc}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="form-group">
                  <label className="form-label">Period Start Date</label>
                  <input
                    type="date"
                    className="form-input"
                    value={periodStart}
                    onChange={(e) => setPeriodStart(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Period End Date</label>
                  <input
                    type="date"
                    className="form-input"
                    value={periodEnd}
                    onChange={(e) => setPeriodEnd(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Certificate Notes / Billing Summary</label>
                <textarea
                  className="form-textarea"
                  rows={2}
                  placeholder="e.g. Interim certification for completed structural works and masonry"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={generating}>
                  {generating ? 'Certifying...' : 'Issue IPC'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
