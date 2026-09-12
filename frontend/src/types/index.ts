export type UserRole = 'CONTRACTOR' | 'RE' | 'CLIENT';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: number;
}

export interface BoqItem {
  id: number;
  project_id: number;
  item_number: number;
  category: string;
  description: string;
  unit: string;
  contract_qty: string | number;
  rate_pkr: string | number;
  amount_pkr: string | number;
  remark?: string;
  is_active: number;
  approved_qty: string | number;
  remaining_qty: string | number;
  approved_amount_pkr: string | number;
  progress_pct: string | number;
  status: string;
}

export interface ProjectSummary {
  contract_value_pkr: string | number;
  approved_value_pkr: string | number;
  remaining_value_pkr: string | number;
  physical_progress_pct: string | number;
  financial_progress_pct: string | number;
  pending_inspections: number;
  pending_re_approvals: number;
  pending_client_approvals: number;
  ipc_current_value_pkr: string | number;
  ipc_cumulative_value_pkr: string | number;
}

export interface Evidence {
  id: number;
  check_request_id: number;
  inspection_id?: number;
  filename: string;
  file_path: string;
  file_type: string;
  file_size_bytes: number;
  caption?: string;
  uploaded_by_id: number;
  created_at: string;
}

export interface AiReview {
  id: number;
  check_request_id: number;
  readiness: string;
  confidence_score: number;
  missing_evidence?: string;
  potential_issues?: string;
  suggested_checks?: string;
  recommended_questions?: string;
  created_at: string;
}

export interface Observation {
  id: number;
  inspection_id: number;
  title: string;
  description: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  category: string;
  corrective_action?: string;
  is_ai_generated: boolean;
  accepted_by_re: boolean;
  created_at: string;
}

export interface Inspection {
  id: number;
  check_request_id: number;
  inspector_id: number;
  decision?: 'ACCEPT' | 'REJECT' | 'CONDITIONAL';
  inspector_notes?: string;
  checklist_results?: string;
  inspected_at?: string;
  created_at: string;
  observations: Observation[];
}

export interface CheckRequest {
  id: number;
  project_id: number;
  boq_item_id: number;
  cr_number: string;
  title: string;
  description?: string;
  proposed_qty: string | number;
  unit: string;
  status: string;
  created_by_id: number;
  created_at: string;
  updated_at?: string;
  boq_item_category?: string;
  boq_item_description?: string;
  boq_item_rate_pkr?: string | number;
  evidences: Evidence[];
  ai_reviews: AiReview[];
  inspections: Inspection[];
}

export interface QuantityApproval {
  id: number;
  quantity_measurement_id: number;
  boq_item_id: number;
  approved_qty: string | number;
  contract_rate_pkr: string | number;
  approved_amount_pkr: string | number;
  re_id: number;
  status: string;
  re_comments?: string;
  created_at: string;
  cr_number?: string;
  boq_item_description?: string;
  boq_item_unit?: string;
  client_review_status?: string;
}

export interface IpcItem {
  id: number;
  ipc_id: number;
  boq_item_id: number;
  quantity_approval_id: number;
  item_number: number;
  category: string;
  description: string;
  unit: string;
  approved_qty: string | number;
  contract_rate_pkr: string | number;
  amount_pkr: string | number;
}

export interface Ipc {
  id: number;
  project_id: number;
  ipc_number: string;
  period_start: string;
  period_end: string;
  total_current_amount_pkr: string | number;
  cumulative_amount_pkr: string | number;
  status: string;
  notes?: string;
  created_by_id: number;
  created_at: string;
  items: IpcItem[];
}

export interface AuditLog {
  id: number;
  project_id?: number;
  actor_id?: number;
  actor_name: string;
  actor_role: string;
  action: string;
  entity_type: string;
  entity_id: string;
  old_value?: string;
  new_value?: string;
  metadata_json?: string;
  created_at: string;
}
