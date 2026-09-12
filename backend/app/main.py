import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
import backend.models # Ensure all models are registered
from backend.api.router import api_router
from backend.core.exceptions import SiteFlowException
from backend.models.user import User
from backend.db.seed import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Idempotently seed database on startup
try:
    db = SessionLocal()
    if not db.query(User).first():
        logger.info("No users found in database. Running automatic seed script...")
        seed_database(reset=False)
        logger.info("Automatic seed script completed.")
    else:
        logger.info("Database already seeded. Skipping auto-seed.")
except Exception as e:
    logger.error(f"Error during automatic database seeding: {e}")
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Construction Inspection, Approval & IPC Management Platform",
    version="1.0.0"
)

# Enable CORS for local Vite development and testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global custom exception handling for domain errors
@app.exception_handler(SiteFlowException)
async def siteflow_exception_handler(request: Request, exc: SiteFlowException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details
        }
    )

# Static file serving for uploaded evidence and documents
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
app.mount("/storage/uploads", StaticFiles(directory=settings.UPLOADS_DIR), name="uploads")

# Mount API routers
app.include_router(api_router)

# Serve the built React frontend (single-service deployment)
FRONTEND_DIST = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist'))
if os.path.isdir(FRONTEND_DIST):
    app.mount('/', StaticFiles(directory=FRONTEND_DIST, html=True), name='frontend')


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SiteFlow AI API",
        "version": "1.0.0",
        "contract_total_pkr": "5,135,535.00"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)