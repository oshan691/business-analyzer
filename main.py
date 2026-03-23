import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Data Engine v2.4.0", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fc; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .insight-card { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 5px solid #7b2cbf; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("Data Engine")
    st.caption("v2.4.0-pro")
    st.button("＋ New Analysis", use_container_width=True)
    st.markdown("---")
    st.write("💬 Recent Chats")
    st.write("🗄️ SQL Sources")
    st.write("📊 Dashboards")
    st.write("📁 CSV Uploads")
    st.spacer()
    st.write("⚙️ Settings")

# --- Main Header ---
st.title("Q3 Financial Deep-Dive")
st.write("Orchestrated analysis of current market trends and internal performance metrics.")

# --- Layout: Main Content & Live Insights ---
col1, col2 = st.columns([3, 1])

with col1:
    # User Query Mockup
    st.info("**User:** Can you analyze our Q3 revenue growth and compare it with North America and Europe?")
    
    # Intelligence Engine Response
    with st.container():
        st.markdown("### ✨ INTELLIGENCE ENGINE")
        st.write("I've analyzed the Q3 datasets. Revenue grew by **12.4%** compared to Q2. The primary driver was the Enterprise sector in North America.")
        
        # Creating the Chart (July, Aug, Sep, NA, EU)
        months = ['JUL', 'AUG', 'SEP', 'NA', 'EU']
        values = [40, 55, 65, 30, 35]
        colors = ['#1a1c2c', '#1a1c2c', '#7b2cbf', '#e0e1dd', '#e0e1dd']
        
        fig = go.Figure(data=[go.Bar(x=months, y=values, marker_color=colors)])
        fig.update_layout(
            height=300, 
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("Growth Index: +12.4% | **Positive Trend**")

with col2:
    # Live Insights Panel
    st.markdown("""
    <div class="insight-card">
        <h4 style="color: #7b2cbf;">⚡ Live Insights</h4>
        <p style="color: red; font-size: 0.8em;"><b>ANOMALIES DETECTED</b><br>Sudden drop in EU retail conversion (-8%)</p>
        <hr>
        <p style="font-size: 0.8em;"><b>RECOMMENDED ACTION</b><br>Re-allocate marketing budget from Mid-Market to Enterprise.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Bottom Chat Bar ---
st.markdown("---")
query = st.text_input("Ask Orchestrated Intelligence to analyze your data...", placeholder="Predict Q4 churn rate...")
