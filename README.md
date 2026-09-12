# SiteFlow AI — Construction Inspection, Approval & IPC Management Platform

SiteFlow AI is an AI-powered construction project-control platform for residential and commercial works. Built for deterministic quality assurance and financial control, it digitizes the complete lifecycle from Check Requests to Interim Payment Certificates (IPC).

---

## 1. Product Identity & Workflow

SiteFlow AI enforces a strict, server-side verified workflow:

```text
CONTRACTOR
 └── Creates Check Request
 └── Attaches photographic/document evidence
 └── Submits for inspection
      └── AI performs advisory pre-review (readiness, missing docs, risk indicators)
           └── RESIDENT ENGINEER (RE) inspects on-site
                └── Drafts/records observations (AI-assisted or manual)
                └── Accepts or rejects inspection
                     └── Contractor submits actual in-place measured quantity
                          └── RE approves quantity (Atomic check: Approved Qty <= Remaining Qty)
                               └── CLIENT performs independent review
                                    └── Client approves work
                                         └── Work becomes eligible for IPC
                                              └── IPC is generated from authoritative quantities
                                                   └── Dashboards & Audit Trail update
```

---

## 2. Key Business Invariants

1. **Exact 24-Item BOQ**: Totaling exactly **PKR 5,135,535.00** for a 5 Marla model residence (750 sq.ft. covered area).
2. **Contract Baseline Immutability**: Quantities, rates, units, and descriptions cannot be casually altered during normal execution.
3. **Strict RBAC**:
   - `CONTRACTOR`: Raises check requests, uploads evidence, submits measured quantities. Cannot approve own work.
   - `RE`: Conducts site inspections, records observations, accepts/rejects inspections, approves quantities. **Strictly forbidden from Client approval**.
   - `CLIENT`: Performs separate Client approval, issues IPC certificates.
4. **Over-Approval Prevention**: Atomically verifies that any approved quantity $\le$ remaining contractual quantity.
5. **Advisory-Only AI**: AI assists with pre-reviews, observation drafting, and RAG knowledge answers, but never makes authoritative payment or approval decisions. Fully functional offline.

---

## 3. Demo Credentials

| Role | Email | Password | Full Name |
| :--- | :--- | :--- | :--- |
| **Contractor** | `contractor@example.com` | `Contractor@123` | Tariq Mahmood |
| **Resident Engineer** | `re@example.com` | `Engineer@123` | Engr. Bilal Khan |
| **Client** | `client@example.com` | `Client@123` | Malik Zafar |

*Note: The UI includes a Quick Demo Role Switcher in the top bar that generates real authenticated JWT sessions for each role.*

---

## 4. How to Run Locally

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ and npm

### 1. Setup Backend
```bash
# Create virtual environment and install requirements
python -m venv venv
.\venv\Scripts\pip install -r backend\requirements.txt

# Initialize and seed demo database (with 24 BOQ items)
.\venv\Scripts\python -m backend.db.seed

# Run backend API server on http://127.0.0.1:8000
.\venv\Scripts\uvicorn backend.app.main:app --reload --port 8000
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
# App will run on http://localhost:5173
```

### 3. Run Automated Tests
```bash
# From the project root
.\venv\Scripts\pytest -v
```

### 4. Reset Demo Data
```powershell
# Reset database back to clean initial state anytime
.\scripts\reset-demo.ps1
```
