import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { QuantityApproval } from '../types';
import { CheckSquare, ShieldCheck, UserCheck, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

export const Approvals: React.FC = () => {
  const { role } = useAuth();
  const [activeTab, setActiveTab] = useState<'RE_APPROVAL' | 'CLIENT_REVIEW'>(
    role === 'CLIENT' ? 'CLIENT_REVIEW' : 'RE_APPROVAL'
  );

  const [measurements, setMeasurements] = useState<any[]>([]);
  const [approvals, setApprovals] = useState<QuantityApproval[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [actionError, setActionError] = useState('');
  const [actionSuccess, setActionSuccess] = useState('');

  // RE approval form states
  const [selectedMeasurement, setSelectedMeasurement] = useState<any | null>(null);
  const [approvalQty, setApprovalQty] = useState('');
  const [reComments, setReComments] = useState('');
  const [quantityContext, setQuantityContext] = useState<any | null>(null);

  // Client review states
  const [selectedApproval, setSelectedApproval] = useState<QuantityApproval | null>(null);
  const [clientComments, setClientComments] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [measData, apprsData] = await Promise.all([
        api.getMeasurements(),
        api.getApprovals()
      ]);
      setMeasurements(measData);
      setApprovals(apprsData);
    } catch (e) {
      console.error('Failed to load approvals:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [role]);

  const handleSelectMeasurement = async (m: any) => {
    setSelectedMeasurement(m);
    setApprovalQty(String(m.submitted_qty));
    setActionError('');
    setActionSuccess('');
    try {
      const ctx = await api.getQuantityContext(m.boq_item_id, m.submitted_qty);
      setQuantityContext(ctx);
    } catch (e) {
      console.error('Failed to get context:', e);
    }
  };

  const handleProcessReApproval = async (statusDecision: 'APPROVED' | 'REJECTED') => {
    if (!selectedMeasurement) return;
    setSubmitting(true);
    setActionError('');
    setActionSuccess('');
    try {
      const res = await api.reApproveQuantity({
        quantity_measurement_id: selectedMeasurement.id,
        approved_qty: Number(approvalQty),
        status: statusDecision,
        re_comments: reComments || `Quantity ${statusDecision.toLowerCase()} by RE.`
      });
      setActionSuccess(`Quantity ${statusDecision.toLowerCase()} successfully! Amount: PKR ${Number(res.approved_amount_pkr).toLocaleString()}`);
      setSelectedMeasurement(null);
      await loadData();
    } catch (err: any) {
      setActionError(err.message || 'Approval failed');
    } finally {
      setSubmitting(false);
    }
  };

  const handleProcessClientReview = async (decision: 'APPROVED' | 'REJECTED') => {
    if (!selectedApproval) return;
    setSubmitting(true);
    setActionError('');
    setActionSuccess('');
    try {
      await api.submitClientReview({
        quantity_approval_id: selectedApproval.id,
        decision,
        comments: clientComments || `Client review ${decision.toLowerCase()}ed.`
      });
      setActionSuccess(`Client review recorded as ${decision}! Work is now certified for IPC.`);
      setSelectedApproval(null);
      await loadData();
    } catch (err: any) {
      setActionError(err.message || 'Client review failed');
    } finally {
      setSubmitting(false);
    }
  };

  const pendingMeasurements = measurements.filter((m) => m.status === 'SUBMITTED');
  const pendingClientReviews = approvals.filter((a) => a.client_review_status === 'PENDING' && a.status === 'APPROVED');

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Approvals & Certification Control</h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
          Deterministic 2-stage verification: Resident Engineer Quantity Approval ➔ Client Final Review
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '12px', borderBottom: '1px solid var(--border-color)', marginBottom: '24px' }}>
        <button
          onClick={() => { setActiveTab('RE_APPROVAL'); setActionError(''); setActionSuccess(''); }}
          style={{
            background: 'transparent',
            border: 'none',
            borderBottom: activeTab === 'RE_APPROVAL' ? '2px solid var(--primary)' : '2px solid transparent',
            color: activeTab === 'RE_APPROVAL' ? '#fff' : 'var(--text-muted)',
            padding: '10px 18px',
            fontSize: '0.92rem',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <ShieldCheck size={18} color="#38bdf8" />
          RE Quantity Approvals ({pendingMeasurements.length})
        </button>

        <button
          onClick={() => { setActiveTab('CLIENT_REVIEW'); setActionError(''); setActionSuccess(''); }}
          style={{
            background: 'transparent',
            border: 'none',
            borderBottom: activeTab === 'CLIENT_REVIEW' ? '2px solid var(--accent-emerald)' : '2px solid transparent',
            color: activeTab === 'CLIENT_REVIEW' ? '#fff' : 'var(--text-muted)',
            padding: '10px 18px',
            fontSize: '0.92rem',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <UserCheck size={18} color="#34d399" />
          Client Final Reviews ({pendingClientReviews.length})
        </button>
      </div>

      {actionError && (
        <div style={{
          background: 'var(--accent-rose-bg)',
          border: '1px solid rgba(244, 63, 94, 0.4)',
          color: '#fb7185',
          padding: '12px 18px',
          borderRadius: 'var(--radius-md)',
          fontSize: '0.86rem',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <AlertTriangle size={18} />
          {actionError}
        </div>
      )}

      {actionSuccess && (
        <div style={{
          background: 'rgba(16, 185, 129, 0.15)',
          border: '1px solid rgba(16, 185, 129, 0.4)',
          color: '#34d399',
          padding: '12px 18px',
          borderRadius: 'var(--radius-md)',
          fontSize: '0.86rem',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <CheckCircle size={18} />
          {actionSuccess}
        </div>
      )}

      {/* TAB 1: RE QUANTITY APPROVALS */}
      {activeTab === 'RE_APPROVAL' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: selectedMeasurement ? '1.2fr 1fr' : '1fr', gap: '24px' }}>
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '14px' }}>
                Pending Contractor Measurements Awaiting RE Certification
              </h2>

              <div className="table-wrapper">
                <table className="siteflow-table">
                  <thead>
                    <tr>
                      <th>Measurement #</th>
                      <th>Check Request</th>
                      <th>BOQ Item</th>
                      <th style={{ textAlign: 'right' }}>Submitted Qty</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pendingMeasurements.length === 0 ? (
                      <tr>
                        <td colSpan={6} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-dim)' }}>
                          No contractor quantity measurements pending RE approval.
                        </td>
                      </tr>
                    ) : (
                      pendingMeasurements.map((m) => (
                        <tr key={m.id} style={{ background: selectedMeasurement?.id === m.id ? 'var(--bg-card-hover)' : undefined }}>
                          <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>MEAS-{m.id}</td>
                          <td>CR #{m.check_request_id}</td>
                          <td>BOQ Item #{m.boq_item_id}</td>
                          <td style={{ textAlign: 'right', fontWeight: 600 }} className="currency-cell">
                            {m.submitted_qty}
                          </td>
                          <td><span className="status-pill status-amber">{m.status}</span></td>
                          <td>
                            <button
                              className="btn btn-secondary btn-sm"
                              onClick={() => handleSelectMeasurement(m)}
                              disabled={role !== 'RE'}
                            >
                              Review & Certify
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* RE Approval Action Panel */}
            {selectedMeasurement && (
              <div className="card" style={{ border: '1px solid var(--border-color)', height: 'fit-content' }}>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '14px' }}>
                  RE Quantity Certification (MEAS-{selectedMeasurement.id})
                </h3>

                {quantityContext && (
                  <div style={{
                    background: '#131c2e',
                    padding: '14px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-color)',
                    marginBottom: '16px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                    fontSize: '0.82rem'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-dim)' }}>Contract Total Qty:</span>
                      <strong>{quantityContext.contract_qty}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-dim)' }}>Previously Approved:</span>
                      <strong style={{ color: '#34d399' }}>{quantityContext.previously_approved_qty}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-dim)' }}>Remaining Contract Qty:</span>
                      <strong style={{ color: '#38bdf8' }}>{quantityContext.remaining_qty}</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-dim)' }}>Contract Unit Rate:</span>
                      <strong>PKR {Number(quantityContext.contract_rate_pkr).toLocaleString()}</strong>
                    </div>
                  </div>
                )}

                <div className="form-group">
                  <label className="form-label">Approved Quantity</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-input"
                    value={approvalQty}
                    onChange={(e) => setApprovalQty(e.target.value)}
                    required
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                    Authoritative rule: Cannot exceed remaining contract volume.
                  </span>
                </div>

                <div className="form-group">
                  <label className="form-label">RE Endorsement / Comments</label>
                  <textarea
                    className="form-textarea"
                    rows={2}
                    placeholder="e.g. Dimensions verified against structural drawings"
                    value={reComments}
                    onChange={(e) => setReComments(e.target.value)}
                  />
                </div>

                <div style={{ display: 'flex', gap: '10px', marginTop: '16px' }}>
                  <button
                    type="button"
                    className="btn btn-success"
                    style={{ flex: 1 }}
                    onClick={() => handleProcessReApproval('APPROVED')}
                    disabled={submitting || role !== 'RE'}
                  >
                    Approve Quantity
                  </button>
                  <button
                    type="button"
                    className="btn btn-danger"
                    style={{ flex: 1 }}
                    onClick={() => handleProcessReApproval('REJECTED')}
                    disabled={submitting || role !== 'RE'}
                  >
                    Reject
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: CLIENT FINAL REVIEWS */}
      {activeTab === 'CLIENT_REVIEW' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: selectedApproval ? '1.2fr 1fr' : '1fr', gap: '24px' }}>
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '14px' }}>
                RE-Certified Work Awaiting Client Sign-Off (IPC Unlock)
              </h2>

              <div className="table-wrapper">
                <table className="siteflow-table">
                  <thead>
                    <tr>
                      <th>Approval #</th>
                      <th>CR #</th>
                      <th>BOQ Item</th>
                      <th style={{ textAlign: 'right' }}>Certified Qty</th>
                      <th style={{ textAlign: 'right' }}>Rate (PKR)</th>
                      <th style={{ textAlign: 'right' }}>Amount (PKR)</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {pendingClientReviews.length === 0 ? (
                      <tr>
                        <td colSpan={8} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-dim)' }}>
                          No pending items awaiting Client sign-off.
                        </td>
                      </tr>
                    ) : (
                      pendingClientReviews.map((appr) => (
                        <tr key={appr.id} style={{ background: selectedApproval?.id === appr.id ? 'var(--bg-card-hover)' : undefined }}>
                          <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>APPR-{appr.id}</td>
                          <td>{appr.cr_number}</td>
                          <td>{appr.boq_item_description}</td>
                          <td style={{ textAlign: 'right' }} className="currency-cell">{appr.approved_qty}</td>
                          <td style={{ textAlign: 'right' }} className="currency-cell">{Number(appr.contract_rate_pkr).toLocaleString()}</td>
                          <td style={{ textAlign: 'right', fontWeight: 600, color: '#34d399' }} className="currency-cell">
                            {Number(appr.approved_amount_pkr).toLocaleString()}
                          </td>
                          <td><span className="status-pill status-amber">PENDING CLIENT</span></td>
                          <td>
                            <button
                              className="btn btn-secondary btn-sm"
                              onClick={() => setSelectedApproval(appr)}
                              disabled={role !== 'CLIENT'}
                            >
                              Review
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Client Approval Action Panel */}
            {selectedApproval && (
              <div className="card" style={{ border: '1px solid var(--border-color)', height: 'fit-content' }}>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '14px' }}>
                  Client Executive Approval (APPR-{selectedApproval.id})
                </h3>

                <div style={{
                  background: '#131c2e',
                  padding: '14px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-color)',
                  marginBottom: '16px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px',
                  fontSize: '0.82rem'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Check Request:</span>
                    <strong>{selectedApproval.cr_number}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Certified Quantity:</span>
                    <strong>{selectedApproval.approved_qty} {selectedApproval.boq_item_unit}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Contract Unit Rate:</span>
                    <strong>PKR {Number(selectedApproval.contract_rate_pkr).toLocaleString()}</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-dim)' }}>Calculated Amount:</span>
                    <strong style={{ color: '#34d399', fontSize: '0.95rem' }}>
                      PKR {Number(selectedApproval.approved_amount_pkr).toLocaleString()}
                    </strong>
                  </div>
                  {selectedApproval.re_comments && (
                    <div style={{ marginTop: '4px', paddingTop: '6px', borderTop: '1px solid var(--border-color)' }}>
                      <span style={{ color: 'var(--text-dim)' }}>RE Endorsement:</span>
                      <div style={{ color: 'var(--text-muted)' }}>{selectedApproval.re_comments}</div>
                    </div>
                  )}
                </div>

                <div className="form-group">
                  <label className="form-label">Client Certification Remarks</label>
                  <textarea
                    className="form-textarea"
                    rows={2}
                    placeholder="e.g. Checked site photographs and approved for IPC inclusion."
                    value={clientComments}
                    onChange={(e) => setClientComments(e.target.value)}
                  />
                </div>

                <div style={{ display: 'flex', gap: '10px', marginTop: '16px' }}>
                  <button
                    type="button"
                    className="btn btn-success"
                    style={{ flex: 1 }}
                    onClick={() => handleProcessClientReview('APPROVED')}
                    disabled={submitting || role !== 'CLIENT'}
                  >
                    Approve for IPC
                  </button>
                  <button
                    type="button"
                    className="btn btn-danger"
                    style={{ flex: 1 }}
                    onClick={() => handleProcessClientReview('REJECTED')}
                    disabled={submitting || role !== 'CLIENT'}
                  >
                    Reject
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
