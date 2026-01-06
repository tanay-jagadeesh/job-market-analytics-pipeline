import pandas as pd
from db import get_connection
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

def run_query_6():
    """Top Hiring Companies"""
    query = """
    SELECT
        c.company_name,
        COUNT(*) as job_count,
        COUNT(DISTINCT location_id) AS unique_locations,
        AVG((salary_min + salary_max) / 2) AS avg_salary
    FROM companies AS c
    JOIN job_postings AS jp ON c.company_id = jp.company_id
    GROUP BY c.company_name
    HAVING COUNT(*) >= 3
    ORDER BY job_count DESC;
    """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    df.to_csv('results/query_6_top_companies.csv', index=False)
    conn.close()
    print("Query 6 complete: Top Hiring Companies saved to results/query_6_top_companies.csv")
    return df

def run_all_queries():
    """Run all queries and save results to CSV files"""
    print("Running all queries...\n")

    run_query_1()
    run_query_2()
    run_query_3()
    run_query_4()
    run_query_5()
    run_query_6()

    print("\n" + "="*60)
    print("All queries completed successfully!")
    print("Results saved to the 'results/' directory")
    print("="*60)

if __name__ == "__main__":
    # Create results directory if it doesn't exist
    import os
    if not os.path.exists('results'):
        os.makedirs('results')

    # Run all queries
    run_all_queries()

# Read the top skills data from CSV
df = pd.read_csv('results/query_1_top_skills.csv')

# Get top 9 skills
df_top_skills = df.head(9)

# Create a figure with size 10x8 inches
plt.figure(figsize = (10, 8))
# Create horizontal bar chart: skill names on Y-axis, percentages on X-axis
plt.barh(df_top_skills['skill_name'], df_top_skills['percentage_of_jobs'])

# Add labels to axes
plt.xlabel('Percentage of Jobs')
plt.ylabel('Skill')
plt.title('Top 9 In-Demand Skills')

# Save the figure to images folder (bbox_inches='tight' removes extra whitespace)
plt.savefig('images/top_skills.png', bbox_inches='tight')

plt.close()

# Read the top companies data from CSV
df_companies = pd.read_csv('results/query_6_top_companies.csv')

# Get top 10 companies
df_top_companies = df_companies.head(10)

# Create a figure with size 10x8 inches
plt.figure(figsize=(10, 8))
# Create pie chart with percentages
plt.pie(df_top_companies['job_count'], labels=df_top_companies['company_name'], autopct='%1.1f%%')
# Add white circle in center to create donut effect
circle = plt.Circle((0,0), 0.70, fc='white')
plt.gca().add_artist(circle)

# Add title
plt.title('Top 10 Hiring Companies: Market Share')

# Save the figure to images folder
plt.savefig('images/top_companies.png', bbox_inches='tight')

plt.close()

# Read skill co-occurrence data from CSV
df_skills = pd.read_csv('results/query_4_skill_cooccurrence.csv')

# Get all unique skills
all_skills = sorted(set(df_skills['skill_1'].unique()) | set(df_skills['skill_2'].unique()))

# Create a matrix (2D array) to store co-occurrence counts
matrix = np.zeros((len(all_skills), len(all_skills)))

# Fill the matrix with co-occurrence counts
for _, row in df_skills.iterrows():
    skill1_idx = all_skills.index(row['skill_1'])
    skill2_idx = all_skills.index(row['skill_2'])
    
    matrix[skill1_idx][skill2_idx] = row['pair_count']
    matrix[skill2_idx][skill1_idx] = row['pair_count']

# Create a figure with size 12x10 inches
plt.figure(figsize=(12, 10))
# Create heatmap with skill names as labels
sns.heatmap(matrix, xticklabels=all_skills, yticklabels=all_skills,
            annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Co-occurrence Count'})

# Add title
plt.title('Skill Co-occurrence Heatmap')
plt.xlabel('Skills')
plt.ylabel('Skills')

# Rotate labels for better readability
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# Save the figure to images folder
plt.savefig('images/skill_cooccurrence.png', bbox_inches='tight')

plt.close()