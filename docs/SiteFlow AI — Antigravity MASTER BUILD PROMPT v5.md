# SITEFLOW AI
## MASTER BUILD PROMPT v5 — FULL IMPLEMENTATION

You are the lead software architect, senior full-stack engineer, AI engineer, database engineer, UI/UX engineer, QA engineer, and DevOps engineer responsible for building this application.

Your task is to **actually build the complete working application**, not merely describe it, generate a plan, or create a folder structure.

---

# 1. PRODUCT IDENTITY

Build:

**SiteFlow AI — AI-Powered Construction Inspection, Approval & IPC Management Platform**

SiteFlow AI is a construction project-control platform that digitizes:

- BOQ management
- Check Requests
- Site inspections
- AI-assisted inspection pre-review
- AI-assisted observation drafting
- Engineer approval
- Client approval
- Quantity measurement and approval
- IPC generation
- Construction progress tracking
- Document/evidence management
- Audit trails
- AI/RAG project assistance

The product should feel like a **serious construction management SaaS platform**, not a generic CRUD dashboard.

The application must be suitable for a **hackathon demonstration**, while maintaining strong architectural foundations and deterministic business logic.

---

# 2. PRIMARY OBJECTIVE

Build a complete runnable MVP that demonstrates this end-to-end workflow:

CONTRACTOR
→ creates Check Request
→ attaches evidence
→ AI performs advisory pre-review
→ submits for inspection
→ RE inspects
→ RE records observations
→ RE accepts/rejects inspection
→ Contractor submits actual quantity
→ RE approves quantity
→ CLIENT reviews approved work
→ CLIENT approves
→ approved quantity becomes eligible for IPC
→ IPC is generated from approved quantities
→ progress/cost dashboards update
→ every important action is recorded in the audit trail

The entire workflow must work end-to-end using real database records.

---

# 3. IMPORTANT — INSPECT BEFORE CODING

Before modifying the repository:

1. Inspect the entire existing project.
2. Identify:
   - current framework
   - frontend stack
   - backend stack
   - database
   - existing routes
   - existing components
   - existing APIs
   - existing authentication
   - existing dependencies
   - existing environment configuration
3. Reuse useful existing code where practical.
4. Do not blindly delete a working project.
5. Do not rebuild everything from scratch if a functional foundation already exists.
6. Adapt the architecture below to the existing technology if necessary.

If the repository is empty, initialize the project using a sensible modern full-stack architecture.

---

# 4. TARGET ARCHITECTURE

Use the following structure as the **target architecture**.

IMPORTANT:

- You are responsible for creating the folders and files.
- Do not ask me to manually create them.
- Do not merely print the structure.
- Actually create and populate the required files.
- Do not create empty placeholder files.
- Every created implementation file should contain working code or a deliberate configuration/documentation purpose.
- You may slightly adapt filenames to the selected framework.
- Architectural responsibilities must remain equivalent.
- If an existing project already follows a different but sound convention, preserve it rather than forcing unnecessary restructuring.

Target structure:

