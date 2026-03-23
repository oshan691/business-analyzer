import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import os

import streamlit as st

# පිටුවේ සැකසුම් (Page Config)
st.set_page_config(page_title="Data Engine AI", layout="wide")

# අති නවීන UI එක සඳහා CSS
st.markdown("""
    <style>
    /* මුළු පිටුවේම පසුබිම */
    .stApp {
        background-color: #F8F9FC;
    }

    /* Sidebar එක අලුත් ඩිසයින් එකට සැකසීම */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* Sidebar අකුරු */
    [data-testid="stSidebar"] .stMarkdown p {
        color: #4A5568;
        font-weight: 500;
    }

    /* ප්‍රධාන කාඩ් එක (Main Container) */
    .main .block-container {
        padding: 3rem;
        max-width: 1100px;
    }

    /* Buttons - පින්තූරයේ ඇති වයලට් පාටට හුරු කිරීම */
    .stButton>button {
        background-color: #6366F1;
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #4F46E5;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }

    /* Metrics (ඉලක්කම් පෙන්වන කාඩ්ස්) */
    [data-testid="stMetricValue"] {
        color: #1A202C;
        font-size: 2rem !important;
    }
    
    /* Input Box */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Gemini API සම්බන්ධ කිරීම
# සටහන: Streamlit Cloud එකේදී මෙය 'Secrets' හරහා ලබාගත හැක
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    st.error("කරුණාකර Gemini API Key එක Secrets වල ඇතුළත් කරන්න.")

# 3. ප්‍රධාන Header එක
st.title("📊 Pro Business Insights AI")
st.write("ඔබේ ව්‍යාපාරික දත්ත ඇතුළත් කර AI මගින් ගැඹුරු විශ්ලේෂණයක් ලබා ගන්න.")

# 4. Sidebar - දත්ත ලබා ගැනීම
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("ඔබේ CSV හෝ Excel ගොනුව මෙතනට දමන්න", type=['csv', 'xlsx'])
    st.divider()
    st.write("Developed by Nirmala's Workspace")

# 5. ප්‍රධාන වැඩ කොටස
if uploaded_file is not None:
    # දත්ත කියවීම (Reading Data)
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # UI එක කොටස් දෙකකට බෙදීම
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("📋 දත්ත පෙරදසුන (Data Preview)")
        st.dataframe(df.head(10), use_container_width=True)
        
        # සරල Chart එකක් පෙන්වීම
        st.subheader("📊 ක්ෂණික ප්‍රස්ථාරය")
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if len(num_cols) >= 1:
            fig = px.line(df, y=num_cols[0], title=f"{num_cols[0]} කාලයත් සමඟ වෙනස් වීම")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🤖 AI ව්‍යාපාරික විශ්ලේෂණය")
        
        # විශේෂිත ප්‍රශ්නයක් ඇසීමට
        custom_query = st.text_input("විශේෂයෙන් දැනගත යුතු දෙයක් තියෙනවාද? (උදා: ලබන මාසයේ විකුණුම් කොහොම වෙයිද?)")
        
        if st.button("Analyze with Gemini"):
            with st.spinner('Gemini දත්ත පරීක්ෂා කරමින් පවතී...'):
                # දත්ත වල සාරාංශයක් සාදා Prompt එක සැකසීම
                data_str = df.describe().to_string()
                prompt = f"""
                You are a professional business consultant. Analyze this data summary:
                {data_str}
                User question: {custom_query if custom_query else "Provide 3 key insights and 3 growth strategies based on this data."}
                Answer in a professional and easy-to-understand way.
                """
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.success("විශ්ලේෂණය අවසන්!")
                st.markdown(response.text)

else:
    # මුලින්ම පෙන්වන පණිවිඩය
    st.info("පටන් ගැනීමට වම්පස ඇති Sidebar එකෙන් ඔබේ ව්‍යාපාරික දත්ත (Sales/Expenses) ගොනුව Upload කරන්න.")
    
    # පාරිභෝගිකයාට Demo එකක් ලෙස පෙන්වීමට static image එකක් හෝ විස්තරයක්
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=1000", caption="Business Intelligence Dashboard Demo")
