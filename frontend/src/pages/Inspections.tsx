import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { CheckRequest } from '../types';
import { Search, ShieldCheck, ArrowRight, Clock, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const Inspections: React.FC = () => {
  const { role } = useAuth();
  const [crs, setCrs] = useState<CheckRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInspections();
  }, []);

  const loadInspections = async () => {
    try {
      setLoading(true);
      const data = await api.getCheckRequests();
      setCrs(data);
    } catch (e) {
      console.error('Failed to load inspections:', e);
    } finally {
      setLoading(false);
    }
  };

  const pendingInspections = crs.filter((cr) =>
    ['SUBMITTED', 'PENDING_INSPECTION', 'INSPECTION_IN_PROGRESS'].includes(cr.status)
  );
  const completedInspections = crs.filter((cr) =>
    ['INSPECTION_ACCEPTED', 'INSPECTION_REJECTED', 'QUANTITY_SUBMITTED', 'RE_APPROVED', 'CLIENT_APPROVED', 'IPC_INCLUDED'].includes(cr.status)
  );

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Resident Engineer Inspection Workspace</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
          Physical site inspections, checklist verification, AI observation drafting & formal decisions
        </p>
      </div>

      <div style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Clock size={18} color="#fbbf24" /> Pending Site Inspections ({pendingInspections.length})
        </h2>

        <div className="table-wrapper">
          <table className="siteflow-table">
            <thead>
              <tr>
                <th style={{ width: '100px' }}>CR #</th>
                <th>Work Description</th>
                <th>BOQ Item</th>
                <th style={{ textAlign: 'right' }}>Proposed Qty</th>
                <th>AI Readiness</th>
                <th>Status</th>
                <th style={{ width: '140px' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {pendingInspections.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-dim)' }}>
                    No pending site inspections awaiting review.
                  </td>
                </tr>
              ) : (
                pendingInspections.map((cr) => {
                  const aiReview = cr.ai_reviews?.[0];
                  return (
                    <tr key={cr.id}>
                      <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--primary)' }}>
                        {cr.cr_number}
                      </td>
                      <td style={{ fontWeight: 600 }}>{cr.title}</td>
                      <td>#{cr.boq_item_id} - {cr.boq_item_description}</td>
                      <td style={{ textAlign: 'right' }} className="currency-cell">
                        {cr.proposed_qty} {cr.unit}
                      </td>
                      <td>
                        {aiReview ? (
                          <span className={`status-pill ${aiReview.readiness === 'Ready' ? 'status-emerald' : 'status-amber'}`}>
                            {aiReview.readiness} ({aiReview.confidence_score}%)
                          </span>
                        ) : (
                          <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem' }}>Pending</span>
                        )}
                      </td>
                      <td>
                        <span className="status-pill status-amber">{cr.status}</span>
                      </td>
                      <td>
                        {role === 'RE' ? (
                          <button
                            onClick={async () => {
                              const insp = await api.startInspection(cr.id);
                              window.location.href = `/inspections/${insp.id}`;
                            }}
                            className="btn btn-primary btn-sm"
                          >
                            <ShieldCheck size={14} /> Conduct
                          </button>
                        ) : (
                          <Link to={`/check-requests/${cr.id}`} className="btn btn-secondary btn-sm">
                            View
                          </Link>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={18} color="#34d399" /> Completed Inspections ({completedInspections.length})
        </h2>

        <div className="table-wrapper">
          <table className="siteflow-table">
            <thead>
              <tr>
                <th style={{ width: '100px' }}>CR #</th>
                <th>Work Description</th>
                <th>BOQ Item</th>
                <th style={{ textAlign: 'right' }}>Proposed Qty</th>
                <th>Decision / Status</th>
                <th style={{ width: '100px' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {completedInspections.map((cr) => (
                <tr key={cr.id}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--primary)' }}>
                    {cr.cr_number}
                  </td>
                  <td>{cr.title}</td>
                  <td>#{cr.boq_item_id} - {cr.boq_item_description}</td>
                  <td style={{ textAlign: 'right' }} className="currency-cell">{cr.proposed_qty} {cr.unit}</td>
                  <td>
                    <span className={`status-pill ${
                      cr.status.includes('ACCEPTED') || cr.status.includes('APPROVED') ? 'status-emerald' : 'status-rose'
                    }`}>
                      {cr.status}
                    </span>
                  </td>
                  <td>
                    <Link to={`/check-requests/${cr.id}`} className="btn btn-secondary btn-sm">
                      Details <ArrowRight size={12} />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
