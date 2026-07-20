-- 1. Table for Dynamic Calibration Parameters (No more hardcoded 0.02 or 0.1000)
CREATE TABLE clinical_calibration (
    parameter_key VARCHAR(50) PRIMARY KEY,
    numeric_value NUMERIC(6, 4),
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
    id_patient VARCHAR(50) REFERENCES patients(id_patient),
    id_hospital INT REFERENCES hospitals(id_hospital),
    operator_id INT REFERENCES users(id_user),
    control_blank NUMERIC(5,4) NOT NULL,
    control_negative NUMERIC(5,4) NOT NULL,
    control_positive NUMERIC(5,4) NOT NULL,
    replicate_1 NUMERIC(5,4) NOT NULL,
    replicate_2 NUMERIC(5,4) NOT NULL,
    replicate_3 NUMERIC(5,4) NOT NULL,
    mean_beta NUMERIC(5,4),
    diagnostic_verdict VARCHAR(50),
    lims_security_hash VARCHAR(64),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INJECT MASTER OPERATIONAL METADATA
INSERT INTO clinical_calibration (parameter_key, numeric_value, text_value, description) VALUES
('UMBRAL_YOUDEN', 0.1000, NULL, 'Optimal cutoff point for breast cancer positivity calling.'),
('LIMITE_RUIDO', 0.0200, NULL, 'Maximum fluorescence noise allowed for Blank and Negative controls.'),
('CONSTANTE_FONDO', 100.0000, NULL, 'Illumina baseline laser correction constant.'),
('VERSION_PLATAFORMA', NULL, 'METHYLOX v3.0-Production', 'Official SaMD production version tag.');
