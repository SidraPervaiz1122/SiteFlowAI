const API_BASE = '/api';

export function getToken(): string | null {
  return localStorage.getItem('siteflow_token');
}

export function setToken(token: string): void {
  localStorage.setItem('siteflow_token', token);
}

export function removeToken(): void {
  localStorage.removeItem('siteflow_token');
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    removeToken();
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
  }

  if (!response.ok) {
    let errMsg = `Request failed: ${response.statusText}`;
    try {
      const errJson = await response.json();
      errMsg = errJson.message || errJson.detail || errMsg;
    } catch (_) {}
    throw new Error(errMsg);
  }

  return response.json();
}

export const api = {
  // Auth
  login: (data: any) => request<any>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  quickSwitch: (role: string) => request<any>('/auth/quick-switch', { method: 'POST', body: JSON.stringify({ role }) }),
  getMe: () => request<any>('/auth/me'),

  // Project & BOQ
  getCurrentProject: () => request<any>('/projects/current'),
  getProgressSummary: () => request<any>('/projects/progress'),
  getBoqItems: () => request<any[]>('/boq'),
  getBoqDetail: (id: number) => request<any>(`/boq/${id}`),
  validateBoq: () => request<any>('/boq/validate'),

  // Check Requests
  getCheckRequests: (status?: string, boq_item_id?: number) => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (boq_item_id) params.append('boq_item_id', String(boq_item_id));
    return request<any[]>(`/check-requests?${params.toString()}`);
  },
  getCheckRequestDetail: (id: number) => request<any>(`/check-requests/${id}`),
  createCheckRequest: (data: any) => request<any>('/check-requests', { method: 'POST', body: JSON.stringify(data) }),
  submitCheckRequest: (id: number) => request<any>(`/check-requests/${id}/submit`, { method: 'POST' }),
  uploadEvidence: (crId: number, formData: FormData) => request<any>(`/check-requests/${crId}/evidence`, { method: 'POST', body: formData }),

  // Inspections
  startInspection: (crId: number) => request<any>(`/inspections/start/${crId}`, { method: 'POST' }),
  getInspection: (id: number) => request<any>(`/inspections/${id}`),
  generateAiObservation: (id: number, hint?: string) => {
    const url = hint ? `/inspections/${id}/ai-draft?hint=${encodeURIComponent(hint)}` : `/inspections/${id}/ai-draft`;
    return request<any>(url, { method: 'POST' });
  },
  createObservation: (inspectionId: number, data: any) => request<any>(`/inspections/${inspectionId}/observations`, { method: 'POST', body: JSON.stringify(data) }),
  decideInspection: (inspectionId: number, data: any) => request<any>(`/inspections/${inspectionId}/decide`, { method: 'POST', body: JSON.stringify(data) }),

  // Quantities & Approvals
  getQuantityContext: (boqItemId: number, submittedQty: number = 0) => request<any>(`/quantities/context/${boqItemId}?submitted_qty=${submittedQty}`),
  submitQuantity: (data: any) => request<any>('/quantities/submit', { method: 'POST', body: JSON.stringify(data) }),
  getMeasurements: () => request<any[]>('/quantities/measurements'),
  getApprovals: (status?: string) => request<any[]>(`/approvals${status ? `?status=${status}` : ''}`),
  reApproveQuantity: (data: any) => request<any>('/approvals/re', { method: 'POST', body: JSON.stringify(data) }),

  // Client Reviews
  getClientReviews: () => request<any[]>('/client-reviews'),
  submitClientReview: (data: any) => request<any>('/client-reviews', { method: 'POST', body: JSON.stringify(data) }),

  // IPC
  getIpcEligibility: () => request<any>('/ipc/eligible'),
  getIpcs: () => request<any[]>('/ipc'),
  getIpcDetail: (id: number) => request<any>(`/ipc/${id}`),
  generateIpc: (data: any) => request<any>('/ipc/generate', { method: 'POST', body: JSON.stringify(data) }),

  // Documents
  getDocuments: (category?: string) => request<any[]>(`/documents${category ? `?category=${category}` : ''}`),
  uploadDocument: (formData: FormData) => request<any>('/documents', { method: 'POST', body: formData }),

  // Audit & Notifications
  getAuditTrail: (entityType?: string, action?: string) => {
    const p = new URLSearchParams();
    if (entityType) p.append('entity_type', entityType);
    if (action) p.append('action', action);
    return request<any[]>(`/audit?${p.toString()}`);
  },
  getNotifications: () => request<any[]>('/notifications'),
  markNotificationRead: (id: number) => request<any>(`/notifications/${id}/read`, { method: 'POST' }),

  // AI Subsystem
  queryRag: (query: string) => request<any>('/ai/query', { method: 'POST', body: JSON.stringify({ query }) }),
  getAiStatus: () => request<any>('/ai/status')
};
