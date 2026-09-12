import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import settings
from backend.app.database import engine, Base
import backend.models # Ensure all models are registered
from backend.api.router import api_router
from backend.core.exceptions import SiteFlowException

# Initialize database schema
Base.metadata.create_all(bind=engine)

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
