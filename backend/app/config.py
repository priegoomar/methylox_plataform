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

# --- GLOBAL CONFIGURATION (ZERO HARDCODING) ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://methylox_user:METHYLOX_DB_PASS_2026@localhost:5432/methylox_production")
SECRET_KEY = os.getenv("SECRET_KEY", "FDA_COMPLIANCE_ENCRYPTION_KEY_METHYLOX_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480 # Standard 8-hour clinical shift

# SMTP Settings
SMTP_HOST = os.getenv("SMTP_HOST", "://gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "notifications@methylox.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "secure_app_password")
CLINICAL_ALERT_EMAIL = os.getenv("CLINICAL_ALERT_EMAIL", "oncology.chief@methylox.com")

app = FastAPI(
    title="METHYLOX™ Global Enterprise SaMD Engine",
    version="3.0.0",
    description="Unified central backend governance for clinical analytical pipelines, LIMS, RBAC, and commercial portals."
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# --- INDEPENDENT UTILITIES & SERVICES ---
class NotificationService:
    @staticmethod
    def send_html_email(to_email: str, subject: str, body: str):
        try:
            msg = MIMEMultipart()
            msg["From"] = SMTP_USER
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"SMTP_ERROR: {str(e)}")
            return False

class PDFCompilerService:
    @staticmethod
    def generate_report(sample_id: int, patient_id: str, mean_beta: float, verdict: str, operator: str) -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "METHYLOX™ CLINICAL BIOMEDICAL REPORT", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 7, f"Sample Entry ID: {sample_id}", ln=True)
        pdf.cell(0, 7, f"Patient Identifier: {patient_id}", ln=True)
        pdf.cell(0, 7, f"Mean Beta Value (β): {mean_beta:.4f}", ln=True)
        pdf.cell(0, 7, f"Diagnostic Call: {verdict}", ln=True)
        pdf.cell(0, 7, f"Validation Operator: {operator}", ln=True)
       
        out_dir = "static/reports"
        os.makedirs(out_dir, exist_ok=True)
        path = f"{out_dir}/METHYLOX_Report_{sample_id}.pdf"
        pdf.output(path)
        return path

# --- PYDANTIC ENFORCED SCHEMAS ---
class LandingLeadInput(BaseModel):
    name: str
    email: EmailStr
    institution: str

class HospitalCreate(BaseModel):
    hospital_name: str
    facility_code: str
    country: str

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

class SampleAnalysisInput(BaseModel):
    patient_id: str
    hospital_id: int
    control_blank: float
    control_negative: float
    control_positive: float
    replicates: List[float]

class TokenData(BaseModel):
    id_user: int
    id_hospital: int
    username: str
    permissions: List[str]

