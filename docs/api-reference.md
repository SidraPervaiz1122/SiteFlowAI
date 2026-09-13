# API Reference

This is a summary of the main API routes grouped by domain, used by the frontend to interact with the FastAPI backend.

## Auth
Endpoints for authentication and user sessions.
- `POST /api/auth/login`: Authenticate a user with email and password.
- `POST /api/auth/quick-switch`: Convenience endpoint for demo role switching.
- `GET /api/auth/me`: Retrieve the currently authenticated user's details.

## Check Requests
Endpoints for managing inspection requests from the Contractor.
- `GET /api/check-requests`: List all check requests.
- `POST /api/check-requests`: Create a new check request (Contractor only).
- `GET /api/check-requests/{cr_id}`: Get details of a specific check request.
- `POST /api/check-requests/{cr_id}/evidence`: Upload evidence (files/images) for a check request.
- `POST /api/check-requests/{cr_id}/submit`: Submit a check request for inspection.

## Inspections
Endpoints for the Resident Engineer to conduct inspections and record observations.
- `POST /api/inspections/start/{cr_id}`: Start an inspection for a check request.
- `GET /api/inspections/{inspection_id}`: Get details of an inspection.
- `POST /api/inspections/{inspection_id}/ai-draft`: Generate an AI-assisted observation draft.
- `POST /api/inspections/{inspection_id}/observations`: Add an observation to the inspection.
- `POST /api/inspections/{inspection_id}/decide`: Make a final decision (accept/reject) on the inspection.

## Approvals
Endpoints for quantity approvals after a successful inspection.
- `GET /api/approvals`: List all quantity approvals.
- `POST /api/approvals/re`: Resident Engineer approves submitted quantities.

## IPC (Interim Payment Certificate)
Endpoints for generating and managing payment certificates.
- `GET /api/ipc/eligible`: Check eligibility summary for generating a new IPC.
- `GET /api/ipc`: List all generated IPCs.
- `GET /api/ipc/{ipc_id}`: Get details of a specific IPC.
- `POST /api/ipc/generate`: Generate a new IPC from eligible approved quantities (Client or RE).
