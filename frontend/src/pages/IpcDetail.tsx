import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api/client';
import { Ipc } from '../types';
import { ArrowLeft, Printer, FileText, CheckCircle2, ShieldCheck, Building2 } from 'lucide-react';

export const IpcDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [ipc, setIpc] = useState<Ipc | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      api.getIpcDetail(Number(id)).then(setIpc).finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) return <div>Loading payment certificate...</div>;
  if (!ipc) return <div>Certificate not found</div>;

  const formatPKR = (val: string | number) => {
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };

  const CONTRACT_TOTAL = 5135535.00;
  const cumulativeNum = Number(ipc.cumulative_amount_pkr);
  const remainingContract = Math.max(0, CONTRACT_TOTAL - cumulativeNum);

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <Link to="/ipc" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', color: 'var(--primary)', textDecoration: 'none', fontSize: '0.85rem' }}>
          <ArrowLeft size={16} /> Back to IPC Certificates
        </Link>

        <button onClick={() => window.print()} className="btn btn-secondary btn-sm">
          <Printer size={14} /> Print Certificate
        </button>
      </div>

      {/* Official Certificate Paper Panel */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '36px',
        boxShadow: 'var(--shadow-lg)',
        maxWidth: '1000px',
        margin: '0 auto'
      }}>
        {/* Certificate Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '2px solid var(--border-color)', paddingBottom: '24px', marginBottom: '24px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Building2 size={28} color="#38bdf8" />
              <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>SiteFlow AI — Construction Interim Payment Certificate</div>
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.86rem', marginTop: '6px' }}>
              Project: <strong>SiteFlow 5 Marla Model Residence (SITEFLOW-5M)</strong>
            </div>
            <div style={{ color: 'var(--text-dim)', fontSize: '0.82rem' }}>
              Covered Area: 750 sq.ft. • Single Storey Residence
            </div>
          </div>

          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Certificate Number</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 800, color: 'var(--primary)' }}>
              {ipc.ipc_number}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              Issued: {new Date(ipc.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        {/* Certificate Metadata Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', background: '#131c2e', padding: '16px 20px', borderRadius: 'var(--radius-md)', marginBottom: '28px', border: '1px solid var(--border-color)' }}>
          <div>
            <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Billing Period</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#fff', marginTop: '2px' }}>
              {ipc.period_start} to {ipc.period_end}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Certification Status</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#34d399', marginTop: '2px' }}>
              {ipc.status} (Client Certified)
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-dim)', fontWeight: 600 }}>Contract Baseline Value</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem', color: '#fff', marginTop: '2px' }}>
              PKR {CONTRACT_TOTAL.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </div>
          </div>
        </div>

        {/* Certified Items Table */}
        <div style={{ marginBottom: '28px' }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '12px' }}>Certified Work Breakdown</h3>
          <div className="table-wrapper">
            <table className="siteflow-table">
              <thead>
                <tr>
                  <th style={{ width: '40px' }}>Item #</th>
                  <th>Category</th>
                  <th>Contract Description</th>
                  <th>Unit</th>
                  <th style={{ textAlign: 'right' }}>Certified Qty</th>
                  <th style={{ textAlign: 'right' }}>Contract Rate</th>
                  <th style={{ textAlign: 'right' }}>Amount (PKR)</th>
                </tr>
              </thead>
              <tbody>
                {ipc.items.map((item) => (
                  <tr key={item.id}>
                    <td style={{ fontWeight: 700, color: 'var(--primary)' }}>{item.item_number}</td>
                    <td style={{ fontWeight: 600 }}>{item.category}</td>
                    <td>{item.description}</td>
                    <td style={{ color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>{item.unit}</td>
                    <td style={{ textAlign: 'right' }} className="currency-cell">{item.approved_qty}</td>
                    <td style={{ textAlign: 'right' }} className="currency-cell">PKR {formatPKR(item.contract_rate_pkr)}</td>
                    <td style={{ textAlign: 'right', fontWeight: 600, color: '#34d399' }} className="currency-cell">
                      PKR {formatPKR(item.amount_pkr)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Financial Summary Box */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '32px' }}>
          <div style={{ width: '380px', display: 'flex', flexDirection: 'column', gap: '8px', background: '#131c2e', padding: '18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Current Period Amount:</span>
              <strong style={{ color: '#34d399', fontSize: '1.05rem' }}>PKR {formatPKR(ipc.total_current_amount_pkr)}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Cumulative Certified Amount:</span>
              <strong style={{ color: '#38bdf8' }}>PKR {formatPKR(ipc.cumulative_amount_pkr)}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', paddingTop: '6px', borderTop: '1px solid var(--border-color)' }}>
              <span style={{ color: 'var(--text-dim)' }}>Remaining Contract Balance:</span>
              <strong style={{ color: '#fff' }}>PKR {formatPKR(remainingContract)}</strong>
            </div>
          </div>
        </div>

        {/* Signature Blocks */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px', paddingTop: '24px', borderTop: '1px dashed var(--border-color)' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ height: '40px', borderBottom: '1px solid var(--border-color)', marginBottom: '8px' }}></div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#fff' }}>Contractor Representative</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Tariq Mahmood (Verified)</div>
          </div>

          <div style={{ textAlign: 'center' }}>
            <div style={{ height: '40px', borderBottom: '1px solid var(--border-color)', marginBottom: '8px' }}></div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#fff' }}>Resident Engineer (RE)</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Engr. Bilal Khan (Certified)</div>
          </div>

          <div style={{ textAlign: 'center' }}>
            <div style={{ height: '40px', borderBottom: '1px solid var(--border-color)', marginBottom: '8px' }}></div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#fff' }}>Project Client / Sponsor</div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Malik Zafar (Approved)</div>
          </div>
        </div>
      </div>
    </div>
  );
};