```text
siteflow-ai/
│
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── dependencies.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── boq.py
│   │   ├── check_requests.py
│   │   ├── inspections.py
│   │   ├── quantities.py
│   │   ├── approvals.py
│   │   ├── client_reviews.py
│   │   ├── ipc.py
│   │   ├── documents.py
│   │   ├── notifications.py
│   │   ├── audit.py
│   │   └── ai.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── boq_item.py
│   │   ├── check_request.py
│   │   ├── evidence.py
│   │   ├── inspection.py
│   │   ├── observation.py
│   │   ├── quantity_measurement.py
│   │   ├── quantity_approval.py
│   │   ├── client_review.py
│   │   ├── ipc.py
│   │   ├── ipc_item.py
│   │   ├── document.py
│   │   ├── ai_review.py
│   │   ├── ai_observation.py
│   │   ├── rag_document.py
│   │   ├── rag_chunk.py
│   │   ├── notification.py
│   │   └── audit_log.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── project.py
│   │   ├── boq.py
│   │   ├── check_request.py
│   │   ├── inspection.py
│   │   ├── observation.py
│   │   ├── quantity.py
│   │   ├── approval.py
│   │   ├── client_review.py
│   │   ├── ipc.py
│   │   ├── document.py
│   │   ├── ai.py
│   │   ├── notification.py
│   │   └── audit.py
│   │
│   ├── services/
│   │   ├── auth/
│   │   ├── boq/
│   │   ├── workflow/
│   │   │   └── state_machine.py
│   │   ├── check_requests/
│   │   ├── inspections/
│   │   ├── quantities/
│   │   ├── approvals/
│   │   ├── ipc/
│   │   ├── audit/
│   │   ├── notifications/
│   │   └── documents/
│   │
│   ├── ai/
│   │   ├── client.py
│   │   ├── config.py
│   │   ├── prompts.py
│   │   ├── guardrails.py
│   │   ├── output_validator.py
│   │   ├── fallback.py
│   │   ├── review/
│   │   ├── observation/
│   │   ├── assistant/
│   │   └── rag/
│   │
│   ├── core/
│   │   ├── constants.py
│   │   ├── enums.py
│   │   ├── exceptions.py
│   │   ├── permissions.py
│   │   ├── money.py
│   │   ├── pagination.py
│   │   └── logging.py
│   │
│   ├── db/
│   │   ├── migrations/
│   │   ├── seed.py
│   │   ├── seed_users.py
│   │   ├── seed_boq.py
│   │   └── seed_demo.py
│   │
│   ├── data/
│   │   ├── boq/
│   │   │   ├── siteflow_boq.json
│   │   │   └── boq_validation.json
│   │   └── project/
│   │       ├── assumptions.json
│   │       └── takeoff.json
│   │
│   ├── storage/
│   │   ├── uploads/
│   │   └── documents/
│   │
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       │   ├── test_boq_total.py
│       │   ├── test_quantity_calculation.py
│       │   ├── test_quantity_validation.py
│       │   ├── test_amount_calculation.py
│       │   ├── test_progress.py
│       │   ├── test_workflow.py
│       │   └── test_authorization.py
│       │
│       ├── integration/
│       │   ├── test_check_request.py
│       │   ├── test_inspection.py
│       │   ├── test_re_approval.py
│       │   ├── test_client_approval.py
│       │   └── test_ipc.py
│       │
│       └── security/
│           ├── test_role_permissions.py
│           ├── test_contract_immutability.py
│           └── test_quantity_overapproval.py
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   │
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── routes.tsx
│       │
│       ├── api/
│       │
│       ├── components/
│       │   ├── layout/
│       │   ├── common/
│       │   ├── boq/
│       │   ├── check-requests/
│       │   ├── inspections/
│       │   ├── approvals/
│       │   ├── ipc/
│       │   ├── ai/
│       │   ├── documents/
│       │   ├── audit/
│       │   └── dashboard/
│       │
│       ├── pages/
│       │   ├── Login.tsx
│       │   ├── Dashboard.tsx
│       │   ├── Boq.tsx
│       │   ├── BoqItem.tsx
│       │   ├── CheckRequests.tsx
│       │   ├── CheckRequestDetail.tsx
│       │   ├── Inspections.tsx
│       │   ├── InspectionDetail.tsx
│       │   ├── Approvals.tsx
│       │   ├── Ipc.tsx
│       │   ├── IpcDetail.tsx
│       │   ├── Documents.tsx
│       │   ├── AiAssistant.tsx
│       │   ├── Activity.tsx
│       │   └── NotFound.tsx
│       │
│       ├── hooks/
│       ├── context/
│       ├── store/
│       ├── types/
│       ├── utils/
│       ├── styles/
│       └── tests/
│
├── scripts/
│   ├── setup.sh
│   ├── seed.sh
│   ├── test.sh
│   └── reset-demo.sh
│
└── docs/
    ├── architecture.md
    ├── api.md
    ├── database.md
    ├── ai.md
    ├── rag.md
    ├── workflow.md
    └── demo.md
```

---

# 5. ARCHITECTURAL PRINCIPLES

## Backend is the source of truth.

The frontend must NEVER be authoritative for:

- quantity calculations
- remaining quantities
- amount calculations
- progress calculations
- approvals
- IPC values
- workflow transitions
- permissions
- authorization
- contract data

All important calculations and validations must be performed server-side.

The frontend should display values returned by the backend.

---

# 6. BUSINESS ROLES

There are exactly three roles:

1. CONTRACTOR
2. RE — Resident Engineer
3. CLIENT

Do not create additional business roles for the MVP.

## Contractor

Can:

- create Check Requests
- select BOQ items
- enter proposed/current quantity
- upload evidence
- submit requests
- view AI pre-review
- view inspection results
- submit quantities
- view approvals
- view IPC status
- view project progress

Cannot:

- approve their own work
- perform RE approval
- perform Client approval
- modify approved contractual BOQ data

## RE

Can:

- review Check Requests
- inspect work
- review evidence
- use AI advisory recommendations
- draft observations
- record observations
- accept/reject inspections
- approve quantities
- reject quantities
- review progress
- send approved work to Client review

Cannot:

**EVER perform Client approval.**

This restriction must be enforced server-side.

## Client

Can:

- review RE-approved work
- review quantities
- review evidence
- review inspection information
- approve/reject Client review
- view IPC
- view project progress
- view audit information

Cannot:

- perform RE approval
- act as Contractor
- modify contract BOQ quantities/rates

---

# 7. AUTHORIZATION

Implement real role-based access control.

Authorization must be enforced on the backend.

Never rely solely on hiding UI buttons.

For every protected operation:

1. Authenticate the user.
2. Determine their role.
3. Check permission.
4. Validate workflow state.
5. Perform operation only if authorized.
6. Record an audit event.

Attempted unauthorized operations must return appropriate authorization errors.

---

# 8. CONTRACTUAL BOQ — SOURCE OF TRUTH

The application must include the following exact 24 BOQ items.

Do NOT invent, modify, simplify, round, or substitute these values.

## BOQ

