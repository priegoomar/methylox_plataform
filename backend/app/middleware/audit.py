from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.database import SessionLocal
from app import models

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Endpoints que no queremos registrar
        ignored_paths = {
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/api/v1/health",
            "/api/v1/audit/",
        }

        # Ejecutar normalmente la petición
        response = await call_next(request)

        # No registrar endpoints ignorados
        if request.url.path in ignored_paths:
            return response

        # Intentar obtener información del usuario desde el JWT
        user_id = None
        hospital_id = None

        try:
            auth_header = request.headers.get("Authorization")

            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.replace("Bearer ", "", 1)

                from app.config import settings
                import jwt

                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM]
                )

                user_id = payload.get("id_user")
                hospital_id = payload.get("id_hospital")

        except Exception:
            # Si no se puede identificar al usuario,
            # no interrumpimos la petición original.
            pass

        # Obtener IP del cliente
        client_ip = request.client.host if request.client else None

        # Crear registro de auditoría
        db = SessionLocal()

        try:
            audit_log = models.AuditLog(
                user_id=user_id,
                hospital_id=hospital_id,
                action="HTTP_REQUEST",
                module="system",
                entity=request.url.path,
                changes=None,
                ip_address=client_ip,
                endpoint=request.url.path,
                http_method=request.method,
                status_code=response.status_code
            )

            db.add(audit_log)
            db.commit()

        except Exception:
            db.rollback()

        finally:
            db.close()

        return response
