-- 1. Table for Dynamic Calibration Parameters (No more hardcoded 0.02 or 0.1000)
CREATE TABLE clinical_calibration (
    parameter_key VARCHAR(50) PRIMARY KEY,
    numeric_value DOUBLE PRECISION,
    text_value VARCHAR(100),
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table for Enterprise Medical Infrastructure (No more hardcoded Hospitals)
CREATE TABLE hospitals (
    id_hospital SERIAL PRIMARY KEY,
    hospital_name VARCHAR(150) NOT NULL,
    facility_code VARCHAR(50) UNIQUE NOT NULL,
    country VARCHAR(50) DEFAULT 'USA'
);

-- 3. Table for Real User Management and RBAC Roles (No more exposed keys)
CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(30) NOT NULL CHECK (role IN ('METHYLOX-ROOT', 'METH-ONCO-CHIEF', 'LAB-TECHNICIAN')),
    id_hospital INT REFERENCES hospitals(id_hospital),
    is_active BOOLEAN DEFAULT TRUE
);

-- 4. Table for Patient Demographics
CREATE TABLE patients (
    id_patient VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL
);

-- 5. Table for Clinical Samples and Real-time Multiplexed Replicates
CREATE TABLE clinical_samples (
    id_sample SERIAL PRIMARY KEY,
    id_hospital INT REFERENCES hospitals(id_hospital),
    id_patient VARCHAR(50) REFERENCES patients(id_patient),
    barcode_qr VARCHAR(100) UNIQUE,
    specimen_type VARCHAR(50),
    control_blank DOUBLE PRECISION,
    control_negative DOUBLE PRECISION,
    control_positive DOUBLE PRECISION,
    replicate_1 DOUBLE PRECISION,
    replicate_2 DOUBLE PRECISION,
    replicate_3 DOUBLE PRECISION,
    calculated_mean_beta DOUBLE PRECISION,
    diagnostic_verdict VARCHAR(100),
    practitioner_signature VARCHAR(100),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INJECT MASTER OPERATIONAL METADATA
INSERT INTO clinical_calibration (parameter_key, numeric_value, text_value, description) VALUES
('UMBRAL_YOUDEN', 0.1000, NULL, 'Optimal cutoff point for breast cancer positivity calling.'),
('LIMITE_RUIDO', 0.0200, NULL, 'Maximum fluorescence noise allowed for Blank and Negative controls.'),
('CONSTANTE_FONDO', 100.0000, NULL, 'Illumina baseline laser correction constant.'),
('VERSION_PLATAFORMA', NULL, 'METHYLOX v3.0-Production', 'Official SaMD production version tag.');

-- ============================================================================
-- METHYLOX™ PLATFORM v3.0 - ENTERPRISE SECURITY UPGRADE (DYNAMIC RBAC)
-- ============================================================================

-- 1. CREATE PERMISSIONS CATALOG (Universal actions)
CREATE TABLE IF NOT EXISTS permissions (
    id_permission SERIAL PRIMARY KEY,
    permission_code VARCHAR(50) NOT NULL UNIQUE, -- E.g., 'SAMPLE_CREATE', 'ANALYSIS_RUN'
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CREATE DYNAMIC ROLES TABLE (Allows the client to create ANY role name dynamically)
CREATE TABLE IF NOT EXISTS custom_roles (
    id_role SERIAL PRIMARY KEY,
    role_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. CREATE MANY-TO-MANY RELATION: ROLE-PERMISSIONS MATRIX
CREATE TABLE IF NOT EXISTS role_permissions (
    id_role INTEGER REFERENCES custom_roles(id_role) ON DELETE CASCADE,
    id_permission INTEGER REFERENCES permissions(id_permission) ON DELETE CASCADE,
    PRIMARY KEY (id_role, id_permission)
);

-- 4. EVOLVE THE EXISTING USERS TABLE (Add dynamic role support)
-- We inject a reference to the new dynamic roles table to bypass the old static CHECK constraint.
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS dynamic_role_id INTEGER REFERENCES custom_roles(id_role) ON DELETE RESTRICT;

-- 5. SEED UNIVERSAL IMMUTABLE CLINICAL PERMISSIONS
INSERT INTO permissions (permission_code, description) VALUES
('SAMPLE_CREATE', 'Allows registration of new biological and mock cohort samples.'),
('DATA_UPLOAD', 'Allows uploading raw fluorescence intensity files (Methylated/Unmethylated channels).'),
('ANALYSIS_RUN', 'Allows triggering the CRISPR-cas processing engine and Beta-value generation.'),
('REPORT_DOWNLOAD', 'Allows generating and downloading clinical PDF oncology diagnostic reports.'),
('USER_MANAGE', 'Allows creation, role assignment, and suspension of users within the same hospital.')
ON CONFLICT (permission_code) DO NOTHING;


-- ============================================================================
-- SEEDING INITIAL ENTERPRISE CREDENTIALS FOR CLINICAL DEMOSTRATION
-- ============================================================================

-- Provision the baseline corporate hospital client instance (ID 1)
INSERT INTO hospitals (hospital_name, facility_code, country) 
VALUES ('Hospital ABC', 'HOSP-ABC-2026', 'MEX');

-- Provision the master clinical administrative security role (ID 1)
INSERT INTO custom_roles (role_name, description)
VALUES ('Organization Admin', 'Laboratory Director with full granular RBAC access privileges.');

-- Provision the initial clinical administrator master user profile link
INSERT INTO users (username, hashed_password, full_name, dynamic_role_id, id_hospital)
VALUES (
    'brewlint@gmail.com,
    '$2b$12$K.8/e2Xj2M60v.T03/fLHeQ6O9O17zZ6y0n2Yt1vH.cW5gO42/K1.',
    'Director de Oncologia',
    1,
    1
);