| # | Category | Description | Unit | Qty | Rate PKR | Amount PKR | Remark |
|---|---|---|---|---:|---:|---:|---|
| 1 | Preliminaries | Mobilization, setting out, temporary works | L.S. | 1 | 75,000 | 75,000 | Verify site |
| 2 | Earthwork | Excavation in foundations / trenches | m³ | 25 | 1,800 | 45,000 | Provisional; revise after structural design |
| 3 | Earthwork | Backfilling and compaction | m³ | 15 | 1,200 | 18,000 | Provisional |
| 4 | Concrete | PCC/blinding | m³ | 5 | 14,500 | 72,500 | Provisional |
| 5 | Concrete | RCC foundations, columns, beams, slab | m³ | 2.44 | 42,000 | 102,480 | Preliminary |
| 6 | Reinforcement | Deformed steel reinforcement | kg | 7,500 | 285 | 2,137,500 | Preliminary allowance; structural BBS governs |
| 7 | Formwork | Formwork to RCC works | m² | 76.6 | 950 | 72,770 | Provisional |
| 8 | Masonry | Brick/block masonry | m³ | 30.79 | 15,500 | 477,245 | Approx. 9" external + 4.5" internal walls |
| 9 | Plaster | Internal & external cement plaster | m² | 334.5 | 520 | 173,940 | Approximate |
| 10 | Flooring | Floor tiles including adhesive/screed | m² | 45.3 | 650 | 29,445 | Approx. 65% of covered area |
| 11 | Wall Tiling | Bathroom wall/floor tiles | m² | 14.3 | 700 | 10,010 | Approximate |
| 12 | Waterproofing | Roof waterproofing system | m² | 69.7 | 500 | 34,850 | Approximate roof area |
| 13 | Doors | Complete doors incl. frames/hardware | No. | 5 | 45,000 | 225,000 | Schedule-based allowance |
| 14 | Windows | Aluminium/UPVC glazed windows | No. | 5 | 28,000 | 140,000 | Schedule-based allowance |
| 15 | Painting | Internal & external paint system | m² | 334.5 | 420 | 140,490 | Approximate paintable area |
| 16 | Ceiling | False ceiling / ceiling treatment | m² | 52.3 | 750 | 39,225 | Optional/where required |
| 17 | Electrical | Lighting/socket/switch points | Point | 35 | 4,500 | 157,500 | Preliminary |
| 18 | Electrical | DB, breakers, earthing and accessories | L.S. | 1 | 85,000 | 85,000 | Complete installation |
| 19 | Plumbing | Water supply & drainage piping | L.S. | 1 | 225,000 | 225,000 | Complete installation |
| 20 | Sanitary | WC, wash basin, shower, mixers, accessories | Set | 2 | 85,000 | 170,000 | Two bathrooms |
| 21 | Kitchen | Kitchen cabinets / counter / sink | L.S. | 1 | 275,000 | 275,000 | Allowance |
| 22 | External Works | Water tank, pump, chambers and connections | L.S. | 1 | 175,000 | 175,000 | Subject to utility layout |
| 23 | External Works | Car porch / driveway finish | m² | 34.8 | 850 | 29,580 | Approximate |
| 24 | External Works | Main gate and boundary works | L.S. | 1 | 225,000 | 225,000 | Subject to final architectural detail |

### CONTRACT TOTAL

**PKR 5,135,535**

The system must validate that:

```text
sum(all BOQ item amounts) = PKR 5,135,535
```

If the calculated total differs, treat it as a data integrity error.

---

# 9. CONTRACT DATA IMMUTABILITY

Contractual BOQ data is immutable in the MVP.

The following must not be casually edited through the UI:

- contract quantity
- contract rate
- contract amount
- contractual description
- contractual unit

If corrections are needed, they require a controlled administrative/data migration process, not ordinary project execution UI.

Do not implement variations/change orders in the MVP.

---

# 10. PROJECT CONTEXT

The BOQ represents a:

- 5 Marla residential project
- single-storey house
- approximately 750 sq.ft. covered area

Additional context:

- Plot: 25' × 45'
- Covered area: approximately 25' × 30'
- Front parking/porch: approximately 15'
- Single storey
- External wall length: approximately 110 ft
- External wall volume: approximately 825 ft³
- Internal wall volume: approximately 262.5 ft³
- Masonry total: approximately 30.79452 m³
- Floor/roof area: approximately 69.7 m²
- RCC allowance: 2.44 m³
- Rebar allowance: 7,500 kg
- Plaster area: 334.5 m²

Assumptions:

- Structural design is not final engineered design.
- RCC quantities are preliminary allowances.
- Final structural drawings govern.
- Soil investigation may change foundations.
- Rates are indicative working rates.
- Taxes are not included unless explicitly added.
- MEP quantities are preliminary.
- Coordinated shop drawings are required.
- BOQ is preliminary quantity-survey information for budgeting/tender purposes.
- Final IFC drawings require remeasurement.
- Actual plot/setbacks/soil/design changes require recalculation.
- Indicative rates are based on Islamabad/Rawalpindi 2026 working assumptions and are not contractor quotations.
- Final rates must be reconfirmed before procurement.

---

# 11. COST SUMMARY

Display:

Covered area:

**750 sq.ft.**

Total BOQ:

**PKR 5,135,535**

Approximate cost per covered sq.ft.:

**PKR 6,847.38**

Recommended contingency:

**5%**

Budget including contingency:

**PKR 5,392,311.75**

Clearly label contingency as a recommendation/allowance, not part of the contractual BOQ total.

---

# 12. CHECK REQUEST WORKFLOW

Implement a real workflow.

Example lifecycle:

```text
DRAFT
→ SUBMITTED
→ AI_PRE_REVIEW
→ PENDING_INSPECTION
→ INSPECTION_IN_PROGRESS
→ INSPECTION_ACCEPTED / INSPECTION_REJECTED
→ QUANTITY_SUBMITTED
→ RE_APPROVED / RE_REJECTED
→ CLIENT_REVIEW
→ CLIENT_APPROVED / CLIENT_REJECTED
→ IPC_ELIGIBLE
→ IPC_INCLUDED
```

