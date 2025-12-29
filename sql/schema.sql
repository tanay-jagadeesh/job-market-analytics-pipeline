CREATE DATABASE job_market_db;

-- storing unique company names

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL
);

-- storing unique cities

CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL
);

-- storing unique skills

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL
);

-- job postings table (info)
CREATE TABLE job_postings (
    job_id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    salary_min INT NOT NULL,
    salary_max INT NOT NULL,
    posted_date DATE,
    is_remote BOOLEAN,
    experience_level VARCHAR(50),
    job_description TEXT
);

-- job skills table
CREATE TABLE job_skills (
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
);
