from sqlalchemy.orm import Session
from app.models import AuditLog


def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    module: str,
    entity: str | None = None,
    changes: dict | None = None,
    hospital_id: int | None = None,
    ip_address: str | None = None,
    endpoint: str | None = None,
    http_method: str | None = None,
    status_code: int | None = None,
):
    """
    Creates a complete METHYLOX audit trail record.

    Records:
    - User
    - Hospital
    - Action
    - Module
    - Entity
    - Changes
    - IP address
    - API endpoint
    - HTTP method
    - HTTP status code
    """
    log = AuditLog(
        user_id=user_id,
        hospital_id=hospital_id,
        action=action,
        module=module,
        entity=entity,
        changes=changes,
        ip_address=ip_address,
        endpoint=endpoint,
        http_method=http_method,
        status_code=status_code,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
