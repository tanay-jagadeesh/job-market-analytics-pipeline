import pandas as pd
from db import get_connection

def run_query_1():
    """Top 10 In-Demand Skills"""
    query = """
    SELECT
        s.skill_name,
        COUNT(*) as job_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT job_id) FROM job_skills), 2) as percentage_of_jobs
    FROM job_skills js
    JOIN skills s ON js.skill_id = s.skill_id
    GROUP BY s.skill_name
    ORDER BY job_count DESC
    LIMIT 10;
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    df.to_csv('results/query_1_top_skills.csv', index=False)
    conn.close()
    print("Query 1 complete: Top 10 In-Demand Skills saved to results/query_1_top_skills.csv")
    return df

def run_query_2():
    """Job Postings with Company and Location Details"""
    query = """
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
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    df.to_csv('results/query_2_job_details.csv', index=False)
    conn.close()
    print("Query 2 complete: Job Details saved to results/query_2_job_details.csv")
    return df

def run_query_3():
    """Average Salary by Role"""
    query = """
    SELECT job_title,
    ROUND(AVG((salary_min + salary_max) / 2 )) as avg_salary,
    COUNT(*) as job_count,
    AVG(salary_max - salary_min) as salary_range,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (salary_min + salary_max) / 2) as median_salary,
    STDDEV((salary_min + salary_max) / 2) as std_salary
    FROM job_postings
    GROUP BY job_title;
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    df.to_csv('results/query_3_salary_by_role.csv', index=False)
    conn.close()
    print("Query 3 complete: Salary by Role saved to results/query_3_salary_by_role.csv")
    return df

def run_query_4():
    """Skill Co-occurrence"""
    query = """
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
    ORDER BY pair_count DESC;
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    df.to_csv('results/query_4_skill_cooccurrence.csv', index=False)
    conn.close()
    print("Query 4 complete: Skill Co-occurrence saved to results/query_4_skill_cooccurrence.csv")
    return df

def run_query_5():
    """Hiring Trends Over Time"""
    query = """
    SELECT
        DATE_TRUNC('week', posted_date) AS week_start,
        COUNT(*) as jobs_posted,
        COUNT(DISTINCT company_id) as unique_companies
    FROM job_postings
    WHERE posted_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY week_start
    ORDER BY week_start DESC;
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    df.to_csv('results/query_5_hiring_trends.csv', index=False)
    conn.close()
    print("Query 5 complete: Hiring Trends saved to results/query_5_hiring_trends.csv")
    return df
