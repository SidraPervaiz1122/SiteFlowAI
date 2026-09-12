import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { CheckRequest } from '../types';
import {
  ArrowLeft,
  Upload,
  Sparkles,
  ShieldCheck,
  Camera,
  CheckCircle,
  FileText,
  AlertCircle,
  HelpCircle,
  Clock,
  ArrowRight
} from 'lucide-react';

export const CheckRequestDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { role } = useAuth();
  const navigate = useNavigate();

  const [cr, setCr] = useState<CheckRequest | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [evidenceCaption, setEvidenceCaption] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Measured quantity submission (Contractor)
  const [actualQty, setActualQty] = useState('');
  const [contractorNotes, setContractorNotes] = useState('');
  const [qtySubmitting, setQtySubmitting] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState('');

  const loadCR = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const data = await api.getCheckRequestDetail(Number(id));
      setCr(data);
      if (data.proposed_qty && !actualQty) {
        setActualQty(String(data.proposed_qty));
      }
    } catch (e) {
      console.error('Failed to load check request:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCR();
  }, [id, role]);

  const handleUploadEvidence = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile || !cr) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      if (evidenceCaption) formData.append('caption', evidenceCaption);
      await api.uploadEvidence(cr.id, formData);
      setSelectedFile(null);
      setEvidenceCaption('');
      await loadCR();
    } catch (err: any) {
      alert(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleSubmitCR = async () => {
    if (!cr) return;
    setSubmitting(true);
    try {
      await api.submitCheckRequest(cr.id);
      await loadCR();
    } catch (err: any) {
      alert(err.message || 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  const handleSubmitQuantity = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cr) return;
    setQtySubmitting(true);
    setFeedbackMsg('');
    try {
      await api.submitQuantity({
        check_request_id: cr.id,
        submitted_qty: Number(actualQty),
        contractor_notes: contractorNotes
      });
      setFeedbackMsg('Actual quantity submitted successfully! Now pending RE quantity approval.');
      await loadCR();
    } catch (err: any) {
      alert(err.message || 'Quantity submission failed');
    } finally {
      setQtySubmitting(false);
    }
  };

  if (loading) return <div>Loading check request...</div>;
  if (!cr) return <div>Check Request not found</div>;

  const aiReview = cr.ai_reviews?.[0];
  const missingEvidences: string[] = aiReview?.missing_evidence ? JSON.parse(aiReview.missing_evidence) : [];
  const potentialIssues: string[] = aiReview?.potential_issues ? JSON.parse(aiReview.potential_issues) : [];
  const suggestedChecks: string[] = aiReview?.suggested_checks ? JSON.parse(aiReview.suggested_checks) : [];
  const recommendedQuestions: string[] = aiReview?.recommended_questions ? JSON.parse(aiReview.recommended_questions) : [];

  return (
    <div>
      <Link to="/check-requests" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: 'var(--primary)', textDecoration: 'none', marginBottom: '16px', fontSize: '0.85rem' }}>
        <ArrowLeft size={16} /> Back to Check Requests
      </Link>

      {/* Main Header Card */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 800, fontSize: '1.3rem', color: 'var(--primary)' }}>
                {cr.cr_number}
              </span>
              <span className={`status-pill ${
                cr.status.includes('ACCEPTED') || cr.status.includes('APPROVED') ? 'status-emerald' :
                cr.status.includes('REJECTED') ? 'status-rose' : 'status-amber'
              }`}>
                {cr.status}
              </span>
            </div>
            <h1 style={{ fontSize: '1.45rem', fontWeight: 700, marginTop: '6px' }}>{cr.title}</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem', marginTop: '4px' }}>
              BOQ Item #{cr.boq_item_id}: {cr.boq_item_description} ({cr.boq_item_category})
            </p>
          </div>

          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            {cr.status === 'DRAFT' && role === 'CONTRACTOR' && (
              <button className="btn btn-primary" onClick={handleSubmitCR} disabled={submitting}>
                <Sparkles size={16} /> Submit & Run AI Pre-Review
              </button>
            )}

            {(cr.status === 'PENDING_INSPECTION' || cr.status === 'INSPECTION_IN_PROGRESS') && role === 'RE' && (
              <button
                className="btn btn-primary"
                onClick={async () => {
                  const insp = await api.startInspection(cr.id);
                  navigate(`/inspections/${insp.id}`);
                }}
              >
                <ShieldCheck size={16} /> Open Inspection Workspace
              </button>
            )}
          </div>
        </div>

        <div className="metrics-grid" style={{ marginTop: '20px', marginBottom: '0' }}>
          <div className="metric-card">
            <span className="metric-label">Proposed Work Quantity</span>
            <span className="metric-value">{cr.proposed_qty} {cr.unit}</span>
            <span className="metric-subtext">Claimed execution batch</span>
          </div>

          <div className="metric-card">
            <span className="metric-label">Contract Unit Rate</span>
            <span className="metric-value">PKR {Number(cr.boq_item_rate_pkr).toLocaleString()}</span>
            <span className="metric-subtext">Contractual unit rate</span>
          </div>

          <div className="metric-card">
            <span className="metric-label">Batch Value</span>
            <span className="metric-value" style={{ color: '#38bdf8' }}>
              PKR {(Number(cr.proposed_qty) * Number(cr.boq_item_rate_pkr)).toLocaleString()}
            </span>
            <span className="metric-subtext">Estimated current value</span>
          </div>

          <div className="metric-card">
            <span className="metric-label">Created Timestamp</span>
            <span className="metric-value" style={{ fontSize: '1.05rem', color: 'var(--text-main)', marginTop: '8px' }}>
              {new Date(cr.created_at).toLocaleDateString()}
            </span>
            <span className="metric-subtext">{new Date(cr.created_at).toLocaleTimeString()}</span>
          </div>
        </div>
      </div>

      {feedbackMsg && (
        <div style={{
          background: 'rgba(16, 185, 129, 0.15)',
          border: '1px solid rgba(16, 185, 129, 0.4)',
          color: '#34d399',
          padding: '12px 18px',
          borderRadius: 'var(--radius-md)',
          fontSize: '0.86rem',
          marginBottom: '20px'
        }}>
          {feedbackMsg}
        </div>
      )}

      {/* Grid: AI Pre-Review & Evidence Gallery */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '24px', marginBottom: '24px' }}>
        {/* AI Advisory Pre-Review Card */}
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h2 className="card-title">AI Advisory Pre-Review</h2>
              <span className="ai-badge">Advisory Only</span>
            </div>
          </div>

          {!aiReview ? (
            <div style={{ textAlign: 'center', padding: '36px 20px', color: 'var(--text-dim)' }}>
              <Sparkles size={28} style={{ opacity: 0.5, marginBottom: '8px' }} />
              <div>AI Pre-Review triggers automatically upon submission by the Contractor.</div>
            </div>
          ) : (
            <div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '12px 16px',
                background: aiReview.readiness === 'Ready' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                border: `1px solid ${aiReview.readiness === 'Ready' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`,
                borderRadius: 'var(--radius-md)',
                marginBottom: '16px'
              }}>
                <div>
                  <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Inspection Readiness</div>
                  <div style={{ fontSize: '1.15rem', fontWeight: 700, color: aiReview.readiness === 'Ready' ? '#34d399' : '#fbbf24' }}>
                    {aiReview.readiness}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Confidence Score</div>
                  <div style={{ fontSize: '1.15rem', fontWeight: 700, color: '#38bdf8' }}>{aiReview.confidence_score}%</div>
                </div>
              </div>

              {missingEvidences.length > 0 && (
                <div style={{ marginBottom: '14px' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 600, color: '#fb7185', display: 'flex', alignItems: 'center', gap: '5px', marginBottom: '6px' }}>
                    <AlertCircle size={14} /> Missing Documentation / Evidence
                  </div>
                  <ul style={{ paddingLeft: '20px', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {missingEvidences.map((m, idx) => (
                      <li key={idx} style={{ marginBottom: '3px' }}>{m}</li>
                    ))}
                  </ul>
                </div>
              )}

              {suggestedChecks.length > 0 && (
                <div style={{ marginBottom: '14px' }}>
                  <div style={{ fontSize: '0.78rem', fontWeight: 600, color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '5px', marginBottom: '6px' }}>
                    <CheckCircle size={14} /> Suggested Engineering Checks for RE
                  </div>
                  <ul style={{ paddingLeft: '20px', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {suggestedChecks.map((c, idx) => (
                      <li key={idx} style={{ marginBottom: '3px' }}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}

              {recommendedQuestions.length > 0 && (
                <div>
                  <div style={{ fontSize: '0.78rem', fontWeight: 600, color: '#c084fc', display: 'flex', alignItems: 'center', gap: '5px', marginBottom: '6px' }}>
                    <HelpCircle size={14} /> Recommended Verification Inquiries
                  </div>
                  <ul style={{ paddingLeft: '20px', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {recommendedQuestions.map((q, idx) => (
                      <li key={idx} style={{ marginBottom: '3px' }}>{q}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Evidence & Attachment Card */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Inspection Evidence & Photos</h2>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-dim)' }}>
              {cr.evidences?.length || 0} attachment(s)
            </span>
          </div>

          {/* Upload Form for Contractor/RE */}
          <form onSubmit={handleUploadEvidence} style={{ marginBottom: '20px', padding: '14px', background: '#131c2e', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <div>
                <label className="form-label" style={{ marginBottom: '4px' }}>Attach Photo / Test Report</label>
                <input
                  type="file"
                  className="form-input"
                  style={{ padding: '6px' }}
                  onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                  required
                />
              </div>
              <div style={{ display: 'flex', gap: '10px' }}>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Caption (e.g. Mortar joint alignment photo)"
                  style={{ flex: 1 }}
                  value={evidenceCaption}
                  onChange={(e) => setEvidenceCaption(e.target.value)}
                />
                <button type="submit" className="btn btn-secondary btn-sm" disabled={uploading || !selectedFile}>
                  <Upload size={14} /> Upload
                </button>
              </div>
            </div>
          </form>

          {/* Evidence List */}
          {(!cr.evidences || cr.evidences.length === 0) ? (
            <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-dim)', fontSize: '0.85rem' }}>
              No evidence files attached yet.
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))', gap: '12px' }}>
              {cr.evidences.map((ev) => (
                <div
                  key={ev.id}
                  style={{
                    background: '#1a2436',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    padding: '10px',
                    textAlign: 'center'
                  }}
                >
                  <Camera size={24} color="#38bdf8" style={{ marginBottom: '6px' }} />
                  <div style={{ fontSize: '0.75rem', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {ev.filename}
                  </div>
                  {ev.caption && (
                    <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)', marginTop: '2px' }}>{ev.caption}</div>
                  )}
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                    {new Date(ev.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Actual Measured Quantity Submission (Only available when INSPECTION_ACCEPTED) */}
      {cr.status === 'INSPECTION_ACCEPTED' && (
        <div className="card" style={{ border: '1px solid #10b981', background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(15, 23, 42, 0.95))' }}>
          <div className="card-header">
            <div>
              <h2 className="card-title" style={{ color: '#34d399', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle size={20} /> Inspection Accepted by RE — Submit Measured Quantity
              </h2>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                Site inspection passed. Contractor must now submit the authoritative measured quantity for RE quantity certification.
              </p>
            </div>
          </div>

          {role === 'CONTRACTOR' ? (
            <form onSubmit={handleSubmitQuantity}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '16px' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Actual In-Place Measured Quantity ({cr.unit})</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-input"
                    value={actualQty}
                    onChange={(e) => setActualQty(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Contractor Measurement Notes</label>
                  <input
                    type="text"
                    className="form-input"
                    placeholder="e.g. Measured jointly on site with site engineer"
                    value={contractorNotes}
                    onChange={(e) => setContractorNotes(e.target.value)}
                  />
                </div>
              </div>

              <button type="submit" className="btn btn-success" disabled={qtySubmitting}>
                Submit Measured Quantity for RE Approval
              </button>
            </form>
          ) : (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              Awaiting Contractor to submit final measured actual quantity.
            </div>
          )}
        </div>
      )}
    </div>
  );
};
