PRE_REVIEW_PROMPT_TEMPLATE = """
Perform an engineering pre-review of the following Check Request before the Resident Engineer visits the site:
Project: SiteFlow 5 Marla Residential Model
BOQ Item: #{item_number} - {category} ({description})
Contract Qty: {contract_qty} {unit}
Proposed Work Qty: {proposed_qty} {unit}
Contractor Description: {description_text}
Attached Evidences: {evidences_count} attachments ({evidence_names})

Evaluate the request for completeness, technical risks, missing test reports/photographs, and provide inspection check guidelines.
Output JSON schema:
{{
  "readiness": "Ready" | "Needs Attention" | "High Risk",
  "confidence_score": 0-100,
  "missing_evidence": ["item 1", "item 2"],
  "potential_issues": ["issue 1", "issue 2"],
  "suggested_checks": ["check 1", "check 2"],
  "recommended_questions": ["question 1", "question 2"]
}}
"""

OBSERVATION_DRAFT_TEMPLATE = """
Draft an inspection site observation for Resident Engineer review:
BOQ Item: #{item_number} - {category} ({description})
Site Notes/Defect Hint: {hint}
Attached Photos: {evidence_summary}

Output JSON schema:
{{
  "title": "Short descriptive observation title",
  "description": "Technical description of the non-conformance or workmanship issue",
  "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "category": "QUALITY" | "SAFETY" | "SPECIFICATION" | "WORKMANSHIP" | "DOCUMENTATION",
  "recommended_action": "Clear actionable corrective instruction for the contractor"
}}
"""

RAG_PROMPT_TEMPLATE = """
Context:
{context}

User Query: {query}

Provide a concise, professional answer based strictly on the context provided above.
If the answer is not present in the context, respond:
'I could not find sufficient project information to answer that reliably.'
"""
