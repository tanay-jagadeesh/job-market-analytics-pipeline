-- Query 1: Top 10 In-Demand Skills
SELECT
    s.skill_name,
    COUNT(*) as job_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT job_id) FROM job_skills), 2) as percentage_of_jobs
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
GROUP BY s.skill_name
ORDER BY job_count DESC
LIMIT 10;


-- Query 2: Job Postings with Company and Location Details
SELECT
    jp.job_id,
    jp.job_title,
    c.company_name,
    l.city,
    l.province,
    jp.salary_min,
    jp.salary_max,
    jp.is_remote
FROM job_postings jp
JOIN companies c ON jp.company_id = c.company_id
JOIN locations l ON jp.location_id = l.location_id
ORDER BY jp.job_id
LIMIT 10;

-- Query 3: Average Salary by role (rounded average, # of jobs w title, salary range, median, standard deviation)
SELECT job_title, 
ROUND(AVG((salary_min + salary_max) / 2 )) as avg_salary,
COUNT(*) as job_count,
AVG(salary_max - salary_min) as salary_range,
PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (salary_min + salary_max) / 2) as median_salary,
STDDEV((salary_min + salary_max) / 2) as std_salary
FROM job_postings
GROUP BY job_title
;

-- Query 4 - Skill Occurence
SELECT
    s1.skill_name AS skill_1,
    s2.skill_name AS skill_2,
    COUNT(*) as pair_count
FROM job_skills AS js1
JOIN job_skills AS js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
JOIN skills AS s1 ON s1.skill_id = js1.skill_id
JOIN skills AS s2 ON s2.skill_id = js2.skill_id
GROUP BY skill_1, skill_2
HAVING COUNT(*) >= 5
ORDER BY pair_count DESC
;

-- Query 5 - Hiring Trends Over Time
SELECT 
    DATE_TRUNC('week', posted_date) AS week_start,
    COUNT(*) as jobs_posted,
    COUNT(DISTINCT company_id) as unique_companies
FROM job_postings 
WHERE posted_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY week_start
ORDER BY week_start DESC
;

-- Query 6 - Top Hiring Companies
SELECT
    c.company_name,
    COUNT(*) as job_count,
    COUNT(DISTINCT location_id) AS unique_locations,
    AVG((salary_min + salary_max) / 2) AS avg_salary
FROM companies AS c
JOIN job_postings AS jp ON c.company_id = jp.company_id
GROUP BY c.company_name
HAVING COUNT(*) >= 3
ORDER BY job_count DESC
;