Use a centralized workflow state machine.

Do not scatter transition logic throughout controllers/components.

Create something equivalent to:

```text
backend/services/workflow/state_machine.py
```

Every transition must validate:

- current state
- actor role
- actor permission
- required data
- required evidence
- business rules

---

# 13. AI PRE-REVIEW

When a Contractor submits a Check Request, AI should perform an advisory pre-review.

The AI can assess:

- completeness
- evidence quality
- missing information
- likely inspection risks
- possible documentation gaps
- potential non-conformance indicators

AI output should include structured information such as:

```text
Readiness: Ready / Needs Attention
Confidence: 0–100
Missing Evidence
Potential Issues
Suggested Inspection Checks
Recommended Questions
```

IMPORTANT:

AI is advisory only.

AI must NEVER:

- approve work
- reject work
- approve quantities
- change BOQ values
- calculate authoritative payment
- bypass RE
- bypass Client
- change workflow state independently

Human approvals remain authoritative.

---

# 14. AI OBSERVATION DRAFTING

During inspection, RE should be able to request an AI-generated observation draft.

AI can generate:

- observation title
- description
- severity
- likely category
- recommended corrective action
- evidence reference

The RE must be able to:

- edit
- accept
- reject
- regenerate

AI-generated content must clearly indicate that it is AI-assisted.

The final submitted observation belongs to the RE, not the AI.

---

# 15. INSPECTION WORKSPACE

Create a professional inspection interface.

It should show:

- Check Request details
- BOQ item
- contract quantity
- contract rate
- contractor submitted quantity
- evidence/photos/documents
- AI pre-review
- inspection checklist
- observations
- severity
- corrective actions
- RE decision
- timestamps
- activity history

Support:

- Pass / Accept
- Reject
- Conditional/needs correction if appropriate

Do not allow an inspection to be accepted without the required data.

---

# 16. QUANTITY MANAGEMENT

This is one of the most important parts of the application.

Quantity calculations must be deterministic and server-side.

For each BOQ item:

```text
Contract Qty
Previously Approved
Current Submitted Qty
Current Approved Qty
Remaining
Current Amount
Cumulative Approved Qty
Cumulative Amount
Remaining After Approval
```

Definitions:

```text
Previously Approved
=
SUM(authoritative previously approved quantities)
```

```text
Remaining
=
Contract Qty - Previously Approved
```

```text
Current Amount
=
Current Approved Qty × Contract Rate
```

```text
Cumulative Approved Qty
=
Previously Approved + Current Approved Qty
```

```text
Remaining After
=
Contract Qty - Cumulative Approved Qty
```

Never calculate authoritative values only on the frontend.

---

# 17. QUANTITY VALIDATION

The system must prevent over-approval.

If:

```text
Current Approved Qty > Remaining Qty
```

reject the operation.

Use database transactions and appropriate locking/concurrency controls so two simultaneous approvals cannot cause over-approval.

---

# 18. REQUIRED QUANTITY TEST — BOQ ITEM 5

Item 5:

```text
RCC foundations, columns, beams, slab
Contract Qty = 2.44 m³
Rate = PKR 42,000
```

If RE approves:

```text
1.00 m³
```

then:

```text
Approved = 1.00
Amount = PKR 42,000
Remaining = 1.44 m³
```

If someone then attempts to approve:

```text
1.50 m³
```

the backend must reject it.

---

# 19. REQUIRED QUANTITY TEST — BOQ ITEM 8

Item 8:

```text
Brick/block masonry
Contract Qty = 30.79 m³
Rate = PKR 15,500
```

Approve:

```text
10.00 m³
```

Expected:

```text
Amount = PKR 155,000
Remaining = 20.79 m³
```

Then approve:

```text
20.79 m³
```

Expected:

```text
Cumulative = 30.79 m³
Remaining = 0
```

Any additional approval must be rejected.

---

# 20. QUANTITY IMMUTABILITY

Once a quantity approval becomes authoritative:

- do not silently edit it
- do not overwrite it
- do not delete it without controlled correction
- preserve original record
- record corrections separately
- maintain audit history

---

# 21. RE QUANTITY APPROVAL

Only RE can perform authoritative RE quantity approval.

The RE should see:

- contract quantity
- previously approved
- remaining
- submitted quantity
- recommended amount
- evidence
- inspection result

RE can:

- approve
- reject
- approve a lower quantity than submitted if the business rules permit
- enter a reason for rejection/adjustment

All actions must be audited.

---

# 22. CLIENT REVIEW

After RE approval, the work enters Client review.

Client should see:

- BOQ item
- contract quantity
- approved quantity
- rate
- calculated amount
- inspection
- observations
- evidence
- RE decision
- audit information

Client can:

- approve
- reject
- request correction/review if implemented

Client approval must be a separate workflow state.

RE must NEVER be able to execute Client approval.

---

# 23. IPC GENERATION

IPC = Interim Payment Certificate.

IPC values must come from authoritative approved quantities.

Do NOT allow arbitrary payment amounts.

For each IPC item:

```text
Approved Quantity × Contract Rate = Amount
```

IPC should show:

