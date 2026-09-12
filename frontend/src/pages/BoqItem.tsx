import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api/client';
import { BoqItem } from '../types';
import { ArrowLeft, Lock, FileSpreadsheet } from 'lucide-react';

export const BoqItemDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<BoqItem | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      api.getBoqDetail(Number(id)).then(setItem).finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) return <div>Loading BOQ item details...</div>;
  if (!item) return <div>BOQ Item not found</div>;

  return (
    <div>
      <Link to="/boq" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: 'var(--primary)', textDecoration: 'none', marginBottom: '16px', fontSize: '0.85rem' }}>
        <ArrowLeft size={16} /> Back to BOQ Master
      </Link>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div>
            <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--primary)', fontWeight: 700 }}>
              ITEM #{item.item_number} • {item.category}
            </span>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '4px' }}>{item.description}</h1>
          </div>
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
            <Lock size={14} /> Immutable Contract Spec
          </div>
        </div>

        <div className="metrics-grid">
          <div className="metric-card">
            <span className="metric-label">Contract Quantity</span>
            <span className="metric-value">{item.contract_qty} {item.unit}</span>
            <span className="metric-subtext">Original tender allowance</span>
          </div>

          <div className="metric-card">
            <span className="metric-label">Contract Unit Rate</span>
            <span className="metric-value">PKR {Number(item.rate_pkr).toLocaleString()}</span>
            <span className="metric-subtext">Per {item.unit}</span>
          </div>

          <div className="metric-card">
            <span className="metric-label">Approved Quantity</span>
            <span className="metric-value" style={{ color: '#34d399' }}>{item.approved_qty} {item.unit}</span>
            <span className="metric-subtext">{item.progress_pct}% completed</span>
          </div>

          <div className="metric-card">
            <span className="metric-label">Remaining Balance</span>
            <span className="metric-value" style={{ color: '#38bdf8' }}>{item.remaining_qty} {item.unit}</span>
            <span className="metric-subtext">Available for future approvals</span>
          </div>
        </div>

        {item.remark && (
          <div style={{ background: '#131c2e', padding: '12px 16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', marginTop: '12px' }}>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Tender Notes & Remarks</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>{item.remark}</div>
          </div>
        )}
      </div>
    </div>
  );
};