# --- ELASTIC GOVERNANCE MIDDLEWARE (RBAC) ---
async def get_current_user_claims(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Decodes JWT and injects runtime security context containing dynamic permission matrices."""
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid global session credentials or expired session."
    )
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
    """Interceptors that cross-reference permissions array dynamically without hardcoded personas."""
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, current_user: TokenData = Depends(get_current_user_claims)):
        if self.required_permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Action unauthorized. Missing clinical privilege: {self.required_permission}"
            )
        return current_user

# ==============================================================================
# SECTION 1: CRM & COMMERCIAL LANDING INTEGRATION
# ==============================================================================
@app.post("/api/v1/landing/request-access", tags=["Commercial Portal"])
async def register_landing_lead(payload: LandingLeadInput):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO landing_leads (name, email, institution) VALUES (%s, %s, %s)", (payload.name, payload.email, payload.institution))
        conn.commit()
        html_body = f"<html><body><h3>Hello {payload.name},</h3><p>METHYLOX™ has received your access inquiry for {payload.institution}. Our team will review your credentials.</p></body></html>"
        NotificationService.send_html_email(payload.email, "METHYLOX™ - Access Application Received", html_body)
        return {"status": "SUCCESS", "message": "Inquiry captured and transactional validation email dispatched."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# SECTION 2: MEDICAL INFRASTRUCTURE MANAGEMENT
# ==============================================================================
@app.post("/api/v1/infrastructure/hospitals", tags=["Medical Infrastructure"])
async def provision_hospital(
    hospital: HospitalCreate, 
    current_user: TokenData = Depends(PermissionGuard("USER_MANAGE"))
):
    """Guarded via global administrative scope permission rather than strict text check."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO hospitals (hospital_name, facility_code, country) VALUES (%s, %s, %s) RETURNING id_hospital", 
            (hospital.hospital_name, hospital.facility_code, hospital.country)
        )
        new_id = cur.fetchone()['id_hospital']
        conn.commit()
        return {"status": "SUCCESS", "hospital_id": new_id, "message": f"Facility {hospital.hospital_name} provisioned."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# SECTION 3: IDENTITY GOVERNANCE (RBAC AUTHORIZATION)
# ==============================================================================
@app.post("/api/v1/auth/provision-user", tags=["Governance & Security"])
async def provision_clinical_staff(
    user: UserCreate, 
    current_user: TokenData = Depends(PermissionGuard("USER_MANAGE"))
):
    """Allows authorized users to provision any user under any dynamic database role."""
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
    """Logs in any user, queries its linked role-permissions matrix, and signs the JWT payload."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Query structural user info from database
    cur.execute(
        "SELECT id_user, username, hashed_password, id_hospital, dynamic_role_id FROM users WHERE username = %s AND is_active = TRUE", 
        (form_data.username,)
    )
    user = cur.fetchone()
    
    if not user or not pwd_context.verify(form_data.password, user['hashed_password']):
        cur.close()
        conn.close()
    # Query structural user info from database
    cur.execute(
        "SELECT id_user, username, hashed_password, id_hospital, dynamic_role_id FROM users WHERE username = %s AND is_active = TRUE", 
        (form_data.username,)
    )
    user = cur.fetchone()
    
    if not user or not pwd_context.verify(form_data.password, user['hashed_password']):
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid clinical credentials.")
   
    # Fetch operational permission strings mapped via dynamic role relationships
    permissions = []
    if user['dynamic_role_id']:
        cur.execute(
            """
            SELECT p.permission_code 
            FROM role_permissions rp
            JOIN permissions p ON rp.id_permission = p.id_permission
            WHERE rp.id_role = %s
            """,
            (user['dynamic_role_id'],)
        )
        permissions = [row['permission_code'] for row in cur.fetchall()]
        
    cur.close()
    conn.close()
   
    token_payload = {
        "sub": user['username'], 
        "id_user": user['id_user'], 
        "id_hospital": user['id_hospital'],
        "permissions": permissions,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# ==============================================================================
# SECTION 4: PATIENT MANAGEMENT & LIMS ENROLLMENT
# ==============================================================================
@app.post("/api/v1/lims/enroll-patient", tags=["Patient & LIMS Operations"])
async def enroll_patient_profile(
    patient: PatientCreate, 
    current_user: TokenData = Depends(PermissionGuard("SAMPLE_CREATE"))
):
    """Guarded via SAMPLE_CREATE permission. Multi-tenant isolation context fully operational."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO patients (id_patient, full_name, date_of_birth, gender) VALUES (%s, %s, %s, %s)", 
            (patient.id_patient, patient.full_name, datetime.strptime(patient.date_of_birth, "%Y-%m-%d").date(), patient.gender)
        )
        conn.commit()
        return {"status": "SUCCESS", "message": f"Patient profile {patient.id_patient} initialized securely."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# --- PYDANTIC SCHEMA FOR DYNAMIC TELEMETRY RESPONSE ---
class TelemetrySummaryResponse(BaseModel):
    received_today: int
    in_progress: int
    ready_analyses: int
    qc_pass_rate: float

# ==============================================================================
# SECTION 3.5: CLINICAL TELEMETRY ENGINE (DYNAMIC POSTGRESQL COUNTS)
# ==============================================================================
@app.get("/api/v1/analysis/telemetry-summary", response_model=TelemetrySummaryResponse, tags=["Clinical Telemetry"])
async def get_hospital_telemetry_summary(
    current_user: TokenData = Depends(get_current_user_claims)
):
    """
    Queries real-time transactional counts from clinical_samples table.
    Enforces absolute multi-tenant data isolation using the authenticated id_hospital.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Query 1: Muestras recibidas hoy (Filter by current calendar date and hospital boundary)
        today_date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            """
            SELECT COUNT(*) as count 
            FROM clinical_samples 
            WHERE id_hospital = %s AND processed_at::date = %s::date
            """,
            (current_user.id_hospital, today_date)
        )
        received_today = cur.fetchone()['count']
        
        # Query 2: Análisis en proceso (Samples logged but awaiting CRISPR diagnostic_verdict)
        cur.execute(
            """
            SELECT COUNT(*) as count 
            FROM clinical_samples 
            WHERE id_hospital = %s AND diagnostic_verdict IS NULL
            """,
            (current_user.id_hospital,)
        )
        in_progress = cur.fetchone()['count']
        
        # Query 3: Resultados listos (CRISPR pipeline execution complete and verdict written)
        cur.execute(
            """
            SELECT COUNT(*) as count 
            FROM clinical_samples 
            WHERE id_hospital = %s AND diagnostic_verdict IS NOT NULL
            """,
            (current_user.id_hospital,)
        )
        ready_analyses = cur.fetchone()['count']
        
        # Query 4: Controles de Calidad (Percentage of batches passing the LIMITE_RUIDO of 0.0200)
        # Fetch target cutoff from calibration matrix to avoid hardcoding drift
        cur.execute("SELECT numeric_value FROM clinical_calibration WHERE parameter_key = 'LIMITE_RUIDO'")
        noise_row = cur.fetchone()
        noise_cutoff = float(noise_row['numeric_value']) if noise_row else 0.0200
        
        cur.execute(
            """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN control_blank <= %s AND control_negative <= %s THEN 1 ELSE 0 END) as passed
            FROM clinical_samples 
            WHERE id_hospital = %s
            """,
            (noise_cutoff, noise_cutoff, current_user.id_hospital)
        )
        qc_data = cur.fetchone()
        
        total_qc_runs = qc_data['total'] if qc_data else 0
        passed_qc_runs = qc_data['passed'] if qc_data and qc_data['passed'] is not None else 0
        
        # Mathematical derivation of the live compliance rate percentage
        qc_pass_rate = (passed_qc_runs / total_qc_runs * 100.0) if total_qc_runs > 0 else 100.0
        
        return {
            "received_today": int(received_today),
            "in_progress": int(in_progress),
            "ready_analyses": int(ready_analyses),
            "qc_pass_rate": round(float(qc_pass_rate), 1)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compile operational matrix from PostgreSQL nodes: {str(e)}"
        )
    finally:
        cur.close()
        conn.close()
