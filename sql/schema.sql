CREATE DATABASE job_market_db;

-- storing unique company names 
CREATE TABLE companies (
    company_id INT PRIMARY KEY,
    company_name VARCHAR NOT NULL
)