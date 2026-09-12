import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { CheckRequest, BoqItem } from '../types';
import { Plus, Search, Filter, ClipboardCheck, ArrowRight, Camera, Sparkles } from 'lucide-react';

export const CheckRequests: React.FC = () => {
  const { role } = useAuth();
  const [crs, setCrs] = useState<CheckRequest[]>([]);
  const [boqItems, setBoqItems] = useState<BoqItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [statusFilter, setStatusFilter] = useState('ALL');

  // Form states
  const [selectedBoqId, setSelectedBoqId] = useState<number>(8); // Default to Item 8 (Masonry) for test!
  const [title, setTitle] = useState('');
  const [proposedQty, setProposedQty] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [crsData, boqData] = await Promise.all([
        api.getCheckRequests(),
        api.getBoqItems()
      ]);
      setCrs(crsData);
      setBoqItems(boqData);
    } catch (e) {
      console.error('Failed to load check requests:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateCR = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');
    setSubmitting(true);
    try {
      await api.createCheckRequest({
        boq_item_id: Number(selectedBoqId),
        title,
        proposed_qty: Number(proposedQty),
        description
      });
      setShowModal(false);
      setTitle('');
      setProposedQty('');
      setDescription('');
      loadData();
    } catch (err: any) {
      setFormError(err.message || 'Failed to create Check Request');
    } finally {
      setSubmitting(false);
    }
  };

  const filteredCrs = crs.filter((cr) => {
    if (statusFilter === 'ALL') return true;
    return cr.status === statusFilter;
  });

  const selectedBoq = boqItems.find((b) => b.id === Number(selectedBoqId));

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Check Requests (Inspection Calls)</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            Contractor raises inspection notices for completed construction batches
          </p>
        </div>

        {role === 'CONTRACTOR' && (
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            <Plus size={16} /> New Check Request
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '18px', overflowX: 'auto', paddingBottom: '4px' }}>
        {['ALL', 'DRAFT', 'PENDING_INSPECTION', 'INSPECTION_ACCEPTED', 'QUANTITY_SUBMITTED', 'RE_APPROVED', 'CLIENT_APPROVED'].map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className="btn btn-secondary btn-sm"
            style={{
              background: statusFilter === st ? 'rgba(56, 189, 248, 0.15)' : undefined,
              borderColor: statusFilter === st ? 'var(--primary)' : undefined,
              color: statusFilter === st ? 'var(--primary)' : undefined
            }}
          >
            {st.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Check Requests List */}
      <div className="table-wrapper">
        <table className="siteflow-table">
          <thead>
            <tr>
              <th style={{ width: '100px' }}>CR #</th>
              <th>Title / Description</th>
              <th>BOQ Item</th>
              <th style={{ textAlign: 'right' }}>Proposed Qty</th>
              <th>Attached Evidence</th>
              <th>AI Readiness</th>
              <th>Status</th>
              <th style={{ width: '80px' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredCrs.length === 0 ? (
              <tr>
                <td colSpan={8} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No check requests found matching this filter.
                </td>
              </tr>
            ) : (
              filteredCrs.map((cr) => {
                const aiReview = cr.ai_reviews?.[0];
                return (
                  <tr key={cr.id}>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--primary)' }}>
                      {cr.cr_number}
                    </td>
                    <td>
                      <div style={{ fontWeight: 600, color: '#fff' }}>{cr.title}</div>
                      {cr.description && (
                        <div style={{ fontSize: '0.74rem', color: 'var(--text-dim)' }}>{cr.description}</div>
                      )}
                    </td>
                    <td>
                      <div style={{ fontWeight: 500 }}>{cr.boq_item_description}</div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>{cr.boq_item_category}</div>
                    </td>
                    <td style={{ textAlign: 'right' }} className="currency-cell">
                      {cr.proposed_qty} {cr.unit}
                    </td>
                    <td>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '0.78rem', color: cr.evidences?.length > 0 ? '#34d399' : 'var(--text-dim)' }}>
                        <Camera size={13} />
                        {cr.evidences?.length || 0} file(s)
                      </span>
                    </td>
                    <td>
                      {aiReview ? (
                        <span className={`status-pill ${aiReview.readiness === 'Ready' ? 'status-emerald' : 'status-amber'}`}>
                          <Sparkles size={11} /> {aiReview.readiness} ({aiReview.confidence_score}%)
                        </span>
                      ) : (
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Pending submission</span>
                      )}
                    </td>
                    <td>
                      <span className={`status-pill ${
                        cr.status.includes('ACCEPTED') || cr.status.includes('APPROVED') ? 'status-emerald' :
                        cr.status.includes('REJECTED') ? 'status-rose' : 'status-amber'
                      }`}>
                        {cr.status}
                      </span>
                    </td>
                    <td>
                      <Link to={`/check-requests/${cr.id}`} className="btn btn-secondary btn-sm">
                        Open <ArrowRight size={12} />
                      </Link>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* New Check Request Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '16px' }}>Raise Check Request</h2>

            {formError && (
              <div style={{
                background: 'var(--accent-rose-bg)',
                border: '1px solid rgba(244, 63, 94, 0.4)',
                color: '#fb7185',
                padding: '10px',
                borderRadius: 'var(--radius-md)',
                fontSize: '0.82rem',
                marginBottom: '16px'
              }}>
                {formError}
              </div>
            )}

            <form onSubmit={handleCreateCR}>
              <div className="form-group">
                <label className="form-label">Target BOQ Item</label>
                <select
                  className="form-select"
                  value={selectedBoqId}
                  onChange={(e) => setSelectedBoqId(Number(e.target.value))}
                  required
                >
                  {boqItems.map((b) => (
                    <option key={b.id} value={b.id}>
                      #{b.item_number} - {b.category}: {b.description} ({b.contract_qty} {b.unit})
                    </option>
                  ))}
                </select>
              </div>

              {selectedBoq && (
                <div style={{
                  background: '#131c2e',
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-md)',
                  marginBottom: '16px',
                  fontSize: '0.78rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  border: '1px solid var(--border-color)'
                }}>
                  <span>Contract Qty: <strong>{selectedBoq.contract_qty} {selectedBoq.unit}</strong></span>
                  <span>Rate: <strong>PKR {Number(selectedBoq.rate_pkr).toLocaleString()}</strong></span>
                  <span>Remaining: <strong style={{ color: '#38bdf8' }}>{selectedBoq.remaining_qty} {selectedBoq.unit}</strong></span>
                </div>
              )}

              <div className="form-group">
                <label className="form-label">Check Request Title</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Ground Floor Brick Masonry Inspection"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Proposed Quantity for Inspection ({selectedBoq?.unit || 'Units'})</label>
                <input
                  type="number"
                  step="0.01"
                  className="form-input"
                  placeholder="e.g. 10.00"
                  value={proposedQty}
                  onChange={(e) => setProposedQty(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Contractor Site Notes / Location</label>
                <textarea
                  className="form-textarea"
                  rows={3}
                  placeholder="e.g. Masonry completed for northern external walls up to lintel level."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={submitting}>
                  Create Request
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
