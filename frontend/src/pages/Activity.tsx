import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { AuditLog } from '../types';
import { History, Filter, Search, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const Activity: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEntity, setSelectedEntity] = useState('ALL');

  const loadLogs = async () => {
    try {
      setLoading(true);
      const data = await api.getAuditTrail(selectedEntity === 'ALL' ? undefined : selectedEntity);
      setLogs(data);
    } catch (e) {
      console.error('Failed to load audit logs:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, [selectedEntity]);

  const entityTypes = ['ALL', 'CHECK_REQUEST', 'INSPECTION', 'OBSERVATION', 'QUANTITY_MEASUREMENT', 'QUANTITY_APPROVAL', 'CLIENT_REVIEW', 'IPC', 'USER'];

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Project Audit Trail & Timeline</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            Immutable event log recording every state transition, evidence upload, quantity approval & payment certification
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <select
            className="form-select"
            value={selectedEntity}
            onChange={(e) => setSelectedEntity(e.target.value)}
            style={{ width: '220px' }}
          >
            {entityTypes.map((et) => (
              <option key={et} value={et}>{et}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="siteflow-table">
          <thead>
            <tr>
              <th style={{ width: '160px' }}>Timestamp</th>
              <th>Actor</th>
              <th>Action</th>
              <th>Entity</th>
              <th>Details / Values</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No audit logs recorded matching this criteria.
                </td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id}>
                  <td style={{ color: 'var(--text-dim)', fontSize: '0.78rem', whiteSpace: 'nowrap' }}>
                    {new Date(log.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'medium' })}
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: log.actor_role === 'CONTRACTOR' ? '#fbbf24' : (log.actor_role === 'RE' ? '#38bdf8' : (log.actor_role === 'CLIENT' ? '#34d399' : '#a5b4fc'))
                      }} />
                      <strong style={{ color: '#fff', fontSize: '0.85rem' }}>{log.actor_name}</strong>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>({log.actor_role})</span>
                    </div>
                  </td>
                  <td>
                    <span className="status-pill status-cyan">{log.action}</span>
                  </td>
                  <td>
                    <div style={{ fontSize: '0.82rem', fontWeight: 600 }}>{log.entity_type}</div>
                    <code style={{ fontSize: '0.74rem', color: 'var(--primary)' }}>{log.entity_id}</code>
                  </td>
                  <td>
                    {log.new_value && (
                      <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)', maxWidth: '400px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {log.new_value}
                      </div>
                    )}
                    {log.old_value && (
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                        prev: {log.old_value}
                      </div>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
