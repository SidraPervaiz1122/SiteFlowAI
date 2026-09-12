import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.dependencies import get_current_user
from backend.models.user import User
from backend.models.document import Document
from backend.schemas.document import DocumentResponse
from backend.app.config import settings

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("", response_model=List[DocumentResponse])
def list_documents(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Document).order_by(Document.created_at.desc())
    if category:
        query = query.filter(Document.category == category)
    return [DocumentResponse.model_validate(d) for d in query.all()]

@router.post("", response_model=DocumentResponse)
def upload_document(
    title: str = Form(...),
    category: str = Form("GENERAL"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    safe_name = f"DOC_{os.path.basename(file.filename)}"
    dest = os.path.join(settings.DOCUMENTS_DIR, safe_name)
    with open(dest, "wb") as buf:
        shutil.copyfileobj(file.file, buf)

    size = os.path.getsize(dest)
    doc = Document(
        project_id=1,
        title=title,
        category=category,
        filename=file.filename,
        file_path=dest,
        file_type=file.content_type or "application/octet-stream",
        file_size_bytes=size,
        uploaded_by_id=current_user.id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return DocumentResponse.model_validate(doc)