- IPC number
- date
- period
- BOQ items
- approved quantities
- rates
- item amounts
- cumulative amounts
- total current IPC
- cumulative contract value
- remaining contract value

Only Client-approved/IPC-eligible work can enter the IPC.

---

# 24. DASHBOARD

Create role-aware dashboards.

## Contractor Dashboard

Show:

- project overview
- submitted Check Requests
- pending actions
- approved work
- rejected work
- quantity progress
- financial progress
- IPC status
- recent activity

## RE Dashboard

Show:

- pending inspections
- pending quantity approvals
- AI review alerts
- recent inspections
- rejected items
- progress
- outstanding actions

## Client Dashboard

Show:

- pending Client reviews
- approved work
- IPC status
- financial progress
- physical progress
- recent activity
- project overview

---

# 25. BOQ PROGRESS

Provide a BOQ progress table.

Columns should include:

- Item #
- Category
- Description
- Unit
- Contract Qty
- Approved Qty
- Remaining Qty
- Rate
- Approved Amount
- Progress %
- Status

Useful statuses:

- Not Started
- In Progress
- Partially Approved
- Fully Approved
- Inspection Pending
- Client Review
- Completed

Progress should be calculated from authoritative quantities.

---

# 26. PROJECT PROGRESS

Show useful high-level metrics:

- Contract Value
- Approved Value
- Remaining Value
- Physical Progress
- Financial Progress
- Pending Inspections
- Pending RE Approvals
- Pending Client Approvals
- IPC Current Value
- IPC Cumulative Value

Use deterministic backend calculations.

---

# 27. ACTIVITY TIMELINE

Create a project activity timeline.

Example events:

```text
Contractor submitted Check Request
AI pre-review completed
Inspection started
RE added observation
RE accepted inspection
Quantity submitted
RE approved quantity
Client review started
Client approved
IPC generated
```

Display:

- actor
- role
- action
- object
- timestamp
- relevant metadata

---

# 28. AUDIT TRAIL

Every important mutation must generate an audit event.

At minimum audit:

- login/authentication events
- Check Request creation
- Check Request submission
- evidence upload
- AI review
- inspection creation
- observation creation/edit
- inspection decision
- quantity submission
- RE quantity approval
- quantity rejection
- Client review
- Client approval
- Client rejection
- IPC creation
- IPC changes
- controlled corrections

Audit records should include:

```text
actor
actor_role
action
entity_type
entity_id
timestamp
old_value where appropriate
new_value where appropriate
metadata
```

Audit records should not be casually editable/deletable.

---

# 29. DATABASE DESIGN

Implement normalized relational database models.

At minimum support entities equivalent to:

```text
users
projects
boq_items
check_requests
evidence
inspections
observations
quantity_measurements
quantity_approvals
client_reviews
ipcs
ipc_items
documents
ai_reviews
ai_observations
rag_documents
rag_chunks
notifications
audit_logs
```

Use foreign keys and constraints.

Use timestamps.

Use indexes on frequently queried workflow/status/project fields.

Use appropriate decimal/numeric types for financial values and quantities.

Do not use floating-point arithmetic for authoritative money calculations.

---

# 30. MONEY HANDLING

Use Decimal/numeric database types for:

- rates
- amounts
- contract values
- IPC values

Avoid binary floating-point for financial truth.

Centralize money calculations in a backend utility/service.

---

# 31. BOQ IMPORT VALIDATION

Create a BOQ import/seed process.

The imported BOQ must validate:

- exactly 24 items
- correct item numbers
- correct descriptions
- correct units
- correct quantities
- correct rates
- correct amounts
- total = PKR 5,135,535

Create a validation report.

If data is inconsistent, fail loudly rather than silently changing values.

---

# 32. SEED DATA

Provide demo users:

```text
contractor@example.com
re@example.com
client@example.com
```

Use secure demo passwords and document them appropriately for local development.

Seed:

- one project
- exact 24-item BOQ
- demo Check Requests
- demo evidence
- demo inspection
- demo observations
- demo quantity approvals
- demo client review
- demo IPC
- demo audit trail

The application must have a clean demo state.

---

# 33. DEMO RESET

Provide a reset mechanism for hackathon demonstrations.

Example:

```text
scripts/reset-demo.sh
```

or equivalent for the selected stack.

It should safely reset demo data to a known state.

---

# 34. DOCUMENT MANAGEMENT

Support project documents/evidence.

Document metadata should include:

- filename
- type
- size
- uploaded by
- upload date
- linked entity
- category

Support evidence attachments for Check Requests and inspections.

For MVP, local file storage is acceptable if designed so storage can later be replaced by object storage.

---

# 35. RAG / PROJECT KNOWLEDGE

Implement a practical RAG foundation.

Potential project knowledge sources:

- BOQ
- project assumptions
- takeoff information
- uploaded project documents
- inspection records
- approved observations
- relevant project notes

The AI assistant should be able to answer project-specific questions using retrieved project context.

Examples:

> What is the remaining quantity for masonry?

> What is the contract rate for RCC?

> Which inspections are pending?

> What evidence was attached to Check Request CR-001?

> What was the latest observation?

AI answers should distinguish retrieved project facts from generated recommendations.

---

# 36. RAG GUARDRAILS

The AI must not invent project facts.

If information is unavailable:

```text
I could not find sufficient project information to answer that reliably.
```

Do not fabricate:

- quantities
- rates
- approvals
- payment values
- project statuses
- inspection results
- contract information

