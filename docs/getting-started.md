# Getting Started

## Prerequisites
- Python 3.10+
- Node.js 18+ and npm

## Backend Setup
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

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
# The app will run on http://localhost:5173
```

## Running Tests
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
