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

-- storing unique skills

CREATE TABLE skills (
    skill_id INT PRIMARY KEY,
    skill_name VARCHAR NOT NULL
)

-- job postings table (info)
CREATE TABLE job_postings (
    job_id INT PRIMARY KEY,
    job_title VARCHAR NOT NULL,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    salary_min INT NOT NULL,
    salary_max INT NOT NULL,
    posted_date DATE,
    is_remote BOOLEAN,
    experience_level VARCHAR,
    job_description VARCHAR
)

-- job skills table
CREATE TABLE job_skills (
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
)
