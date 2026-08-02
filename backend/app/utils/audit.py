from sqlalchemy.orm import Session
from app.models import AuditLog


def create_audit_log(db: Session, user_id: int | None, action: str, module: str, entity: str | None = None, changes: dict | None = None):
    log = AuditLog(user_id=user_id, action=action, module=module, entity=entity, changes=changes)
    db.add(log)
    db.commit()
    return log
