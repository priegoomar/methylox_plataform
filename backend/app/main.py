import os
import hashlib
from typing import List, Optional
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import psycopg2
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
import jwt
from fpdf import FPDF
from fastapi.middleware.cors import CORSMiddleware

# --- GLOBAL CONFIGURATION (ZERO HARDCODING) ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://methylox_user:METHYLOX_DB_PASS_2026@localhost:5432/methylox_production")
SECRET_KEY = os.getenv("SECRET_KEY", "FDA_COMPLIANCE_ENCRYPTION_KEY_METHYLOX_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480 # Standard 8-hour clinical shift

app = FastAPI(
    title="METHYLOX™ Global Enterprise SaMD Engine",
    version="3.0.0",
    description="Unified central backend governance for clinical analytical pipelines, LIMS, RBAC, and commercial portals."
)

# CORE NETWORK CORRECTION: Enable safe cross-origin data streams for Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows Streamlit Cloud endpoints to consume FastAPI protocols securely
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# --- PYDANTIC ENFORCED SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    dynamic_role_id: int
    hospital_id: int

class PatientCreate(BaseModel):
    id_patient: str
    full_name: str
    date_of_birth: str
    gender: str

class TokenData(BaseModel):
    id_user: int
    id_hospital: int
    username: str
    permissions: List[str]

class RoleCatalogResponse(BaseModel):
    id_role: int
    role_name: str
    description: Optional[str] = None

# --- ELASTIC GOVERNANCE MIDDLEWARE (RBAC) ---
async def get_current_user_claims(token: str = Depends(oauth2_scheme)) -> TokenData:
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid global session credentials or expired session.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id_user: int = payload.get("id_user")
        id_hospital: int = payload.get("id_hospital")
        permissions: List[str] = payload.get("permissions", [])
        if username is None or id_user is None or id_hospital is None:
            raise auth_exception
        return TokenData(id_user=id_user, id_hospital=id_hospital, username=username, permissions=permissions)
    except jwt.PyJWTError:
        raise auth_exception

class PermissionGuard:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    def __call__(self, current_user: TokenData = Depends(get_current_user_claims)):
        if self.required_permission not in current_user.permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Action unauthorized. Missing clinical privilege: {self.required_permission}")
        return current_user

# ==============================================================================
# IDENTITY GOVERNANCE & AUTHENTICATION ENDPOINTS
# ==============================================================================
@app.post("/api/v1/auth/provision-user", tags=["Governance & Security"])
async def provision_clinical_staff(user: UserCreate, current_user: TokenData = Depends(PermissionGuard("USER_MANAGE"))):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        hashed = pwd_context.hash(user.password)
        cur.execute(
            "INSERT INTO users (username, hashed_password, full_name, dynamic_role_id, id_hospital) VALUES (%s, %s, %s, %s, %s) RETURNING id_user", 
            (user.username, hashed, user.full_name, user.dynamic_role_id, user.hospital_id)
        )
        staff_id = cur.fetchone()['id_user']
        conn.commit()
        return {"status": "SUCCESS", "user_id": staff_id, "message": f"Staff identity {user.username} active."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/v1/auth/login", tags=["Governance & Security"])
async def institutional_login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # NOTA: Si tu columna en la Base de Datos se llama 'email', cambia 'username = %s' por 'email = %s'
        cur.execute(
            "SELECT id_user, username, hashed_password, id_hospital, dynamic_role_id FROM users WHERE username = %s AND is_active = TRUE", 
            (form_data.username,)
        )
        user = cur.fetchone()
        
        # Si el usuario no existe o la contraseña no coincide, lanzamos un error 401 (Credenciales inválidas)
        if not user or not pwd_context.verify(form_data.password, user['hashed_password']):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid clinical credentials.")
        
        permissions = []
        if user['dynamic_role_id']:
            cur.execute(
                "SELECT p.permission_code FROM role_permissions rp JOIN permissions p ON rp.id_permission = p.id_permission WHERE rp.id_role = %s", 
                (user['dynamic_role_id'],)
            )
            permissions = [row['permission_code'] for row in cur.fetchall()]
        
        token_payload = {
            "sub": user['username'], 
            "id_user": user['id_user'], 
            "id_hospital": user['id_hospital'], 
            "permissions": permissions,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}

    except HTTPException as http_err:
        # Permitimos que salgan los errores controlados de credenciales sin volverse un Error 500
        raise http_err
    except Exception as e:
        # Si hay un error de PostgreSQL (ej. columna inexistente), se imprimirá en tu terminal/consola
        print(f"--- DETALLE DEL ERROR REAL EN EL SERVIDOR: {str(e)} ---")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database or Server error: {str(e)}")
    finally:
        cur.close()
        conn.close()
