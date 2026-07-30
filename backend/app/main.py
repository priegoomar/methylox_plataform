# ==============================================================================
# METHYLOX™ GLOBAL ENTERPRISE SaMD ENGINE
# backend/app/main.py
# VERSION 3.0.1 - Backend Harmonized Edition
# ==============================================================================

import csv
import io
import random
from datetime import datetime, timezone, timedelta
from typing import List

import jwt
import psycopg2
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, EmailStr

from app.config import settings

# ==============================================================================
# APPLICATION CORE
# ==============================================================================

app = FastAPI(
    title="METHYLOX™ Global Enterprise SaMD Engine",
    version="3.0.1",
    description="Clinical molecular intelligence backend integrating LIMS, RBAC, epigenetic analytics and reporting."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# ==============================================================================
# DATABASE CONNECTION
# ==============================================================================

def get_db_connection():
    try:
        return psycopg2.connect(settings.DATABASE_URL, cursor_factory=RealDictCursor)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# ==============================================================================
# PYDANTIC MODELS
# ==============================================================================

class TokenData(BaseModel):
    id_user: int
    id_hospital: int
    username: str
    role: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class PatientCreate(BaseModel):
    id_patient: str
    full_name: str
    date_of_birth: str
    gender: str
    hospital_id: int

class UserProvision(BaseModel):
    username: EmailStr
    password: str
    full_name: str
    role: str
    hospital_id: int

class SampleCreate(BaseModel):
    sample_id: str
    patient_id: str
    barcode_qr: str
    specimen_type: str

class TelemetrySummaryResponse(BaseModel):
    received_today: int
    in_progress: int
    ready_analyses: int
    qc_pass_rate: float

# ==============================================================================
# SECURITY JWT
# ==============================================================================

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user_claims(token: str = Depends(oauth2_scheme)) -> TokenData:
    auth_exception = HTTPException(status_code=401, detail="Invalid session credentials.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username, id_user, id_hospital, role = (
            payload.get("sub"),
            payload.get("id_user"),
            payload.get("id_hospital"),
            payload.get("role")
        )
        if None in (username, id_user, id_hospital, role):
            raise auth_exception
        return TokenData(id_user=id_user, id_hospital=id_hospital, username=username, role=role)
    except jwt.PyJWTError:
        raise auth_exception

class RoleGuard:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: TokenData = Depends(get_current_user_claims)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions.")
        return current_user

# ==============================================================================
# AUTHENTICATION
# ==============================================================================

@app.post("/api/v1/auth/login", response_model=LoginResponse, tags=["Authentication"])
async def login_user(payload: dict):
    username = payload.get("username")
    password = payload.get("password")
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        
        if not user or not pwd_context.verify(password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials.")
            
        token = create_access_token({
            "sub": user["username"],
            "id_user": user["id"],
            "id_hospital": user["hospital_id"],
            "role": user["role"]
        })
        return {"access_token": token, "token_type": "bearer"}
    finally:
        cur.close()
        conn.close()

@app.post("/api/v1/auth/provision-user", tags=["Authentication"])
async def provision_user(user: UserProvision, current_user: TokenData = Depends(RoleGuard(["admin"]))):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        password_hash = pwd_context.hash(user.password)
        cur.execute(
            """
            INSERT INTO users (username, full_name, password_hash, role, hospital_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user.username, user.full_name, password_hash, user.role, user.hospital_id)
        )
        conn.commit()
        return {"status": "SUCCESS", "message": "User activated."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# HOSPITAL DIRECTORY
# ==============================================================================

@app.get("/api/v1/hospitals/directory", tags=["LIMS Operations"])
async def get_hospitals_directory(current_user: TokenData = Depends(get_current_user_claims)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, clinical_code FROM hospitals ORDER BY name")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# PATIENT MANAGEMENT
# ==============================================================================

@app.post("/api/v1/lims/enroll-patient", tags=["LIMS Operations"])
async def enroll_patient_profile(patient: PatientCreate, current_user: TokenData = Depends(RoleGuard(["admin", "md"]))):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO patients (id_patient, full_name, date_of_birth, gender, hospital_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                patient.id_patient,
                patient.full_name,
                datetime.strptime(patient.date_of_birth, "%Y-%m-%d").date(),
                patient.gender,
                current_user.id_hospital
            )
        )
        conn.commit()
        return {"status": "SUCCESS", "message": "Patient profile created."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# PATIENT COHORT DIRECTORY
# ==============================================================================

@app.get("/api/v1/lims/cohort-directory", tags=["LIMS Operations"])
async def get_cohort_directory(current_user: TokenData = Depends(get_current_user_claims)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT p.id_patient AS patient_id, p.full_name AS anonymous_code,
                   EXTRACT(YEAR FROM AGE(p.date_of_birth))::int AS age,
                   p.gender AS sexo, h.name AS institucion
            FROM patients p
            JOIN hospitals h ON p.hospital_id = h.id
            WHERE p.hospital_id = %s
            """,
            (current_user.id_hospital,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# LIMS SAMPLE DIRECTORY
# ==============================================================================

@app.get("/api/v1/lims/samples/directory", tags=["LIMS Operations"])
async def get_samples_directory(current_user: TokenData = Depends(get_current_user_claims)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT sample_id, patient_id, barcode_qr, specimen_type, workflow_state
            FROM samples WHERE hospital_id = %s ORDER BY created_at DESC
            """,
            (current_user.id_hospital,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

@app.get("/api/v1/lims/samples/pending-evaluation", tags=["METHYLOX Engine"])
async def pending_samples(current_user: TokenData = Depends(get_current_user_claims)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT sample_id FROM samples
            WHERE hospital_id = %s AND workflow_state != 'Clinical Report Compiled'
            """,
            (current_user.id_hospital,)
        )
        return [x["sample_id"] for x in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# SAMPLE INTAKE
# ==============================================================================

@app.post("/api/v1/lims/samples/intake", tags=["LIMS Operations"])
async def sample_intake(sample: SampleCreate, current_user: TokenData = Depends(RoleGuard(["admin", "cls"]))):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO samples (sample_id, patient_id, barcode_qr, specimen_type, workflow_state, hospital_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (sample.sample_id, sample.patient_id, sample.barcode_qr, sample.specimen_type, "Sample Registered", current_user.id_hospital)
        )
        conn.commit()
        return {"status": "SUCCESS", "message": "Sample synchronized."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# METHYLOX COMPUTATIONAL ENGINE
# ==============================================================================

@app.post("/api/v1/lims/samples/evaluate/{sample_id}", tags=["METHYLOX Engine Core"])
async def evaluate_methylox_pipeline(
    sample_id: str,
    file: UploadFile = File(...),
    current_user: TokenData = Depends(RoleGuard(["admin", "cls"]))
):
    contents = await file.read()
    reader = csv.DictReader(io.StringIO(contents.decode("utf-8")))
    
    beta_values = []
    for row in reader:
        if "Methylated_Intensity" in row and "Unmethylated_Intensity" in row:
            m = float(row["Methylated_Intensity"])
            u = float(row["Unmethylated_Intensity"])
            beta_values.append(m / (m + u + 100))
            
    if not beta_values:
        raise HTTPException(status_code=400, detail="Invalid methylation file.")
        
    mean_beta = sum(beta_values) / len(beta_values)
    verdict = (
        "Epigenetic profile compatible with METHYLOX tumor panel"
        if mean_beta >= 0.1000
        else "Stable Baseline Control Range"
    )
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE samples SET workflow_state = 'Clinical Report Compiled' WHERE sample_id = %s",
            (sample_id,)
        )
        security_hash = f"HSH-{random.randint(10000, 99999)}"
        cur.execute(
            """
            INSERT INTO reports (muestra_id, paciente_id, score, clasificacion, operador, hash_seguridad)
            VALUES (%s, (SELECT patient_id FROM samples WHERE sample_id = %s), %s, %s, %s, %s)
            """,
            (sample_id, sample_id, mean_beta, verdict, current_user.username, security_hash)
        )
        conn.commit()
        return {"status": "SUCCESS", "mean_beta": mean_beta, "verdict": verdict}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# REPORT DIRECTORY
# ==============================================================================

@app.get("/api/v1/analysis/reports-directory", tags=["Reports"])
async def reports_directory(current_user: TokenData = Depends(get_current_user_claims)):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT r.muestra_id, r.paciente_id, p.full_name AS nombre_codigo,
                   r.score, r.clasificacion, r.operador, r.hash_seguridad,
                   TO_CHAR(r.created_at, 'YYYY-MM-DD HH24:MI') AS fecha_analisis,
                   p.date_of_birth, p.gender AS sexo, h.name AS institucion
            FROM reports r
            JOIN samples s ON r.muestra_id = s.sample_id
            JOIN patients p ON s.patient_id = p.id_patient
            JOIN hospitals h ON p.hospital_id = h.id
            WHERE h.id = %s
            """,
            (current_user.id_hospital,)
        )
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# ==============================================================================
# HEALTH CHECK
# ==============================================================================

@app.get("/api/v1/health", tags=["System"])
async def health():
    return {
        "status": "ONLINE",
        "engine": "METHYLOX v3.0.1",
        "timestamp": datetime.now(timezone.utc)
    }
