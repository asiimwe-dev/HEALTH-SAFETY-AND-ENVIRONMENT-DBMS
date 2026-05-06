-- ============================================================
--  HSE MANAGEMENT SYSTEM — FULL DATABASE SCRIPT
--  Project: Ugandan Oil & Gas Sector (Tilenga / Kingfisher)
--  Author : Gilbert  |  Stack: MySQL 8.0+
--  Usage  : Run once to create and seed the database.
--           SOURCE hse_db.sql;
-- ============================================================

DROP DATABASE IF EXISTS hse_db;
CREATE DATABASE hse_db
  CHARACTER SET utf8mb4
  COLLATE       utf8mb4_unicode_ci;

USE hse_db;

-- ---------------------------------------------------------
-- TABLE: sites
-- ---------------------------------------------------------
CREATE TABLE sites (
  site_id           INT           NOT NULL AUTO_INCREMENT,
  site_name         VARCHAR(100)  NOT NULL,
  site_type         ENUM(
                      'Drilling Pad',
                      'Flow Station',
                      'Pipeline Corridor',
                      'Logistics Base',
                      'Camp'
                    )             NOT NULL,
  district          VARCHAR(50)   NOT NULL,
  region            VARCHAR(50)   NOT NULL DEFAULT 'Albertine Graben',
  gps_lat           DECIMAL(9,6)  NULL,
  gps_lng           DECIMAL(9,6)  NULL,
  hse_risk_category ENUM('Low','Medium','High','Critical')
                                  NOT NULL DEFAULT 'Medium',
  commissioned_date DATE          NULL,
  site_status       ENUM('Operational','Standby','Decommissioned')
                                  NOT NULL DEFAULT 'Operational',
  PRIMARY KEY (site_id),
  INDEX idx_district (district),
  INDEX idx_type     (site_type)
) ENGINE=InnoDB;


