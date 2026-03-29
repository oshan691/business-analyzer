import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="AQW Analytical Architect", layout="wide", page_icon="📊")

# 2. Advanced Custom CSS (Interface එකේ පෙනුම සඳහා)
st.markdown("""
    <style>
    /* මුළු පිටුවේම පසුබිම */
    .stApp { background-color: #F8FAFC; }
    
    /* කාඩ් එකක මූලික හැඩය */
    .metric-card {
        background-color: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .metric-title { color: #64748B; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { color: #0F172A; font-size: 32px; font-weight: 700; margin: 8px 0; }
    .metric-delta { font-size: 14px; font-weight: 600; }
    .delta-up { color: #10B981; } /* Green */
    
    /* Anomaly Detected Card (Mint Color) */
    .anomaly-card {
        background-color: #CCFBF1;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #99F6E4;
        margin-top: 20px;
    }
    
    /* Navigation Bar (යට තියෙන එක) */
    .nav-bar {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        padding: 10px 30px;
        border-radius: 40px;
        display: flex;
        gap: 40px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    
    /* Sidebar අයින් කිරීම සහ Clean පෙනුමක් ලබා දීම */
    section[data-testid="stSidebar"] { width: 0px !important; display: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. Header (AQW Logo & Profile)
col_logo, col_profile = st.columns([10, 1])
with col_logo:
    st.markdown("### 📊 **AQW**")
with col_profile:
    st.markdown("👤")

# 5. Top Stats (Revenue, Users, Reports)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Total Revenue Annualized</div>
        <div class="metric-value">$42.8M</div>
        <div class="metric-delta delta-up">↗ +12.4% VS PREV. YEAR</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Active Users</div>
        <div class="metric-value">842.1k</div>
        <div class="metric-delta delta-up">👤 +4.1K TODAY</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-title">Processing Reports</div>
        <div class="metric-value">18</div>
        <div class="metric-delta" style="color:#6366F1;">🔄 6 HIGH PRIORITY</div>
    </div>""", unsafe_allow_html=True)

# 6. Regional Insights Table
st.markdown("#### Regional Insights")
data = {
    "REGION": ["North Am.", "EU West", "APAC Hub"],
    "GROWTH": ["+18.2%", "+6.4%", "-2.1%"],
    "LIQUIDITY": ["$2.4B", "$1.9B", "$840M"],
    "RISK SCORE": ["LOW", "MOD", "HIGH"]
}
df_display = pd.DataFrame(data)
st.table(df_display)

# 7. Anomaly Section
st.markdown(f"""<div class="anomaly-card">
    <h4 style="color:#0D9488; margin:0;">⚡ Anomaly Detected</h4>
    <p style="color:#134E48;">System AI identified a 14% deviation in APAC transaction volume within the last 4 hours.</p>
    <button style="background-color:#5EEAD4; border:none; padding:10px 20px; border-radius:10px; font-weight:bold; cursor:pointer;">VIEW DIAGNOSTIC →</button>
</div>""", unsafe_allow_html=True)

# 8. File Upload & Chat Area
st.markdown("---")
uploaded_file = st.file_uploader("ඔබේ ව්‍යාපාරික දත්ත (CSV) අප්ලෝඩ් කරන්න", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data Synced: All global nodes synchronized.")
    
    # Chat Input (Bottom bar look)
    user_input = st.text_input("Ask AI Architect about your business...")
    if user_input:
        with st.spinner("Analyzing..."):
            response = model.generate_content(f"Business Data Context: {df.head(5).to_string()}\nQuestion: {user_input}")
            st.info(response.text)

# 9. Fake Bottom Navigation Bar (Visual only)
st.markdown("""
    <div class="nav-bar">
        <span title="Dash">🏠</span>
        <span title="Reports">📄</span>
        <span style="background-color:#1E293B; color:white; padding:8px; border-radius:12px;">✨</span>
        <span title="AI">💬</span>
        <span title="Settings">⚙️</span>
    </div>
    """, unsafe_allow_html=True)
