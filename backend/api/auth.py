from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.schemas.auth import UserLoginRequest, UserQuickLoginRequest, TokenResponse, UserResponse
from backend.services.auth.auth_service import authenticate_user, authenticate_by_role, create_access_token
from backend.app.dependencies import get_current_user
from backend.models.user import User
from backend.services.audit.audit_service import record_audit
from backend.core.enums import AuditAction

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, req.email, req.password)
    token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    record_audit(db, user, AuditAction.AUTH_LOGIN.value, "USER", str(user.id), commit=True)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.post("/quick-switch", response_model=TokenResponse)
def quick_switch(req: UserQuickLoginRequest, db: Session = Depends(get_db)):
    """Convenience for hackathon demonstration: signs in as real seeded account."""
    user = authenticate_by_role(db, req.role)
    token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    record_audit(db, user, AuditAction.AUTH_LOGIN.value, "USER", str(user.id), metadata={"quick_switch": True}, commit=True)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
