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
