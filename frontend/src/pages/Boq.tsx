import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { BoqItem } from '../types';
import { Link } from 'react-router-dom';
import { ShieldCheck, Search, Filter, Lock, CheckCircle2 } from 'lucide-react';

export const Boq: React.FC = () => {
  const [items, setItems] = useState<BoqItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [validationMsg, setValidationMsg] = useState<string | null>(null);

  useEffect(() => {
    loadBoq();
  }, []);

  const loadBoq = async () => {
    try {
      setLoading(true);
      const data = await api.getBoqItems();
      setItems(data);
    } catch (e) {
      console.error('Failed to load BOQ items:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleValidateBoq = async () => {
    try {
      const res = await api.validateBoq();
      setValidationMsg(res.status_message);
      setTimeout(() => setValidationMsg(null), 6000);
    } catch (e: any) {
      setValidationMsg(e.message || 'Validation failed');
    }
  };

  const categories = ['ALL', ...Array.from(new Set(items.map((i) => i.category)))];

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
      String(item.item_number).includes(searchTerm);
    const matchesCat = selectedCategory === 'ALL' || item.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  const formatPKR = (val: string | number) => {
    return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };

  return (
    <div>
      {/* Header & Immutability Badge */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Contractual Bill of Quantities (BOQ)</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            Authoritative 24-Item Contract Baseline — Non-editable during execution
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
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
            Contract Baseline Immutable
          </div>

          <button onClick={handleValidateBoq} className="btn btn-secondary btn-sm">
            <CheckCircle2 size={14} color="#10b981" />
            Verify Total
          </button>
        </div>
      </div>

      {validationMsg && (
        <div style={{
          background: 'rgba(16, 185, 129, 0.15)',
          border: '1px solid rgba(16, 185, 129, 0.4)',
          color: '#34d399',
          padding: '12px 18px',
          borderRadius: 'var(--radius-md)',
          fontSize: '0.85rem',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <CheckCircle2 size={16} />
          {validationMsg}
        </div>
      )}

      {/* Contract & Cost Summary Cards */}
      <div className="metrics-grid" style={{ marginBottom: '20px' }}>
        <div className="metric-card">
          <span className="metric-label">Covered Area</span>
          <span className="metric-value">750 sq.ft.</span>
          <span className="metric-subtext">Single Storey (25' × 45' Plot)</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Contract BOQ Total</span>
          <span className="metric-value">PKR 5,135,535.00</span>
          <span className="metric-subtext">Sum of exactly 24 tender items</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Cost per Covered sq.ft.</span>
          <span className="metric-value">PKR 6,847.38</span>
          <span className="metric-subtext">Indicative working rate (Islamabad 2026)</span>
        </div>

        <div className="metric-card">
          <span className="metric-label">Budget with 5% Contingency</span>
          <span className="metric-value" style={{ color: '#fbbf24' }}>PKR 5,392,311.75</span>
          <span className="metric-subtext">Recommended allowance (PKR 256,776.75)</span>
        </div>
      </div>

      {/* Search and Filters */}
      <div style={{ display: 'flex', gap: '14px', marginBottom: '16px' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }} />
          <input
            type="text"
            className="form-input"
            placeholder="Search by description, category, or #..."
            style={{ paddingLeft: '36px', width: '100%' }}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <select
          className="form-select"
          style={{ width: '220px' }}
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      {/* BOQ Master Table */}
      <div className="table-wrapper">
        <table className="siteflow-table">
          <thead>
            <tr>
              <th style={{ width: '40px' }}>#</th>
              <th>Category</th>
              <th>Description</th>
              <th>Unit</th>
              <th style={{ textAlign: 'right' }}>Contract Qty</th>
              <th style={{ textAlign: 'right' }}>Rate (PKR)</th>
              <th style={{ textAlign: 'right' }}>Contract Amount</th>
              <th style={{ textAlign: 'right' }}>Approved Qty</th>
              <th style={{ textAlign: 'right' }}>Remaining Qty</th>
              <th style={{ textAlign: 'right' }}>Approved Amount</th>
              <th style={{ width: '110px' }}>Progress</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredItems.map((item) => (
              <tr key={item.id}>
                <td style={{ fontWeight: 700, color: 'var(--primary)' }}>{item.item_number}</td>
                <td style={{ fontWeight: 600 }}>{item.category}</td>
                <td>
                  <Link to={`/boq/${item.id}`} style={{ color: '#fff', textDecoration: 'none', fontWeight: 500 }}>
                    {item.description}
                  </Link>
                  {item.remark && (
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>{item.remark}</div>
                  )}
                </td>
                <td style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{item.unit}</td>
                <td style={{ textAlign: 'right' }} className="currency-cell">{item.contract_qty}</td>
                <td style={{ textAlign: 'right' }} className="currency-cell">{formatPKR(item.rate_pkr)}</td>
                <td style={{ textAlign: 'right', fontWeight: 600 }} className="currency-cell">{formatPKR(item.amount_pkr)}</td>
                <td style={{ textAlign: 'right', color: '#34d399' }} className="currency-cell">{item.approved_qty}</td>
                <td style={{ textAlign: 'right', color: '#38bdf8' }} className="currency-cell">{item.remaining_qty}</td>
                <td style={{ textAlign: 'right', color: '#34d399' }} className="currency-cell">{formatPKR(item.approved_amount_pkr)}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div className="progress-bar-container" style={{ width: '60px' }}>
                      <div className="progress-bar-fill" style={{ width: `${Math.min(100, Number(item.progress_pct))}%` }}></div>
                    </div>
                    <span style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>{item.progress_pct}%</span>
                  </div>
                </td>
                <td>
                  <span className={`status-pill ${
                    item.status === 'Fully Approved' ? 'status-emerald' :
                    item.status === 'Partially Approved' ? 'status-amber' :
                    item.status === 'In Progress' ? 'status-cyan' : 'status-slate'
                  }`}>
                    {item.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
