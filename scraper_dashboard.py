import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import time

# Page config
st.set_page_config(
    page_title="Web Scraper Dashboard",
    page_icon="🕷️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🕷️ Web Scraper Dashboard")
st.markdown("Real-time data from **Hacker News** - Top tech stories and trends")

# Sidebar
st.sidebar.header("⚙️ Settings")
num_stories = st.sidebar.slider("Number of stories to fetch", 10, 100, 30)
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", False)

@st.cache_data(ttl=60)
def scrape_hackernews(limit=30):
    """Scrape Hacker News stories"""
    try:
        url = "https://news.ycombinator.com/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        stories = []
        titles = soup.find_all('span', class_='titleline')
        subtexts = soup.find_all('td', class_='subtext')
        
        for i, (title_span, subtext) in enumerate(zip(titles[:limit], subtexts[:limit])):
            try:
                title_link = title_span.find('a')
                title = title_link.text if title_link else "N/A"
                link = title_link['href'] if title_link else "#"
                
                # Get points and comments
                score_span = subtext.find('span', class_='score')
                points = int(score_span.text.split()[0]) if score_span else 0
                
                comments_link = subtext.find_all('a')[-1]
                comments_text = comments_link.text if comments_link else "0"
                comments = int(comments_text.split()[0]) if comments_text.split()[0].isdigit() else 0
                
                stories.append({
                    'rank': i + 1,
                    'title': title,
                    'link': link,
                    'points': points,
                    'comments': comments
                })
            except Exception as e:
                continue
        
        return stories, datetime.now()
    except Exception as e:
        st.error(f"Scraping error: {e}")
        return [], None

# Scrape data
with st.spinner("🔍 Scraping data..."):
    stories, last_updated = scrape_hackernews(num_stories)

if not stories:
    st.error("Failed to fetch data. Please try again.")
    st.stop()

# Convert to DataFrame
df = pd.DataFrame(stories)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Stories", len(df))
with col2:
    st.metric("⭐ Avg Points", f"{df['points'].mean():.0f}")
with col3:
    st.metric("💬 Total Comments", f"{df['comments'].sum():.0f}")
with col4:
    st.metric("🔥 Top Score", df['points'].max())

st.markdown(f"*Last updated: {last_updated.strftime('%H:%M:%S')}*")

# Tabs
tab1, tab2, tab3 = st.tabs(["📰 Stories", "📊 Analytics", "🔥 Top Stories"])

with tab1:
    st.subheader("Latest Stories")
    
    # Search filter
    search = st.text_input("🔍 Search stories", "")
    
    filtered_df = df[df['title'].str.contains(search, case=False, na=False)] if search else df
    
    # Display stories
    for _, row in filtered_df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                st.markdown(f"**{row['rank']}. [{row['title']}]({row['link']})**")
            with col2:
                st.markdown(f"⭐ {row['points']}")
            with col3:
                st.markdown(f"💬 {row['comments']}")
            st.divider()

with tab2:
    st.subheader("Data Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Points distribution
        fig_points = px.histogram(
            df, 
            x='points', 
            nbins=20,
            title="Points Distribution",
            color_discrete_sequence=['#FF6B35']
        )
        fig_points.update_layout(
            xaxis_title="Points",
            yaxis_title="Number of Stories",
            showlegend=False
        )
        st.plotly_chart(fig_points, use_container_width=True)
    
    with col2:
        # Comments vs Points scatter
        fig_scatter = px.scatter(
            df,
            x='points',
            y='comments',
            size='points',
            hover_data=['title'],
            title="Comments vs Points",
            color='points',
            color_continuous_scale='Viridis'
        )
        fig_scatter.update_layout(
            xaxis_title="Points",
            yaxis_title="Comments"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Top stories by engagement
    df['engagement'] = df['points'] + df['comments'] * 2
    top_engagement = df.nlargest(10, 'engagement')[['title', 'points', 'comments', 'engagement']]
    
    fig_bar = px.bar(
        top_engagement,
        x='engagement',
        y='title',
        orientation='h',
        title="Top 10 Stories by Engagement (Points + Comments×2)",
        color='engagement',
        color_continuous_scale='Blues'
    )
    fig_bar.update_layout(
        xaxis_title="Engagement Score",
        yaxis_title="",
        showlegend=False,
        height=500
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.subheader("🔥 Trending Stories")
    
    top_stories = df.nlargest(10, 'points')
    
    for idx, row in top_stories.iterrows():
        with st.container():
            st.markdown(f"### #{row['rank']} - {row['title']}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Points", row['points'])
            with col2:
                st.metric("Comments", row['comments'])
            with col3:
                st.markdown(f"[🔗 Read More]({row['link']})")
            st.divider()

# Download data
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Download CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f'hackernews_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
    mime='text/csv'
)

# Auto-refresh
if auto_refresh:
    time.sleep(30)
    st.rerun()