---

# 37. AI ARCHITECTURE

Keep AI isolated from core transaction logic.

Create centralized AI components for:

- model client
- prompt templates
- guardrails
- structured output validation
- fallback behavior
- RAG retrieval
- inspection review
- observation drafting
- assistant responses

AI failures must not break core transactional workflows.

If AI is unavailable:

- application must remain usable
- show a clear fallback message
- never block human inspection/approval solely because AI is unavailable

---

# 38. AI OUTPUT VALIDATION

Validate AI responses before displaying or storing them.

Do not blindly trust arbitrary model output.

Use structured schemas where possible.

Validate:

- required fields
- allowed enum values
- numeric ranges
- text length
- confidence range

---

# 39. NOTIFICATIONS

Implement basic notifications.

Notify relevant users when:

- Check Request submitted
- inspection pending
- inspection completed
- quantity submitted
- RE approval required
- Client approval required
- Client approval completed
- IPC generated

Notifications should be stored server-side.

---

# 40. SEARCH AND FILTERING

Provide useful search/filter functionality for:

- BOQ
- Check Requests
- inspections
- approvals
- IPCs
- activity
- documents

Filters may include:

- status
- category
- date
- BOQ item
- role
- actor

---

# 41. UI/UX REQUIREMENTS

Build a polished professional construction-management interface.

Visual direction:

- modern SaaS
- clean
- professional
- high information density without feeling cluttered
- construction/project-control aesthetic
- strong typography
- clear status indicators
- meaningful cards
- tables optimized for operational use
- responsive layout

Avoid:

- generic template-looking UI
- excessive gradients
- unnecessary animations
- oversized empty cards
- meaningless decorative elements
- fake metrics

---

# 42. RESPONSIVE DESIGN

Support:

- desktop
- laptop
- tablet
- mobile where practical

The main hackathon demonstration should be optimized for desktop.

---

# 43. ACCESSIBILITY

Implement reasonable accessibility:

- semantic HTML
- keyboard navigation
- visible focus states
- accessible form labels
- appropriate contrast
- meaningful error messages
- accessible status indicators

---

# 44. FRONTEND COMPONENT ARCHITECTURE

Keep reusable components separate from pages.

Examples:

```text
components/common/
components/boq/
components/check-requests/
components/inspections/
components/approvals/
components/ipc/
components/ai/
components/dashboard/
```

Do not place business calculations inside UI components.

---

# 45. FRONTEND STATE MANAGEMENT

Use a sensible state-management/data-fetching approach.

Keep:

- server state
- authentication state
- UI state

appropriately separated.

Do not duplicate authoritative backend calculations in local state.

---

# 46. API DESIGN

Build clean REST or equivalent APIs.

At minimum support operations for:

```text
Authentication
Projects
BOQ
Check Requests
Evidence
Inspections
Observations
Quantities
RE approvals
Client reviews
IPC
Documents
Notifications
Audit
AI
```

Use validation schemas.

Return useful error responses.

---

# 47. API SECURITY

Protect all sensitive routes.

Validate:

- authentication
- role
- ownership/project access
- workflow state
- input data
- quantity limits

Never trust client-supplied:

- role
- approval status
- calculated amount
- remaining quantity
- contract amount
- IPC total

---

# 48. WORKFLOW SECURITY

A user cannot simply call an endpoint with a different workflow state.

For example:

A Contractor must not be able to send:

```text
status = CLIENT_APPROVED
```

and cause a Client approval.

The backend must derive/validate workflow transitions.

---

# 49. CONCURRENCY

Quantity approval must be transaction-safe.

Example:

If remaining quantity is:

```text
10
```

and two RE approval requests simultaneously attempt:

```text
7
```

and

```text
6
```

the system must ensure that only valid total approval can commit.

Do not rely solely on frontend validation.

---

# 50. ERROR HANDLING

Implement clear error handling.

Examples:

```text
Unauthorized
Forbidden
Invalid workflow transition
Quantity exceeds remaining contract quantity
BOQ item not found
Inspection not ready
Client approval not permitted
IPC item not eligible
AI service unavailable
Document upload failed
```

Show user-friendly messages in the UI.

---

# 51. TESTING

Implement automated tests.

At minimum test:

## BOQ

- exact 24 items
- exact total
- exact rates
- exact quantities

## Quantity

- remaining calculation
- current amount
- cumulative amount
- zero remaining
- over-approval rejection

## Authorization

- Contractor cannot RE approve
- Contractor cannot Client approve
- RE cannot Client approve
- Client cannot RE approve

## Workflow

- valid transitions
- invalid transitions
- rejected workflows
- duplicate transitions

## IPC

- only eligible approved work
- amount derived from quantity × rate
- no arbitrary payment amount

## Security

- unauthorized API calls
- contract immutability
- quantity race/over-approval protection

---

# 52. REQUIRED ACCEPTANCE TEST

Before declaring the project complete, execute this scenario:

### STEP 1

Login as Contractor.

### STEP 2

Create Check Request for BOQ Item 8.

### STEP 3

Enter quantity:

```text
10.00 m³
```

### STEP 4

Upload evidence.

### STEP 5

Submit Check Request.

### STEP 6

AI pre-review appears.

### STEP 7

Login as RE.

### STEP 8

Inspect the Check Request.

### STEP 9

Review AI recommendation.

### STEP 10

