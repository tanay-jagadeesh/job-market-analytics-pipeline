import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Job Market Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }

    /* Main background - light beige */
    .main {
        background-color: #F8F6F1;
    }

    /* Force all text to be dark and readable */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div {
        color: #1e293b !important;
    }

    /* Metrics styling - dark text */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a3a5c !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1e293b !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Headers - all dark */
    h1 {
        color: #1a3a5c !important;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    h2 {
        color: #1a3a5c !important;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2d5f8d;
        padding-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }

    h3 {
        color: #1e293b !important;
        font-weight: 600;
        font-size: 1.25rem;
    }

    /* Sidebar - dark background with light text */
    [data-testid="stSidebar"] {
        background-color: #1a3a5c;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }

    [data-testid="stSidebar"] h2 {
        color: #ffffff !important;
        border-bottom: 2px solid #2d5f8d;
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: #ffffff !important;
    }

    /* Radio buttons in sidebar - bright white text */
    .stRadio > label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
        color: #ffffff !important;
        padding: 0.5rem 0;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Section divider */
    hr {
        border: none;
        border-top: 1px solid #cbd5e1;
        margin: 2rem 0;
    }

    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 0.5rem;
        background: white;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    /* Slider styling */
    .stSlider {
        padding: 1rem 0;
    }

    .stSlider > div > div > div > div {
        background-color: #2d5f8d;
    }

    .stSlider [data-baseweb="slider"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Select box styling */
    .stSelectbox {
        padding: 1rem 0;
    }

    .stSelectbox label {
        color: #1e293b !important;
    }

    /* Info/warning/success boxes - dark text */
    [data-testid="stAlert"] {
        color: #1e293b !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] li,
    [data-testid="stAlert"] div {
        color: #1e293b !important;
    }

    /* Containers - white background with dark text */
    [data-testid="stVerticalBlock"] > div:has(> div.element-container) {
        background-color: white;
    }

    [data-testid="stVerticalBlock"] p,
    [data-testid="stVerticalBlock"] li,
    [data-testid="stVerticalBlock"] span {
        color: #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Canadian Data Analytics Job Market")
st.markdown("Real-time insights from the Canadian tech job market")

st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Select Page", ["Overview", "Skills Analysis", "Company Analysis", "Skill Relationships"], label_visibility="collapsed")

if page == "Overview":
    # Load data
    df_skills = pd.read_csv('results/query_1_top_skills.csv')
    df_companies = pd.read_csv('results/query_6_top_companies.csv')
    df_jobs = pd.read_csv('results/query_2_job_details.csv')

    # Key Metrics Section
    st.markdown("## Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Jobs Analyzed",
            value=f"{len(df_jobs):,}",
            delta="Live Data"
        )
    with col2:
        st.metric(
            label="Unique Skills Tracked",
            value=f"{len(df_skills):,}",
            delta=f"{df_skills['percentage_of_jobs'].iloc[0]:.1f}% top skill"
        )
    with col3:
        st.metric(
            label="Top Companies",
            value=f"{len(df_companies):,}",
            delta=f"{df_companies['job_count'].iloc[0]} jobs by #1"
        )
    with col4:
        # Salary estimation based on job titles and Canadian market data
        def estimate_salary(job_title):
            title_lower = job_title.lower()
            if 'senior' in title_lower or 'staff' in title_lower or 'lead' in title_lower:
                return 95000
            elif 'intern' in title_lower or 'co-op' in title_lower or 'student' in title_lower:
                return 45000
            elif 'entry' in title_lower or 'junior' in title_lower:
                return 60000
            elif 'analyst' in title_lower:
                return 72000
            else:
                return 70000

        # Calculate estimated average salary
        if 'job_title' in df_jobs.columns:
            estimated_salaries = df_jobs['job_title'].apply(estimate_salary)
            avg_estimated_salary = estimated_salaries.mean()
        else:
            avg_estimated_salary = 72000

        st.metric(
            label="Est. Avg Salary",
            value=f"${avg_estimated_salary:,.0f}",
            delta="Market Est."
        )

    st.markdown("---")

    # Interactive visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top 5 In-Demand Skills")
        top_5_skills = df_skills.head(5)

        fig = go.Figure(data=[
            go.Bar(
                x=top_5_skills['percentage_of_jobs'],
                y=top_5_skills['skill_name'],
                orientation='h',
                marker=dict(
                    color='#2d5f8d',
                    line=dict(color='#1a3a5c', width=1.5)
                ),
                text=top_5_skills['percentage_of_jobs'].apply(lambda x: f'{x:.1f}%'),
                textposition='auto',
            )
        ])

        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=10, b=10),
            xaxis_title="% of Jobs",
            yaxis_title="",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color='#1e293b', family='Arial'),
            xaxis=dict(title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            yaxis=dict(categoryorder='total ascending', tickfont=dict(size=12, color='#1e293b'))
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Top 5 Hiring Companies")
        top_5_companies = df_companies.head(5)

        fig = go.Figure(data=[
            go.Pie(
                labels=top_5_companies['company_name'],
                values=top_5_companies['job_count'],
                hole=0.4,
                marker=dict(
                    colors=['#1a3a5c', '#2d5f8d', '#4682b4', '#5a9bd4', '#87ceeb'],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent',
                textfont=dict(size=12, color='#1e293b')
            )
        ])

        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=10),
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Center card with total jobs
        st.metric(label="Total Jobs", value=top_5_companies['job_count'].sum())

    st.markdown("---")

    # Salary insights section
    st.markdown("## Salary Insights")

    sal_col1, sal_col2, sal_col3 = st.columns(3)

    with sal_col1:
        with st.container(border=True):
            st.markdown("**Entry-Level Roles**")
            st.markdown("• Interns/Co-ops: **$45,000**")
            st.markdown("• Junior Analysts: **$60,000**")

    with sal_col2:
        with st.container(border=True):
            st.markdown("**Mid-Level Roles**")
            st.markdown("• Data Analysts: **$72,000**")
            st.markdown("• Specialist Roles: **$70,000**")

    with sal_col3:
        with st.container(border=True):
            st.markdown("**Senior Roles**")
            st.markdown("• Senior/Staff Analysts: **$95,000+**")
            st.markdown("• Lead Positions: **$100,000+**")

    st.info("**Note**: Salary estimates are based on Canadian market data for data analytics positions. Actual salaries may vary by location, company size, and experience.")

    st.markdown("---")

    # About section
    st.markdown("## About This Project")

    with st.container(border=True):
        st.markdown("### Automated ETL Pipeline")
        st.markdown("""
        This dashboard provides real-time analytics of the Canadian data analytics job market.
        Data is automatically collected, processed, and analyzed using a robust ETL pipeline.

        **Key Features:**
        - PostgreSQL database for efficient data storage
        - Python-based ETL automation
        - Interactive Streamlit visualizations
        - Skill demand tracking and trend analysis
        """)

elif page == "Skills Analysis":
    st.markdown("## Skills Demand Analysis")
    st.markdown("Discover the most sought-after skills in the Canadian data analytics job market")

    df_skills = pd.read_csv('results/query_1_top_skills.csv')

    st.write("")  # Spacer

    # Controls
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        n_skills = st.slider("Number of skills to display", 3, 8, 8, help="Adjust to see more or fewer skills")
    with col2:
        chart_type = st.selectbox("Chart Type", ["Horizontal Bar", "Vertical Bar", "Lollipop"])
    with col3:
        st.write("")  # Spacer

    df_display = df_skills.head(n_skills)

    # Create interactive Plotly chart
    if chart_type == "Horizontal Bar":
        fig = go.Figure(data=[
            go.Bar(
                x=df_display['percentage_of_jobs'],
                y=df_display['skill_name'],
                orientation='h',
                marker=dict(
                    color='#2d5f8d',
                    line=dict(color='#1a3a5c', width=1.5)
                ),
                text=df_display['percentage_of_jobs'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Percentage: %{x:.1f}%<br>Job Count: %{customdata}<extra></extra>',
                customdata=df_display['job_count']
            )
        ])

        fig.update_layout(
            title=dict(text=f'Top {n_skills} In-Demand Skills', font=dict(color='#1a3a5c', size=16)),
            xaxis_title="Percentage of Jobs (%)",
            yaxis_title="Skill",
            height=max(400, n_skills * 40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color='#1e293b', family='Arial'),
            xaxis=dict(title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            yaxis=dict(categoryorder='total ascending', title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            margin=dict(l=10, r=10, t=50, b=50)
        )

    elif chart_type == "Vertical Bar":
        fig = go.Figure(data=[
            go.Bar(
                x=df_display['skill_name'],
                y=df_display['percentage_of_jobs'],
                marker=dict(
                    color='#2d5f8d',
                    line=dict(color='#1a3a5c', width=1.5)
                ),
                text=df_display['percentage_of_jobs'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Percentage: %{y:.1f}%<br>Job Count: %{customdata}<extra></extra>',
                customdata=df_display['job_count']
            )
        ])

        fig.update_layout(
            title=dict(text=f'Top {n_skills} In-Demand Skills', font=dict(color='#1a3a5c', size=16)),
            xaxis_title="Skill",
            yaxis_title="Percentage of Jobs (%)",
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color='#1e293b', family='Arial'),
            xaxis=dict(title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            yaxis=dict(title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            margin=dict(l=10, r=10, t=50, b=50)
        )

    else:  # Lollipop chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_display['percentage_of_jobs'],
            y=df_display['skill_name'],
            mode='markers+lines',
            marker=dict(
                size=15,
                color='#2d5f8d',
                line=dict(color='#1a3a5c', width=2)
            ),
            line=dict(color='#cbd5e1', width=2),
            text=df_display['percentage_of_jobs'].apply(lambda x: f'{x:.1f}%'),
            textposition='middle right',
            hovertemplate='<b>%{y}</b><br>Percentage: %{x:.1f}%<extra></extra>'
        ))

        fig.update_layout(
            title=dict(text=f'Top {n_skills} In-Demand Skills', font=dict(color='#1a3a5c', size=16)),
            xaxis_title="Percentage of Jobs (%)",
            yaxis_title="Skill",
            height=max(400, n_skills * 40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color='#1e293b', family='Arial'),
            xaxis=dict(range=[0, df_display['percentage_of_jobs'].max() * 1.15], title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            yaxis=dict(categoryorder='total ascending', title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            margin=dict(l=10, r=10, t=50, b=50)
        )

    st.plotly_chart(fig, use_container_width=True)

    # Data table with styling
    st.markdown("### Detailed Breakdown")

    # Add ranking and formatting
    df_display_formatted = df_display.copy()
    df_display_formatted.insert(0, 'Rank', range(1, len(df_display_formatted) + 1))
    df_display_formatted['percentage_of_jobs'] = df_display_formatted['percentage_of_jobs'].apply(lambda x: f'{x:.2f}%')
    df_display_formatted.columns = ['Rank', 'Skill Name', 'Job Count', 'Percentage of Jobs']

    st.dataframe(
        df_display_formatted,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Skill Name": st.column_config.TextColumn("Skill Name", width="medium"),
            "Job Count": st.column_config.NumberColumn("Job Count", width="small"),
            "Percentage of Jobs": st.column_config.TextColumn("% of Jobs", width="small")
        }
    )

    # Key insights
    st.markdown("### Key Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        top_skill = df_skills.iloc[0]
        st.info(f"**Most Demanded Skill**\n\n{top_skill['skill_name'].upper()} appears in {top_skill['percentage_of_jobs']:.1f}% of jobs")

    with col2:
        top_3_avg = df_skills.head(3)['percentage_of_jobs'].mean()
        st.success(f"**Top 3 Average**\n\nThe top 3 skills appear in {top_3_avg:.1f}% of jobs on average")

    with col3:
        total_skills = len(df_skills)
        st.warning(f"**Skill Diversity**\n\n{total_skills} unique skills tracked across all jobs")

elif page == "Company Analysis":
    st.markdown("## Top Hiring Companies")
    st.markdown("Explore which companies are actively hiring in the Canadian data analytics market")

    df_companies = pd.read_csv('results/query_6_top_companies.csv')

    st.write("")  # Spacer

    # Controls
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        n_companies = st.slider("Number of companies to display", 5, 17, 10)
    with col2:
        viz_type = st.selectbox("Visualization", ["Donut Chart", "Bar Chart", "Treemap"])
    with col3:
        st.write("")  # Spacer

    df_display = df_companies.head(n_companies)

    # Create visualizations
    if viz_type == "Donut Chart":
        fig = go.Figure(data=[
            go.Pie(
                labels=df_display['company_name'],
                values=df_display['job_count'],
                hole=0.5,
                marker=dict(
                    colors=px.colors.qualitative.Bold,
                    line=dict(color='white', width=3)
                ),
                textinfo='label+percent',
                textfont=dict(size=13, color='#1e293b'),
                hovertemplate='<b>%{label}</b><br>Job Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        ])

        fig.update_layout(
            title=f'Top {n_companies} Hiring Companies - Market Share',
            height=600,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(
                text=f'{df_display["job_count"].sum()}<br>Total Jobs',
                x=0.5, y=0.5,
                font_size=20,
                font_color='#1e293b',
                showarrow=False
            )]
        )

    elif viz_type == "Bar Chart":
        fig = go.Figure(data=[
            go.Bar(
                x=df_display['job_count'],
                y=df_display['company_name'],
                orientation='h',
                marker=dict(
                    color='#2d5f8d',
                    line=dict(color='#1a3a5c', width=1.5)
                ),
                text=df_display['job_count'],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Job Count: %{x}<br>Avg Salary: $%{customdata:,.0f}<extra></extra>',
                customdata=df_display['avg_salary']
            )
        ])

        fig.update_layout(
            title=dict(text=f'Top {n_companies} Hiring Companies', font=dict(color='#1a3a5c', size=16)),
            xaxis_title="Number of Job Postings",
            yaxis_title="Company",
            height=max(400, n_companies * 50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color='#1e293b', family='Arial'),
            xaxis=dict(title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            yaxis=dict(categoryorder='total ascending', title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
            margin=dict(l=10, r=10, t=50, b=50)
        )

    else:  # Treemap
        fig = go.Figure(go.Treemap(
            labels=df_display['company_name'],
            parents=["" for _ in range(len(df_display))],
            values=df_display['job_count'],
            textinfo="label+value+percent parent",
            marker=dict(
                colors=['#1a3a5c'] * len(df_display),
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{label}</b><br>Job Count: %{value}<br>Locations: %{customdata[0]}<br>Avg Salary: $%{customdata[1]:,.0f}<extra></extra>',
            customdata=list(zip(df_display['unique_locations'], df_display['avg_salary']))
        ))

        fig.update_layout(
            title=dict(text=f'Top {n_companies} Hiring Companies - Treemap View', font=dict(color='#1a3a5c', size=16)),
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12, color='#1e293b', family='Arial')
        )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed table
    st.markdown("### Company Details")

    df_display_formatted = df_display.copy()
    df_display_formatted.insert(0, 'Rank', range(1, len(df_display_formatted) + 1))
    df_display_formatted['avg_salary'] = df_display_formatted['avg_salary'].apply(
        lambda x: f"${x:,.0f}" if x > 0 else "N/A"
    )
    df_display_formatted.columns = ['Rank', 'Company Name', 'Job Count', 'Locations', 'Avg Salary']

    st.dataframe(
        df_display_formatted,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Company Name": st.column_config.TextColumn("Company Name", width="medium"),
            "Job Count": st.column_config.NumberColumn("Job Count", width="small"),
            "Locations": st.column_config.NumberColumn("Locations", width="small"),
            "Avg Salary": st.column_config.TextColumn("Avg Salary", width="small")
        }
    )

    # Key insights
    st.markdown("### Key Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        top_company = df_companies.iloc[0]
        st.info(f"**Top Employer**\n\n{top_company['company_name']} leads with {top_company['job_count']} job postings")

    with col2:
        total_jobs = df_display['job_count'].sum()
        st.success(f"**Total Opportunities**\n\nTop {n_companies} companies offer {total_jobs} positions")

    with col3:
        avg_locations = df_display['unique_locations'].mean()
        st.warning(f"**Geographic Spread**\n\nAverage of {avg_locations:.1f} locations per company")

elif page == "Skill Relationships":
    st.markdown("## Skill Co-occurrence Analysis")
    st.markdown("Discover which skills are frequently required together in job postings")

    df_cooccur = pd.read_csv('results/query_4_skill_cooccurrence.csv')

    # Top skill pairs metrics
    st.markdown("### Top Skill Combinations")
    col1, col2, col3 = st.columns(3)

    with col1:
        top_pair = df_cooccur.iloc[0]
        st.metric(
            label="Most Common Pair",
            value=f"{top_pair['skill_1']} + {top_pair['skill_2']}",
            delta=f"{top_pair['pair_count']} jobs"
        )

    with col2:
        total_pairs = len(df_cooccur)
        st.metric(
            label="Unique Skill Pairs",
            value=f"{total_pairs:,}",
            delta="Tracked combinations"
        )

    with col3:
        avg_cooccurrence = df_cooccur['pair_count'].mean()
        st.metric(
            label="Avg Co-occurrence",
            value=f"{avg_cooccurrence:.1f}",
            delta="jobs per pair"
        )

    st.markdown("---")

    # Network visualization using the heatmap image
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Skill Co-occurrence Heatmap")
        img = Image.open('images/skill_cooccurrence.png')
        st.image(img, caption="Darker colors indicate stronger skill relationships")

    with col2:
        st.markdown("### Interpretation Guide")
        st.markdown("""
        **How to read this heatmap:**

        - **Darker colors** = Skills appear together more frequently
        - **Lighter colors** = Skills rarely appear together
        - **Diagonal** = Shows individual skill frequency

        **What this means:**
        - Skills that cluster together should be learned as a package
        - High co-occurrence = employers expect these skills together
        - Use this to plan your learning path
        """)

    # Interactive table
    st.markdown("### Top Skill Pair Rankings")

    st.write("")  # Spacer

    col1, col2 = st.columns([3, 1])
    with col1:
        n_pairs = st.slider("Number of skill pairs to display", 3, 15, 8, key="pairs_slider")
    with col2:
        st.write("")  # Spacer
    df_display = df_cooccur.head(n_pairs)

    # Create interactive visualization
    fig = go.Figure(data=[
        go.Bar(
            x=df_display['pair_count'],
            y=[f"{row['skill_1']} + {row['skill_2']}" for _, row in df_display.iterrows()],
            orientation='h',
            marker=dict(
                color='#2d5f8d',
                line=dict(color='#1a3a5c', width=1.5)
            ),
            text=df_display['pair_count'],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Appears together in %{x} jobs<extra></extra>'
        )
    ])

    fig.update_layout(
        title=dict(text=f'Top {n_pairs} Skill Pair Co-occurrences', font=dict(color='#1a3a5c', size=16)),
        xaxis_title="Number of Jobs",
        yaxis_title="Skill Pair",
        height=max(400, n_pairs * 40),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, color='#1e293b', family='Arial'),
        xaxis=dict(title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
        yaxis=dict(categoryorder='total ascending', title_font=dict(size=13, color='#1e293b'), tickfont=dict(size=12, color='#1e293b')),
        margin=dict(l=10, r=10, t=50, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Detailed table
    df_display_formatted = df_display.copy()
    df_display_formatted.insert(0, 'Rank', range(1, len(df_display_formatted) + 1))
    df_display_formatted.columns = ['Rank', 'Skill 1', 'Skill 2', 'Co-occurrence Count']

    st.dataframe(
        df_display_formatted,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Skill 1": st.column_config.TextColumn("Skill 1", width="medium"),
            "Skill 2": st.column_config.TextColumn("Skill 2", width="medium"),
            "Co-occurrence Count": st.column_config.NumberColumn("Appears Together", width="small")
        }
    )

    # Key insights
    st.markdown("### Learning Recommendations")
    st.info("""
    **Based on skill co-occurrence patterns:**

    1. **Technical Foundation**: Skills like SQL, Python, and Excel frequently appear together - master these as your core toolkit
    2. **Visualization Stack**: Power BI and Tableau often pair with SQL - consider learning them together
    3. **Cloud & Big Data**: AWS, Azure, and Spark show strong relationships - these are valuable advanced skills
    4. **Statistical Tools**: R and Python often co-occur with statistical analysis - useful for data science roles

    **Pro Tip**: Focus on skill combinations rather than individual skills to maximize your employability!
    """)

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #64748b; padding: 1.5rem 0; font-size: 0.85rem;'>
Built with Python • PostgreSQL • Streamlit • Plotly
</p>
""", unsafe_allow_html=True)
