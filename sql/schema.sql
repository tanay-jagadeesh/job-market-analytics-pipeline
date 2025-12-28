CREATE DATABASE job_market_db;

-- storing unique company names 

CREATE TABLE companies (
    company_id INT PRIMARY KEY,
    company_name VARCHAR NOT NULL
)

-- storing unique cities

CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL
)

CREATE TABLE skills (
    skill_id INT PRIMARY KEY,
    skill_name VARCHAR NOT NULL
)