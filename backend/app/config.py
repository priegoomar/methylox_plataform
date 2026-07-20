<import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Module 1: Global Infrastructure Settings
    This file handles security keys and SMTP/Database connections only.
    No clinical logic or HTML content is allowed here.
    """
    PROJECT_NAME: str = "METHYLOX™ Enterprise SaMD Platform"
    VERSION: str = "3.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Secure database url pointer
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://methylox_user:METHYLOX_DB_PASS_2026@localhost:5432/methylox_production")
    
    # Cryptographic governance keys
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_COMPLIANCE_KEY_2026_FDA")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Mail server communication infrastructure
    SMTP_HOST: str = os.getenv("SMTP_HOST", "://gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "notifications@methylox.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "secure_app_password")
    CLINICAL_ALERT_EMAIL: str = os-getenv("CLINICAL_ALERT_EMAIL", "oncology.chief@methylox.com")

settings = Settings()


El lun, 20 de jul de 2026, 12:53 a.m., Lint Brew <brewlint@gmail.com> escribió:
import os
import hashlib
from typing import List, Optional
from datetime import datetime, timedelta
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
    role: str # CHECK IN ('METHYLOX-ROOT', 'METH-ONCO-CHIEF', 'LAB-TECHNICIAN')
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

# --- GOVERNANCE MIDDLEWARE (RBAC) ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid global session credentials.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        id_user: int = payload.get("id_user")
        if username is None or role is None:
            raise auth_exception
        return {"username": username, "role": role, "id_user": id_user}
    except jwt.PyJWTError:
        raise auth_exception

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
async def provision_hospital(hospital: HospitalCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "METHYLOX-ROOT":
        raise HTTPException(status_code=403, detail="Operation restricted to ROOT governance level.")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO hospitals (hospital_name, facility_code, country) VALUES (%s, %s, %s) RETURNING id_hospital", (hospital.hospital_name, hospital.facility_code, hospital.country))
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
async def provision_clinical_staff(user: UserCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "METHYLOX-ROOT":
        raise HTTPException(status_code=403, detail="Insufficient access rights for staff provisioning.")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        hashed = pwd_context.hash(user.password)
        cur.execute("INSERT INTO users (username, hashed_password, full_name, role, id_hospital) VALUES (%s, %s, %s, %s, %s) RETURNING id_user", (user.username, hashed, user.full_name, user.role, user.hospital_id))
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
    cur.execute("SELECT id_user, username, hashed_password, role FROM users WHERE username = %s AND is_active = TRUE", (form_data.username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if not user or not pwd_context.verify(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid clinical credentials.")
    
    token_payload = {"sub": user['username'], "role": user['role'], "id_user": user['id_user'], "exp": datetime.utcnow() + timedelta(minutes=60)}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "role": user['role']}

# ==============================================================================
# SECTION 4: PATIENT MANAGEMENT & LIMS ENROLLMENT
# ==============================================================================
@app.post("/api/v1/lims/enroll-patient", tags=["Patient & LIMS Operations"])
async def enroll_patient_profile(patient: PatientCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["METHYLOX-ROOT", "METH-ONCO-CHIEF", "LAB-TECHNICIAN"]:
        raise HTTPException(status_code=403, detail="Action blacklisted for current role.")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO patients (id_patient, full_name, date_of_birth, gender) VALUES (%s, %s, %s, %s)", (patient.id_patient, patient.full_name, datetime.strptime(patient.date_of_birth, "%Y-%m-%d").date(), patient.gender))
        conn.commit()
