from fastapi import APIRouter
from backend.api.auth import router as auth_router
from backend.api.projects import router as projects_router
from backend.api.boq import router as boq_router
from backend.api.check_requests import router as check_requests_router
from backend.api.inspections import router as inspections_router
from backend.api.quantities import router as quantities_router
from backend.api.approvals import router as approvals_router
from backend.api.client_reviews import router as client_reviews_router
from backend.api.ipc import router as ipc_router
from backend.api.documents import router as documents_router
from backend.api.notifications import router as notifications_router
from backend.api.audit import router as audit_router
from backend.api.ai import router as ai_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(projects_router)
api_router.include_router(boq_router)
api_router.include_router(check_requests_router)
api_router.include_router(inspections_router)
api_router.include_router(quantities_router)
api_router.include_router(approvals_router)
api_router.include_router(client_reviews_router)
api_router.include_router(ipc_router)
api_router.include_router(documents_router)
api_router.include_router(notifications_router)
api_router.include_router(audit_router)
api_router.include_router(ai_router)
