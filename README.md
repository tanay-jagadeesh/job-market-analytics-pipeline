# Job Market Analytics Pipeline

End-to-end data pipeline for job market analysis: scraping, cleaning, database storage, and interactive dashboard.

## Structure
```
scrapers/      # Web scraping
data/          # Raw & cleaned data
config/        # Configuration
logs/          # Logs
notebooks/     # Analysis
sql/           # Database scripts
queries/       # Query functions
dashboard/     # Dashboard app
tests/         # Tests
```

## Tech Stack
**Scraping:** BeautifulSoup, Selenium, Requests
**Data Processing:** Pandas, NumPy
**Database:** PostgreSQL, SQLAlchemy
**Automation:** Apache Airflow
**Analysis:** Jupyter Notebooks
**Visualization:** Plotly, Matplotlib, Seaborn