Add/accept inspection observation.

### STEP 11

Accept inspection.

### STEP 12

Approve:

```text
10.00 m³
```

Expected:

```text
Amount = PKR 155,000
Remaining = 20.79 m³
```

### STEP 13

Login as Client.

### STEP 14

Review the work.

### STEP 15

Approve Client review.

### STEP 16

Generate IPC.

### STEP 17

Verify IPC contains:

```text
10.00 m³ × PKR 15,500
=
PKR 155,000
```

### STEP 18

Return to BOQ dashboard.

Verify progress updated.

### STEP 19

Open activity/audit.

Verify every major action exists.

---

# 53. SECOND ACCEPTANCE TEST

Test BOQ Item 5.

Contract:

```text
2.44 m³
×
PKR 42,000
```

Approve:

```text
1.00 m³
```

Expected:

```text
Amount = PKR 42,000
Remaining = 1.44 m³
```

Then attempt:

```text
1.50 m³
```

Expected:

```text
REJECTED
```

No database corruption.

No negative remaining quantity.

No excess IPC value.

---

# 54. PROJECT SINGLE-PROJECT MVP

This is a single-project hackathon MVP.

The database may support:

```text
projects
```

but the main UI does not need project switching.

Default to the seeded SiteFlow project.

Do not spend excessive time building multi-project management.

---

# 55. NO VARIATIONS IN MVP

Do not implement:

- variation orders
- claims
- change orders
- complex contract amendments
- advanced procurement

These are future capabilities.

Focus on the core inspection → approval → quantity → IPC workflow.

---

# 56. DEMO DATA SHOULD LOOK REAL

Use realistic construction terminology and records.

Example:

```text
CR-001
Foundation excavation inspection
```

```text
CR-002
Brick masonry — Ground Floor
```

```text
CR-003
RCC structural work
```

Do not fill the dashboard with obviously fake/random lorem ipsum content.

---

# 57. ENVIRONMENT CONFIGURATION

Create:

```text
.env.example
```

Include configuration for:

- database
- backend URL
- frontend URL
- authentication secret
- AI provider/API key
- storage configuration
- environment mode

Never hardcode production secrets.

If no AI API key exists, the application must use a deterministic/mock fallback suitable for the demo.

---

# 58. LOCAL DEVELOPMENT

Provide clear setup instructions.

A new developer should be able to:

```text
clone
install
configure .env
initialize database
seed demo data
start backend
start frontend
open browser
login
```

Document this in README.

---

# 59. DEMO CREDENTIALS

Document demo credentials in development documentation.

Provide separate users for:

```text
Contractor
RE
Client
```

Make it easy to switch roles during the hackathon demonstration.

---

# 60. DEMO EXPERIENCE

The UI should make role switching easy for demonstration without compromising authorization.

If a demo role selector is implemented, it must actually authenticate/switch to a real seeded account or session.

Do not implement fake role switching that merely changes frontend UI.

---

# 61. IMPORTANT BUSINESS RULES

These rules are absolute:

1. There are exactly three business roles:
   Contractor, RE, Client.

2. RE cannot perform Client approval.

3. AI cannot approve work.

4. AI cannot approve quantities.

5. AI cannot modify contractual BOQ values.

6. Backend is the source of truth.

7. Frontend cannot determine authoritative financial values.

8. Contract BOQ is immutable during normal execution.

9. No quantity approval can exceed remaining contract quantity.

10. Approved quantities are cumulative.

11. IPC values come from authoritative approved quantities.

12. No arbitrary IPC amount entry.

13. Every important mutation must be audited.

14. Workflow transitions must be validated server-side.

15. Quantity approval must be transaction-safe.

16. AI failure must not stop the core application.

17. AI must not invent project facts.

18. No variations/change orders in the MVP.

19. The BOQ must contain exactly 24 items.

20. BOQ total must equal:

**PKR 5,135,535**

---

# 62. IMPLEMENTATION PRIORITY

Build in this order:

## Priority 1 — Foundation

- repository inspection
- project setup
- database
- configuration
- authentication
- roles
- core models

## Priority 2 — Contract/BOQ

- exact BOQ
- import/seed
- BOQ display
- contract immutability
- progress calculations

## Priority 3 — Core Workflow

- Check Requests
- evidence
- inspections
- observations
- workflow state machine

## Priority 4 — Quantity

- measurement
- approval
- deterministic calculations
- over-approval protection
- RE approval

## Priority 5 — Client

- Client review
- Client approval
- workflow integration

## Priority 6 — IPC

- IPC eligibility
- IPC generation
- IPC detail
- cumulative values

## Priority 7 — AI

- AI pre-review
- observation drafting
- RAG assistant
- fallbacks
- guardrails

## Priority 8 — Dashboards

- Contractor
- RE
- Client
- BOQ progress
- activity
- notifications

## Priority 9 — QA

- tests
- security
- workflow testing
- UI testing
- acceptance scenarios

## Priority 10 — Polish

- responsive UI
- loading states
- error states
- empty states
- accessibility
- demo readiness

---

# 63. DO NOT OVERENGINEER

This is a hackathon MVP.

Do not waste implementation time on:

- Kubernetes
- microservices
- complicated event buses
- unnecessary distributed infrastructure
- advanced enterprise IAM
- elaborate DevOps pipelines
- unnecessary abstractions

Prefer a clean modular monolith with clear boundaries.

