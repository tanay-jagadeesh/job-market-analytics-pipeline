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
