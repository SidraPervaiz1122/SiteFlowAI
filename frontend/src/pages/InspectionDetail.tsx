import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { Inspection, CheckRequest, Observation } from '../types';
import {
  ArrowLeft,
  ShieldCheck,
  Sparkles,
  CheckCircle,
  XCircle,
  Plus,
  AlertTriangle,
  FileText,
  Camera
} from 'lucide-react';

export const InspectionDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { role } = useAuth();
  const navigate = useNavigate();

  const [inspection, setInspection] = useState<Inspection | null>(null);
  const [cr, setCr] = useState<CheckRequest | null>(null);
  const [loading, setLoading] = useState(true);

  // Checklist states
  const [checklist, setChecklist] = useState({
    materials: true,
    dimensions: true,
    workmanship: true,
    safety: true
  });

  // AI Observation Drafting states
  const [obsHint, setObsHint] = useState('');
  const [aiDraft, setAiDraft] = useState<any | null>(null);
  const [draftingAi, setDraftingAi] = useState(false);

  // Manual observation form
  const [obsTitle, setObsTitle] = useState('');
  const [obsDesc, setObsDesc] = useState('');
  const [obsSeverity, setObsSeverity] = useState<'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'>('LOW');
  const [obsCategory, setObsCategory] = useState('QUALITY');
  const [obsAction, setObsAction] = useState('');

  // Decision state
  const [inspectorNotes, setInspectorNotes] = useState('');
  const [deciding, setDeciding] = useState(false);

  const loadData = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const insp = await api.getInspection(Number(id));
      setInspection(insp);
      const checkReq = await api.getCheckRequestDetail(insp.check_request_id);
      setCr(checkReq);
    } catch (e) {
      console.error('Failed to load inspection:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  const handleGenerateAiDraft = async () => {
    if (!inspection) return;
    setDraftingAi(true);
    try {
      const res = await api.generateAiObservation(inspection.id, obsHint);
      setAiDraft(res);
      setObsTitle(res.title);
      setObsDesc(res.description);
      setObsSeverity(res.severity as any);
      setObsCategory(res.category);
      setObsAction(res.recommended_action || '');
    } catch (e: any) {
      alert(e.message || 'Failed to draft AI observation');
    } finally {
      setDraftingAi(false);
    }
  };

  const handleAddObservation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inspection) return;
    try {
      await api.createObservation(inspection.id, {
        title: obsTitle,
        description: obsDesc,
        severity: obsSeverity,
        category: obsCategory,
        corrective_action: obsAction,
        is_ai_generated: !!aiDraft
      });
      setObsTitle('');
      setObsDesc('');
      setObsAction('');
      setAiDraft(null);
      await loadData();
    } catch (e: any) {
      alert(e.message || 'Failed to add observation');
    }
  };

  const handleMakeDecision = async (decision: 'ACCEPT' | 'REJECT') => {
    if (!inspection) return;
    setDeciding(true);
    try {
      await api.decideInspection(inspection.id, {
        decision,
        inspector_notes: inspectorNotes || `Inspection ${decision.toLowerCase()}ed by Resident Engineer.`,
        checklist_results: JSON.stringify(checklist)
      });
      navigate(`/check-requests/${inspection.check_request_id}`);
    } catch (e: any) {
      alert(e.message || 'Decision failed');
    } finally {
      setDeciding(false);
    }
  };

  if (loading) return <div>Loading inspection workspace...</div>;
  if (!inspection || !cr) return <div>Inspection not found</div>;

  return (
    <div>
      <Link to="/inspections" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: 'var(--primary)', textDecoration: 'none', marginBottom: '16px', fontSize: '0.85rem' }}>
        <ArrowLeft size={16} /> Back to Inspections List
      </Link>

      {/* Header Info */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 800, fontSize: '1.25rem', color: 'var(--primary)' }}>
                {cr.cr_number}
              </span>
              <span className="status-pill status-amber">{cr.status}</span>
            </div>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '4px' }}>{cr.title}</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
              BOQ Item #{cr.boq_item_id}: {cr.boq_item_description} • Proposed: {cr.proposed_qty} {cr.unit}
            </p>
          </div>

          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Inspection ID</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#fff' }}>INSP-{inspection.id}</div>
          </div>
        </div>
      </div>

      {/* Split Layout: Checklist/Observations vs AI Draft & Decision */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '24px' }}>
        {/* Left Column: Checklist & Evidence */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Inspection Verification Checklist */}
          <div className="card">
            <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={18} color="var(--primary)" /> Engineering Verification Checklist
            </h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '14px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={checklist.materials}
                  onChange={(e) => setChecklist({ ...checklist, materials: e.target.checked })}
                  style={{ width: '16px', height: '16px' }}
                />
                <span>Material specifications & test certificates verified on site</span>
              </label>

              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={checklist.dimensions}
                  onChange={(e) => setChecklist({ ...checklist, dimensions: e.target.checked })}
                  style={{ width: '16px', height: '16px' }}
                />
                <span>Dimensional accuracy, line, level and plumb checked against drawings</span>
              </label>

              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={checklist.workmanship}
                  onChange={(e) => setChecklist({ ...checklist, workmanship: e.target.checked })}
                  style={{ width: '16px', height: '16px' }}
                />
                <span>Workmanship standards and jointing/mortar/curing compliance</span>
              </label>

              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={checklist.safety}
                  onChange={(e) => setChecklist({ ...checklist, safety: e.target.checked })}
                  style={{ width: '16px', height: '16px' }}
                />
                <span>Site safety, scaffold stability & PPE adherence confirmed</span>
              </label>
            </div>
          </div>

          {/* Attached Evidence Preview */}
          <div className="card">
            <h2 className="card-title">Attached Site Photographs ({cr.evidences?.length || 0})</h2>
            {(!cr.evidences || cr.evidences.length === 0) ? (
              <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-dim)', fontSize: '0.85rem' }}>
                No contractor evidence photos attached.
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))', gap: '12px', marginTop: '12px' }}>
                {cr.evidences.map((ev) => (
                  <div key={ev.id} style={{ background: '#1a2436', padding: '10px', borderRadius: 'var(--radius-md)', textAlign: 'center', border: '1px solid var(--border-color)' }}>
                    <Camera size={22} color="#38bdf8" style={{ marginBottom: '4px' }} />
                    <div style={{ fontSize: '0.74rem', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {ev.filename}
                    </div>
                    {ev.caption && (
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)' }}>{ev.caption}</div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: AI Observation Drafting & Decision */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* AI Observation Drafter */}
          <div className="card">
            <div className="card-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 className="card-title">AI Observation Assistant</h2>
                <span className="ai-badge">Advisory Drafter</span>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px', marginBottom: '16px' }}>
              <input
                type="text"
                className="form-input"
                placeholder="Optional defect hint (e.g. mortar joints, honeycomb, curing)..."
                value={obsHint}
                onChange={(e) => setObsHint(e.target.value)}
                style={{ flex: 1 }}
              />
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={handleGenerateAiDraft}
                disabled={draftingAi}
              >
                <Sparkles size={14} color="#c084fc" />
                {draftingAi ? 'Drafting...' : 'Generate Draft'}
              </button>
            </div>

            {/* Form for RE to Review / Edit / Add Observation */}
            <form onSubmit={handleAddObservation}>
              <div className="form-group">
                <label className="form-label">Observation Title</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Mortar joint thickness deviation"
                  value={obsTitle}
                  onChange={(e) => setObsTitle(e.target.value)}
                  required
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div className="form-group">
                  <label className="form-label">Severity</label>
                  <select
                    className="form-select"
                    value={obsSeverity}
                    onChange={(e) => setObsSeverity(e.target.value as any)}
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="CRITICAL">CRITICAL</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Category</label>
                  <select
                    className="form-select"
                    value={obsCategory}
                    onChange={(e) => setObsCategory(e.target.value)}
                  >
                    <option value="QUALITY">QUALITY</option>
                    <option value="SAFETY">SAFETY</option>
                    <option value="SPECIFICATION">SPECIFICATION</option>
                    <option value="WORKMANSHIP">WORKMANSHIP</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Technical Observation Description</label>
                <textarea
                  className="form-textarea"
                  rows={2}
                  value={obsDesc}
                  onChange={(e) => setObsDesc(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Recommended Corrective Action</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Rake out fresh joints and ensure 10mm uniform thickness"
                  value={obsAction}
                  onChange={(e) => setObsAction(e.target.value)}
                />
              </div>

              <button type="submit" className="btn btn-secondary btn-sm" style={{ width: '100%' }}>
                <Plus size={14} /> Record Observation into Inspection Log
              </button>
            </form>
          </div>

          {/* Recorded Observations List */}
          {inspection.observations?.length > 0 && (
            <div className="card">
              <h2 className="card-title">Recorded Site Observations ({inspection.observations.length})</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '12px' }}>
                {inspection.observations.map((obs) => (
                  <div key={obs.id} style={{ background: '#131c2e', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-md)', padding: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.88rem', color: '#fff' }}>{obs.title}</span>
                      <span className={`status-pill ${obs.severity === 'CRITICAL' || obs.severity === 'HIGH' ? 'status-rose' : 'status-amber'}`}>
                        {obs.severity} • {obs.category}
                      </span>
                    </div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      {obs.description}
                    </div>
                    {obs.corrective_action && (
                      <div style={{ fontSize: '0.75rem', color: 'var(--primary)', marginTop: '6px' }}>
                        <strong>Corrective Action:</strong> {obs.corrective_action}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* RE Decision Card */}
          <div className="card" style={{ border: '1px solid var(--border-color)' }}>
            <h2 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={18} color="var(--primary)" /> Resident Engineer Formal Decision
            </h2>

            <div className="form-group" style={{ marginTop: '14px' }}>
              <label className="form-label">Official Inspector Remarks / Site Notes</label>
              <textarea
                className="form-textarea"
                rows={2}
                placeholder="Enter final remarks on structural alignment, curing, and tolerance..."
                value={inspectorNotes}
                onChange={(e) => setInspectorNotes(e.target.value)}
              />
            </div>

            <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
              <button
                type="button"
                className="btn btn-success"
                style={{ flex: 1 }}
                onClick={() => handleMakeDecision('ACCEPT')}
                disabled={deciding}
              >
                <CheckCircle size={16} /> Accept Inspection (Pass)
              </button>

              <button
                type="button"
                className="btn btn-danger"
                style={{ flex: 1 }}
                onClick={() => handleMakeDecision('REJECT')}
                disabled={deciding}
              >
                <XCircle size={16} /> Reject Inspection
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
