# SiteFlow AI — Construction Workflow & IPC Management

SiteFlow AI is an AI-powered construction project-control platform for residential and commercial works. Built for deterministic quality assurance and financial control, it digitizes the complete lifecycle from Check Requests to Interim Payment Certificates (IPC).

[![Build Status](https://github.com/SidraPervaiz1122/SiteFlowAI/actions/workflows/ci.yml/badge.svg)](https://github.com/SidraPervaiz1122/SiteFlowAI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Key Features

- **Strict Server-Side Verified Workflow**: Digitizes the entire inspection lifecycle seamlessly from initial check requests to final IPC generation.
- **Role-Based Access Control (RBAC)**: Supports roles for `CONTRACTOR`, Resident Engineer (`RE`), and `CLIENT` with robust isolation of privileges enforced via JWT.
- **Atomic Quantity Validation**: Mathematically prevents over-approvals natively within the database transactions (approved quantity cannot exceed remaining contractual BOQ quantity).
- **Immutable Contract Baseline**: Core BOQ structures (quantities, rates, units) remain immutable throughout the normal execution lifecycle.
- **AI-Assisted Processing**: Features advisory-only AI pre-reviews and assistance that helps with document readiness, but keeps final authoritative decisions human-in-the-loop.

## Tech Stack

### Backend
- **Framework**: FastAPI (>=0.110.0)
- **Database**: SQLAlchemy (>=2.0.28) / SQLite (Development)
- **Validation**: Pydantic (>=2.6.4)
- **Authentication**: PyJWT (>=2.8.0), PassLib with bcrypt

### Frontend
- **Framework**: React (^18.2.0)
- **Routing**: React Router DOM (^6.22.3)
- **Tooling**: Vite (^5.1.6) & TypeScript (^5.2.2)
- **Icons**: Lucide React (^0.359.0)

## Architecture & Workflow Diagram

```text
[CONTRACTOR] 
  └── Creates Check Request (Attaches evidence)
       └── Submits for Inspection
            └── AI Pre-Review (Advisory: Readiness, risk indicators)
                 └── [RESIDENT ENGINEER] Inspects on-site
                      └── Drafts observations & Accepts/Rejects
                           └── [CONTRACTOR] Submits actual measured quantity
                                └── [RESIDENT ENGINEER] Approves quantity (Atomic: Approved Qty <= Remaining Qty)
                                     └── [CLIENT] Performs independent review
                                          └── [CLIENT] Approves work
                                               └── IPC Generated from Authoritative Quantities
```

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Backend Setup
```bash
# Create virtual environment and install requirements
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r backend/requirements.txt

# Initialize and seed demo database
python -m backend.db.seed

# Run backend API server
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# The app will run on http://localhost:5173
```

### Running Tests
```bash
# From the project root, ensure virtualenv is activated
pytest -v
```

## Demo Credentials

The backend comes pre-seeded with demo roles. The UI includes a Quick Demo Role Switcher that generates real authenticated JWT sessions using the `/api/auth/quick-switch` endpoint.

| Role | Email | Password | Full Name |
| :--- | :--- | :--- | :--- |
| **Contractor** | `contractor@example.com` | `Contractor@123` | Tariq Mahmood |
| **Resident Engineer** | `re@example.com` | `Engineer@123` | Engr. Bilal Khan |
| **Client** | `client@example.com` | `Client@123` | Malik Zafar |

## Deployment Pipeline

Deployment is automated via a robust GitHub Actions CI/CD pipeline targeting Azure App Service using Docker. 
1. **Build & Push**: Triggers on pushes to `main`. The Docker image is built from the root `Dockerfile` and pushed to Azure Container Registry (ACR).
2. **Deploy**: Azure Web App is restarted with the latest image.
3. **Health Check**: The pipeline validates successful startup via the exposed health check endpoints.

## Project Structure

```text
.
├── backend/          # FastAPI backend application
│   ├── api/          # API routing (auth, check_requests, boq, ipc, ai, etc.)
│   ├── app/          # Core setup (main.py, config, dependencies)
│   ├── db/           # Database seed scripts
│   ├── models/       # SQLAlchemy schema definitions
│   └── services/     # Business logic (quantities, approvals, workflows)
├── frontend/         # React SPA (Vite + TS)
│   └── src/          # Source code and components
└── scripts/          # Utility scripts (e.g., reset-demo)
```

## Contributing

To contribute to SiteFlow AI:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
