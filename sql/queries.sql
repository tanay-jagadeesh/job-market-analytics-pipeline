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