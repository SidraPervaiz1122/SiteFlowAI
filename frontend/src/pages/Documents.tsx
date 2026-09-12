import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { FolderArchive, Upload, FileText, Download, Plus } from 'lucide-react';

export const Documents: React.FC = () => {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('GENERAL');
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const loadDocs = async () => {
    try {
      setLoading(true);
      const data = await api.getDocuments();
      setDocuments(data);
    } catch (e) {
      console.error('Failed to load documents:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocs();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append('title', title);
      fd.append('category', category);
      fd.append('file', file);
      await api.uploadDocument(fd);
      setShowModal(false);
      setTitle('');
      setFile(null);
      await loadDocs();
    } catch (err: any) {
      alert(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Project Documents & Specifications</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            Central repository for drawings, takeoff sheets, specifications and reports
          </p>
        </div>

        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Upload Document
        </button>
      </div>

      <div className="table-wrapper">
        <table className="siteflow-table">
          <thead>
            <tr>
              <th>Document Title</th>
              <th>Category</th>
              <th>Filename</th>
              <th>Size</th>
              <th>Date Uploaded</th>
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '36px', color: 'var(--text-dim)' }}>
                  No documents uploaded yet.
                </td>
              </tr>
            ) : (
              documents.map((d) => (
                <tr key={d.id}>
                  <td style={{ fontWeight: 600, color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={16} color="var(--primary)" />
                    {d.title}
                  </td>
                  <td><span className="status-pill status-cyan">{d.category}</span></td>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-muted)' }}>{d.filename}</td>
                  <td style={{ color: 'var(--text-dim)' }}>{(d.file_size_bytes / 1024).toFixed(1)} KB</td>
                  <td style={{ color: 'var(--text-dim)' }}>{new Date(d.created_at).toLocaleDateString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '16px' }}>Upload Project Document</h2>
            <form onSubmit={handleUpload}>
              <div className="form-group">
                <label className="form-label">Document Title</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g. Structural Rebar BBS Schedule"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Category</label>
                <select
                  className="form-select"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                >
                  <option value="GENERAL">GENERAL</option>
                  <option value="SPECIFICATION">SPECIFICATION</option>
                  <option value="DRAWING">DRAWING</option>
                  <option value="CONTRACT">CONTRACT</option>
                  <option value="REPORT">REPORT</option>
                  <option value="TAKEOFF">TAKEOFF</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">File</label>
                <input
                  type="file"
                  className="form-input"
                  style={{ padding: '6px' }}
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  required
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={uploading}>
                  {uploading ? 'Uploading...' : 'Upload'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