The application should be:

```text
simple enough to run
+
structured enough to scale
+
complete enough to demo
```

---

# 64. DO NOT FAKE FUNCTIONALITY

Do not create UI buttons that do nothing.

Do not create fake:

- approvals
- IPC values
- AI results
- progress numbers
- audit logs
- workflow states

If something is displayed as a real application capability, it should be backed by real implementation or clearly labeled as demo/mock fallback behavior.

---

# 65. IMPLEMENTATION REQUIREMENT

DO NOT merely generate a plan.

DO NOT stop after creating folders.

DO NOT return a long explanation instead of implementing.

Actually:

1. Create the project structure.
2. Create the required files.
3. Install/configure dependencies.
4. Build the database.
5. Build the APIs.
6. Build the frontend.
7. Seed the exact BOQ.
8. Implement authentication.
9. Implement RBAC.
10. Implement workflows.
11. Implement inspections.
12. Implement quantities.
13. Implement approvals.
14. Implement Client review.
15. Implement IPC.
16. Implement AI features.
17. Implement RAG foundation.
18. Implement audit trail.
19. Implement dashboards.
20. Implement tests.
21. Run the application.
22. Fix errors.
23. Execute acceptance tests.
24. Verify the complete demo flow.

---

# 66. EXISTING PROJECT RULE

If code already exists:

DO NOT blindly delete it.

Instead:

1. inspect it
2. understand it
3. preserve useful functionality
4. refactor where necessary
5. add missing architecture
6. fix broken implementation
7. integrate the required features

Only replace existing code when necessary.

---

# 67. FILE CREATION RULE

The target architecture is a guide for implementation.

Create only the files that are actually needed, but make sure every required responsibility has a clear home.

For example:

```text
workflow logic
→ services/workflow/state_machine

permissions
→ core/permissions

quantity calculations
→ services/quantities

IPC calculations
→ services/ipc

AI guardrails
→ ai/guardrails

AI output validation
→ ai/output_validator
```

Do not put all business logic into one giant file.

Do not put business logic directly into React components.

---

# 68. FINAL QUALITY AUDIT

Before considering the task complete, inspect the implementation and verify:

### Architecture

- clean separation
- backend owns business truth
- AI isolated
- workflow centralized
- permissions centralized

### Data

- exact BOQ
- exact total
- correct seed
- no accidental mutations

### Security

- role enforcement
- protected endpoints
- no client-side authorization reliance
- contract immutability
- quantity protection

### Workflow

- Contractor → RE → Client
- valid transitions
- invalid transitions rejected

### Quantity

- deterministic
- cumulative
- remaining correct
- over-approval impossible

### IPC

- derived from approved quantities
- no arbitrary amount

### AI

- advisory only
- validated
- fallback available
- no fabricated project facts

### UI

- professional
- responsive
- clear status
- useful tables
- meaningful empty/loading/error states

### Testing

- unit tests
- integration tests
- authorization tests
- quantity tests
- IPC tests

---

# 69. FINAL DEMO STORY

The finished application should allow me to tell this story:

> “SiteFlow AI connects the entire construction inspection and payment-control process.”

> “The Contractor raises a Check Request and uploads evidence.”

> “AI performs an instant advisory pre-review and highlights potential gaps.”

> “The Resident Engineer conducts the inspection, reviews AI recommendations, records observations, and approves the work.”

> “The approved quantity is calculated against the contractual BOQ, with the system automatically preventing over-approval.”

> “The Client then performs a separate approval.”

> “Once Client-approved, the quantity becomes eligible for the Interim Payment Certificate.”

> “The IPC is generated directly from authoritative approved quantities and contract rates.”

> “Every action is recorded in the audit trail.”

> “AI assists the project team, but never replaces human authority.”

That should be the core product story.

---

# 70. FINAL REPORT

After implementation, provide a concise final report containing:

## A. What was built

List the major implemented features.

## B. Architecture

Explain the final architecture briefly.

## C. Important files

List the most important files/modules created or changed.

## D. Database

Explain the main tables/models.

## E. AI

Explain AI features, guardrails, fallback, and RAG.

## F. Authentication

List demo users/roles.

## G. Testing

Report tests executed and results.

## H. Acceptance Tests

Report the results of:

- Item 5 quantity test
- Item 8 quantity test
- Contractor → RE → Client → IPC workflow

## I. How to Run

Give exact commands.

## J. Known Limitations

Clearly identify anything intentionally left as MVP/fallback.

---

# 71. DEFINITION OF DONE

The project is NOT complete merely because:

- folders exist
- files exist
- pages render
- mock data appears
- buttons exist

The project is complete when:

```text
The application runs
AND
the database works
AND
authentication works
AND
RBAC works
AND
the exact BOQ exists
AND
the workflow works
AND
quantity calculations are correct
AND
over-approval is prevented
AND
RE approval works
AND
Client approval is separate
AND
IPC is derived correctly
AND
audit logging works
AND
AI assistance works or safely falls back
AND
the main dashboards work
AND
tests pass
AND
the complete demo flow works
```

---

# 72. START NOW

Begin by inspecting the repository.

Then implement the application incrementally.

Do not wait for further instructions unless there is a genuinely blocking ambiguity.

Make reasonable technical decisions yourself.

Prioritize working functionality over excessive documentation.

Do not stop at planning.

**BUILD THE APPLICATION.**