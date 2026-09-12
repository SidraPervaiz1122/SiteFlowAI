from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.database import get_db
from backend.models.user import User
from backend.core.exceptions import UnauthorizedException, ForbiddenException
from backend.core.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user

def require_contractor_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.CONTRACTOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only Contractor can perform this action (current: {current_user.role})"
        )
    return current_user

def require_re_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.RE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only Resident Engineer (RE) can perform this action (current: {current_user.role})"
        )
    return current_user

def require_client_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.CLIENT.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Only Client can perform this action (current: {current_user.role})"
        )
    return current_user

def require_re_or_client_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.RE.value, UserRole.CLIENT.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only RE or Client can perform this action"
        )
    return current_user
