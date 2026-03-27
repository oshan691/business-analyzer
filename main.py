import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.express as px

# 1. Page Configuration (මේක මුලින්ම තියෙන්න ඕනේ)
st.set_page_config(page_title="Pro Business Analyzer", layout="wide", page_icon="📈")

# 2. Modern UI Design (CSS කොටස)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    .main-header { font-size: 36px; font-weight: bold; color: #1E293B; text-align: center; margin-bottom: 20px; }
    .stButton>button {
        background: linear-gradient(45deg, #6366F1, #4F46E5);
        color: white; border-radius: 12px; border: none; padding: 10px 24px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3); }
    [data-testid="stSidebar"] { background-color: #1E293B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Sidebar (මෙතනට ඔයාගේ Brand එක දාන්න පුළුවන්)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=100) # නිකන් icon එකක්
    st.title("Business Solutions")
    st.markdown("---")
    uploaded_file = st.file_uploader("ඔබේ දත්ත ගොනුව මෙතනට දමන්න", type=['csv', 'xlsx'])
    st.info("Developed by Nirmala's Workspace")

# 5. Main Dashboard
st.markdown("<div class='main-header'>📊 Advanced Business Intelligence AI</div>", unsafe_allow_html=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # දත්ත විශ්ලේෂණ කොටස
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("දත්ත පෙරදසුන (Data Preview)")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("ක්ෂණික සංඛ්‍යාලේඛන")
        st.metric("මුළු දත්ත පේළි ගණන", len(df))
        st.metric("තීරු (Columns) ගණන", len(df.columns))

    # Chart
    st.markdown("---")
    st.subheader("📈 ව්‍යාපාරික ප්‍රස්ථාර (Visualizations)")
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) >= 1:
        fig = px.area(df, y=numeric_cols[0], title=f"{numeric_cols[0]} කාලය අනුව වෙනස් වීම")
        st.plotly_chart(fig, use_container_width=True)

    # AI Insights Button
    if st.button("🪄 AI මගින් දත්ත විශ්ලේෂණය කරන්න"):
        with st.spinner("AI එක දත්ත කියවමින් පවතී..."):
            context = df.head(20).to_string()
            response = model.generate_content(f"Analyze this business data and provide 3 expert growth tips in Sinhala and English: {context}")
            st.success("විශ්ලේෂණය අවසන්!")
            st.markdown(f"### ✨ AI Insights\n{response.text}")
else:
    st.markdown("<br><br><center><h3>ආරම්භ කිරීමට වම් පසින් ඇති Sidebar එක හරහා CSV හෝ Excel ගොනුවක් අප්ලෝඩ් කරන්න.</h3></center>", unsafe_allow_html=True)
