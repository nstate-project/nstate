-- nstate DuckDB schema
-- Run once to initialise the warehouse

-- ─── Meta tables ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS meta_datasets (
    id          VARCHAR PRIMARY KEY,
    country     VARCHAR NOT NULL,
    name        VARCHAR NOT NULL,
    description VARCHAR,
    source_url  VARCHAR,
    licence     VARCHAR DEFAULT 'OGL v3',
    last_loaded TIMESTAMP,
    row_count   INTEGER,
    priority    INTEGER DEFAULT 99
);

CREATE TABLE IF NOT EXISTS meta_sources (
    id           VARCHAR PRIMARY KEY,
    country      VARCHAR NOT NULL,
    institution  VARCHAR NOT NULL,
    dataset_name VARCHAR NOT NULL,
    release_url  VARCHAR,
    release_date DATE,
    licence      VARCHAR DEFAULT 'OGL v3',
    sha256       VARCHAR,
    loaded_at    TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meta_findings (
    id              VARCHAR PRIMARY KEY,
    country         VARCHAR NOT NULL,
    question        VARCHAR,
    headline        VARCHAR NOT NULL,
    explanation     VARCHAR,
    key_stat_value  DECIMAL(18,2),
    key_stat_unit   VARCHAR,
    key_stat_label  VARCHAR,
    caveat          VARCHAR,
    status          VARCHAR DEFAULT 'automated_finding',
    chart_spec      JSON,
    sql_query       VARCHAR,
    source_ids      VARCHAR[],
    created_at      TIMESTAMP,
    reviewed_at     TIMESTAMP,
    reviewed_by     VARCHAR
);

CREATE TABLE IF NOT EXISTS meta_queries (
    id         INTEGER PRIMARY KEY,
    question   VARCHAR NOT NULL,
    country    VARCHAR NOT NULL,
    result_id  VARCHAR,
    created_at TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS meta_queries_seq;
ALTER TABLE meta_queries ALTER COLUMN id SET DEFAULT nextval('meta_queries_seq');

CREATE TABLE IF NOT EXISTS meta_gaps (
    topic            VARCHAR NOT NULL,
    country          VARCHAR NOT NULL,
    question_example VARCHAR,
    votes            INTEGER DEFAULT 1,
    created_at       TIMESTAMP,
    PRIMARY KEY (topic, country)
);

-- ─── UK data tables ───────────────────────────────────────────

-- Civil service headcount (Cabinet Office)
CREATE TABLE IF NOT EXISTS uk_civil_service_headcount (
    period        DATE NOT NULL,
    department    VARCHAR,
    headcount     INTEGER,
    fte           DECIMAL(10,1),
    pay_band      VARCHAR,
    geography     VARCHAR DEFAULT 'UK',
    source_id     VARCHAR,
    release_date  DATE,
    _loaded_at    TIMESTAMP DEFAULT current_timestamp
);

-- Civil service pay bill (Cabinet Office)
CREATE TABLE IF NOT EXISTS uk_civil_service_pay (
    period        DATE NOT NULL,
    department    VARCHAR,
    total_pay_gbp DECIMAL(18,2),
    median_pay    DECIMAL(10,2),
    mean_pay      DECIMAL(10,2),
    price_basis   VARCHAR DEFAULT 'nominal',
    source_id     VARCHAR,
    release_date  DATE,
    _loaded_at    TIMESTAMP DEFAULT current_timestamp
);

-- Public sector finances (OBR)
CREATE TABLE IF NOT EXISTS uk_psf_receipts (
    period        DATE NOT NULL,
    category      VARCHAR NOT NULL,
    value_gbpm    DECIMAL(18,2),  -- GBP millions
    price_basis   VARCHAR DEFAULT 'nominal',
    source_id     VARCHAR,
    release_date  DATE,
    _loaded_at    TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS uk_psf_expenditure (
    period        DATE NOT NULL,
    department    VARCHAR,
    category      VARCHAR,
    value_gbpm    DECIMAL(18,2),  -- GBP millions
    price_basis   VARCHAR DEFAULT 'nominal',
    source_id     VARCHAR,
    release_date  DATE,
    _loaded_at    TIMESTAMP DEFAULT current_timestamp
);

-- Register datasets in meta
INSERT OR IGNORE INTO meta_datasets VALUES
    ('uk_civil_service', 'uk', 'Civil Service Statistics',
     'UK civil service headcount and pay by department, 2010–present',
     'https://www.gov.uk/government/collections/civil-service-statistics',
     'OGL v3', NULL, NULL, 1),
    ('uk_psf', 'uk', 'Public Sector Finances',
     'Monthly public sector receipts and expenditure from OBR',
     'https://obr.uk/data/',
     'OGL v3', NULL, NULL, 2);

SELECT 'Schema initialised' as status;
