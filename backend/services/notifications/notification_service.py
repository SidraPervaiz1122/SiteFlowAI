from typing import Optional, List
from sqlalchemy.orm import Session
from backend.models.notification import Notification
from backend.models.user import User
from backend.core.enums import UserRole

def notify_user(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    link: Optional[str] = None,
    commit: bool = False
) -> Notification:
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        link=link
    )
    db.add(notif)
    if commit:
        db.commit()
    return notif

def notify_role(
    db: Session,
    role: UserRole,
    title: str,
    message: str,
    link: Optional[str] = None,
    commit: bool = False
) -> List[Notification]:
    users = db.query(User).filter(User.role == role.value, User.is_active == 1).all()
    created = []
    for u in users:
        notif = notify_user(db, u.id, title, message, link, commit=False)
        created.append(notif)
    if commit:
        db.commit()
    return created