-- ---------------------------------------------------------
-- TABLE: employees
-- ---------------------------------------------------------
CREATE TABLE employees (
  employee_id     INT           NOT NULL AUTO_INCREMENT,
  first_name      VARCHAR(50)   NOT NULL,
  last_name       VARCHAR(50)   NOT NULL,
  national_id     VARCHAR(20)   NOT NULL,
  job_title       VARCHAR(100)  NOT NULL,
  department      VARCHAR(50)   NOT NULL,
  site_id         INT           NOT NULL,
  employment_type ENUM('Direct','Contractor','Sub-Contractor')
                                NOT NULL DEFAULT 'Direct',
  date_of_hire    DATE          NOT NULL,
  contact_phone   VARCHAR(20)   NULL,
  emp_status      ENUM('Active','On Leave','Terminated')
                                NOT NULL DEFAULT 'Active',
  PRIMARY KEY (employee_id),
  UNIQUE  KEY uq_national_id (national_id),
  FOREIGN KEY fk_emp_site (site_id)
    REFERENCES sites(site_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  INDEX idx_emp_status (emp_status),
  INDEX idx_emp_dept   (department)
) ENGINE=InnoDB;


-- ---------------------------------------------------------
-- TABLE: incidents
-- ---------------------------------------------------------
CREATE TABLE incidents (
  incident_id          INT       NOT NULL AUTO_INCREMENT,
  incident_date        DATETIME  NOT NULL,
  site_id              INT       NOT NULL,
  reported_by          INT       NOT NULL,
  involved_employee_id INT       NULL,
  incident_type        ENUM(
                         'Near-Miss',
                         'First Aid',
                         'MTC',
                         'LTI',
                         'Fatality',
                         'Environmental'
                       )         NOT NULL,
  severity             ENUM('Low','Medium','High','Critical')
                                 NOT NULL DEFAULT 'Medium',
  description          TEXT      NOT NULL,
  root_cause           ENUM(
                         'Procedural Violation',
                         'Equipment Failure',
                         'Human Error',
                         'Environmental Condition',
                         'Management System Gap'
                       )         NOT NULL,
  immediate_action     TEXT      NULL,
  corrective_action    TEXT      NULL,
  inc_status           ENUM('Open','Under Investigation','Closed')
                                 NOT NULL DEFAULT 'Open',
  closed_date          DATE      NULL,
  PRIMARY KEY (incident_id),
  FOREIGN KEY fk_inc_site     (site_id)
    REFERENCES sites(site_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY fk_inc_reporter (reported_by)
    REFERENCES employees(employee_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY fk_inc_involved (involved_employee_id)
    REFERENCES employees(employee_id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  INDEX idx_inc_date     (incident_date),
  INDEX idx_inc_type     (incident_type),
  INDEX idx_inc_severity (severity),
  INDEX idx_inc_status   (inc_status)
) ENGINE=InnoDB;


-- ---------------------------------------------------------
-- TABLE: training_courses
-- ---------------------------------------------------------
CREATE TABLE training_courses (
  course_id           INT           NOT NULL AUTO_INCREMENT,
  course_name         VARCHAR(150)  NOT NULL,
  course_code         VARCHAR(20)   NOT NULL,
  category            ENUM(
                        'Safety Induction',
                        'Well Control',
                        'Emergency Response',
                        'Environmental',
                        'First Aid',
                        'Hazardous Materials',
                        'Leadership'
                      )             NOT NULL,
  validity_months     INT           NOT NULL DEFAULT 24,
  is_mandatory        TINYINT(1)    NOT NULL DEFAULT 1,
  provider            VARCHAR(100)  NULL,
  description         TEXT          NULL,
  PRIMARY KEY (course_id),
  UNIQUE KEY uq_course_code (course_code)
) ENGINE=InnoDB;


-- ---------------------------------------------------------
-- TABLE: employee_training  (M:N resolution)
-- ---------------------------------------------------------
CREATE TABLE employee_training (
  record_id          INT          NOT NULL AUTO_INCREMENT,
  employee_id        INT          NOT NULL,
  course_id          INT          NOT NULL,
  completion_date    DATE         NOT NULL,
  expiry_date        DATE         NOT NULL,
  certificate_number VARCHAR(60)  NULL,
  score              DECIMAL(5,2) NULL,
  cert_status        ENUM('Valid','Expired','Pending Renewal')
                                  NOT NULL DEFAULT 'Valid',
  PRIMARY KEY (record_id),
  UNIQUE KEY uq_emp_course_date (employee_id, course_id, completion_date),
  FOREIGN KEY fk_et_employee (employee_id)
    REFERENCES employees(employee_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY fk_et_course   (course_id)
    REFERENCES training_courses(course_id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  INDEX idx_et_expiry (expiry_date),
  INDEX idx_et_status (cert_status)
) ENGINE=InnoDB;


-- =========================================================
-- DML: SAMPLE DATA
-- =========================================================

INSERT INTO sites (site_name, site_type, district, region, gps_lat, gps_lng, hse_risk_category, commissioned_date, site_status) VALUES
('Tilenga Pad TP-09',        'Drilling Pad',       'Buliisa',  'Albertine Graben',  1.916700,  31.266700, 'Critical', '2022-03-15', 'Operational'),
('Tilenga Pad TP-14',        'Drilling Pad',       'Buliisa',  'Albertine Graben',  1.930200,  31.289100, 'Critical', '2022-09-01', 'Operational'),
('Kingfisher Flow Station',  'Flow Station',       'Kikuube',  'Albertine Graben',  1.483300,  31.550000, 'High',     '2023-01-20', 'Operational'),
('Buhimba Logistics Base',   'Logistics Base',     'Hoima',    'Albertine Graben',  1.430000,  31.350000, 'Medium',   '2021-06-10', 'Operational'),
('EACOP KP-045 Corridor',    'Pipeline Corridor',  'Kikuube',  'Albertine Graben',  1.390000,  31.610000, 'High',     '2023-06-01', 'Operational');


INSERT INTO employees (first_name, last_name, national_id, job_title, department, site_id, employment_type, date_of_hire, contact_phone, emp_status) VALUES
('Amos',      'Kaboyo',     'UG-CM-2019-0012', 'HSE Supervisor',        'HSE',         1, 'Direct',         '2019-08-01', '+256 772 001001', 'Active'),
('Grace',     'Namutebi',   'UG-KLA-2020-0445','Field Safety Officer',  'HSE',         1, 'Direct',         '2020-02-14', '+256 754 002002', 'Active'),
('Patrick',   'Okello',     'UG-GL-2018-0338', 'Rig Manager',           'Drilling',    1, 'Direct',         '2018-05-20', '+256 782 003003', 'Active'),
('Harriet',   'Akello',     'UG-BU-2021-0097', 'Driller',               'Drilling',    2, 'Direct',         '2021-03-10', '+256 701 004004', 'Active'),
('Emmanuel',  'Byaruhanga', 'UG-KIK-2020-0221','Field Safety Officer',  'HSE',         3, 'Contractor',     '2020-07-15', '+256 788 005005', 'Active'),
('Judith',    'Nassimbwa',  'UG-HOI-2022-0088','Logistics Coordinator', 'Logistics',   4, 'Direct',         '2022-01-03', '+256 777 006006', 'Active'),
('Robert',    'Tugume',     'UG-BU-2019-0501', 'Pipeline Inspector',    'Engineering', 5, 'Contractor',     '2019-11-19', '+256 700 007007', 'Active'),
('Christine', 'Atim',       'UG-GL-2023-0003', 'Rig Hand',              'Drilling',    2, 'Sub-Contractor', '2023-05-01', '+256 752 008008', 'Active'),
('Moses',     'Waiswa',     'UG-KLA-2017-0200','Senior HSE Auditor',    'HSE',         4, 'Direct',         '2017-04-12', '+256 714 009009', 'Active'),
('Florence',  'Amoding',    'UG-KIK-2021-0155','Environmental Officer', 'HSE',         3, 'Direct',         '2021-09-20', '+256 766 010010', 'Active');


INSERT INTO training_courses (course_name, course_code, category, validity_months, is_mandatory, provider, description) VALUES
('BOSIET — Basic Offshore Safety Induction & Emergency Training', 'BOSIET',    'Safety Induction',  36, 1, 'Stork Training Centre, Kampala', 'Sea survival, firefighting, HUET and emergency response.'),
('H2S Awareness and Breathing Apparatus',                         'H2S-BA',    'Hazardous Materials',24,1, 'Stork Training Centre, Kampala', 'Detection, personal monitoring and escape BA for H2S environments.'),
('IWCF Well Control — Level 3 (Drilling)',                        'IWCF-L3',   'Well Control',      24, 1, 'International Well Control Forum','Drilling well control at the supervisory level.'),
('First Aid Level 3 — Occupational',                              'FA-L3',     'First Aid',         24, 1, 'Uganda Red Cross Society',       'Occupational first aid including CPR and AED.'),
('NEBOSH International General Certificate',                      'NEBOSH-IGC','Leadership',         0, 0, 'Makerere University / NEBOSH',   'Globally recognised HSE management qualification.'),
('Environmental Impact Assessment Practitioner',                  'EIA-PRAC',  'Environmental',     30, 0, 'NEMA Uganda',                    'National EIA practitioner accreditation.'),
('Fire Warden & Emergency Response',                              'FWER',      'Emergency Response',12, 1, 'TotalEnergies Site Training',    'Emergency assembly, evacuation and firefighting.'),
('Pipeline Integrity Management (ASME B31.8)',                    'PIM-B318',  'Safety Induction',  24, 0, 'Uganda Petroleum Institute',     'Pipeline inspection and integrity management.');


INSERT INTO incidents (incident_date, site_id, reported_by, involved_employee_id, incident_type, severity, description, root_cause, immediate_action, corrective_action, inc_status, closed_date) VALUES
('2024-02-10 08:35:00', 1, 2, 3, 'Near-Miss', 'Medium',
 'Drill pipe stand improperly racked, nearly fell onto rig floor during pipe-tripping at TP-09. Rig manager was in proximity.',
 'Procedural Violation',
 'Operations halted. Area cordoned and pipe stand re-racked by competent rigger.',
 'Refresher toolbox talk on pipe-racking procedures. Update SOP DRL-007.',
 'Closed', '2024-02-15'),

('2024-03-22 14:10:00', 1, 2, 4, 'First Aid', 'Low',
 'Rig hand sustained laceration to left forearm while handling valve manifold. Required first aid at site medic.',
 'Human Error',
 'First aid administered on-site. Incident communicated to rig manager.',
 'Mandatory glove inspection before manifold handling. Update PPE checklist.',
 'Closed', '2024-03-28'),

('2024-05-07 06:50:00', 2, 2, 8, 'LTI', 'High',
 'Sub-contracted rig hand slipped on wet cellar deck, fractured wrist. Medevac to Hoima Regional Referral Hospital. 18 working days lost.',
 'Environmental Condition',
 'Worker evacuated. Cellar deck operations suspended. PAU notified within 24 hours.',
 'Install non-slip matting on all cellar deck surfaces. Add to pre-shift inspection checklist.',
 'Closed', '2024-06-10'),

('2024-07-19 11:22:00', 3, 5, NULL, 'Environmental', 'High',
 '50 litres of produced water spilled from corroded flange at Kingfisher separator train. Contained within secondary bund; soil contamination at bund edge detected.',
 'Equipment Failure',
 'Separator isolated. Spill contained with absorbent granules. NEMA notification completed.',
 'Inspect all flanges older than 18 months. Replace corroded units. Review containment SOP.',
 'Under Investigation', NULL),

('2024-09-03 16:45:00', 5, 7, 7, 'Near-Miss', 'Critical',
 'Pipeline inspection vehicle struck unmarked third-party excavation trench near EACOP KP-045. Vehicle nearly overturned. No permit-to-work obtained by contractor.',
 'Management System Gap',
 'Trench barricaded. Contractor vehicle impounded. Third-party supervisor escorted off site.',
 'Reinforce permit-to-work system for third-party activities. Install ROW marker posts every 200 m.',
 'Open', NULL);


INSERT INTO employee_training (employee_id, course_id, completion_date, expiry_date, certificate_number, score, cert_status) VALUES
(1, 1, '2022-01-15', '2025-01-15', 'BSIT-UG-2022-0041', 92.50, 'Valid'),
(1, 5, '2021-06-20', '9999-12-31', 'NGC-UG-2021-0099',  78.00, 'Valid'),
(1, 7, '2023-11-10', '2024-11-10', 'FWER-TP-2023-0021', 88.00, 'Valid'),
(2, 1, '2021-09-20', '2024-09-20', 'BSIT-UG-2021-0305', 85.00, 'Expired'),
(2, 2, '2023-04-10', '2025-04-10', 'H2S-UG-2023-1102',  91.00, 'Valid'),
(2, 4, '2022-06-01', '2024-06-01', 'FA3-UG-2022-0088',  88.50, 'Expired'),
(2, 7, '2023-11-10', '2024-11-10', 'FWER-TP-2023-0022', 90.00, 'Valid'),
(3, 1, '2023-03-05', '2026-03-05', 'BSIT-UG-2023-0099', 94.00, 'Valid'),
(3, 3, '2022-11-01', '2024-11-01', 'IWCF-LV3-2022-0088',89.00, 'Expired'),
(3, 5, '2020-08-15', '9999-12-31', 'NGC-UG-2020-0044',  82.00, 'Valid'),
(4, 3, '2023-05-20', '2025-05-20', 'IWCF-LV3-2023-0112',87.50, 'Valid'),
(4, 4, '2024-01-08', '2026-01-08', 'FA3-UG-2024-0017',  93.00, 'Valid'),
(4, 2, '2022-07-14', '2024-07-14', 'H2S-UG-2022-0897',  79.00, 'Expired'),
(5, 1, '2023-02-28', '2026-02-28', 'BSIT-UG-2023-0212', 88.00, 'Valid'),
(5, 2, '2023-08-01', '2025-08-01', 'H2S-UG-2023-1455',  95.00, 'Valid'),
(5, 7, '2024-01-15', '2025-01-15', 'FWER-KF-2024-0003', 86.00, 'Valid'),
(6, 4, '2023-03-12', '2025-03-12', 'FA3-UG-2023-0121',  90.00, 'Valid'),
(6, 7, '2023-11-20', '2024-11-20', 'FWER-BL-2023-0044', 83.00, 'Valid'),
(7, 8, '2023-08-05', '2025-08-05', 'PIM-UG-2023-0034',  91.00, 'Valid'),
(7, 2, '2022-09-10', '2024-09-10', 'H2S-UG-2022-1122',  88.00, 'Expired'),
(7, 7, '2024-02-20', '2025-02-20', 'FWER-EC-2024-0007', 85.00, 'Valid'),
(8, 1, '2023-05-02', '2026-05-02', 'BSIT-UG-2023-0441', 80.00, 'Valid'),
(8, 7, '2023-05-03', '2024-05-03', 'FWER-TP-2023-0088', 77.00, 'Expired'),
(9, 5, '2021-03-15', '9999-12-31', 'NGC-UG-2021-0055',  95.00, 'Valid'),
(9, 1, '2022-06-10', '2025-06-10', 'BSIT-UG-2022-0199', 96.00, 'Valid'),
(9, 4, '2023-09-01', '2025-09-01', 'FA3-UG-2023-0299',  92.00, 'Valid'),
(10, 6, '2022-10-01', '2025-04-01', 'NEMA-EIA-2022-0077',89.00,'Valid'),
(10, 2, '2023-01-15', '2025-01-15', 'H2S-UG-2023-0041', 88.00, 'Valid'),
(10, 4, '2023-06-20', '2025-06-20', 'FA3-UG-2023-0188',  91.00,'Valid');


-- ---------------------------------------------------------
-- VIEWS
-- ---------------------------------------------------------
CREATE OR REPLACE VIEW v_incident_detail AS
SELECT
  i.incident_id,
  i.incident_date,
  s.site_name,
  s.district,
  CONCAT(e.first_name, ' ', e.last_name) AS reported_by,
  i.incident_type,
  i.severity,
  i.root_cause,
  i.inc_status,
  i.description
FROM incidents i
  JOIN sites     s ON i.site_id     = s.site_id
  JOIN employees e ON i.reported_by = e.employee_id;


CREATE OR REPLACE VIEW v_training_compliance AS
SELECT
  e.employee_id,
  CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
  e.job_title,
  s.site_name,
  tc.course_name,
  tc.course_code,
  tc.category,
  et.completion_date,
  et.expiry_date,
  et.cert_status,
  DATEDIFF(et.expiry_date, CURDATE())    AS days_until_expiry
FROM employee_training et
  JOIN employees        e  ON et.employee_id = e.employee_id
  JOIN training_courses tc ON et.course_id   = tc.course_id
  JOIN sites            s  ON e.site_id      = s.site_id
ORDER BY et.expiry_date ASC;
