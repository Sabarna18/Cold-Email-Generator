import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import pandas as pd
import os

# Custom CSS for enhanced UI
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding-top: 1rem;
        }
        
        /* Title styling */
        .main-title {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            text-align: center;
            color: #718096;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: bold;
            font-size: 1.1rem;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Input fields styling */
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Card styling */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        
        .email-card {
            background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            margin: 1.5rem 0;
            border: 1px solid #e2e8f0;
        }
        
        .skill-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            margin: 0.3rem;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        /* File uploader styling */
        .uploadedFile {
            border-radius: 10px;
        }
        
        /* Section headers */
        .section-header {
            color: #2d3748;
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Info/Warning/Success boxes */
        .stAlert {
            border-radius: 10px;
            border-left-width: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_streamlit_app(llm, portfolio, clean_text):
    # Header Section
    st.markdown('<h1 class="main-title">📧 COLD EMAIL GENERATOR</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Generate personalized cold emails for job postings using AI</p>', unsafe_allow_html=True)
    
    # Display portfolio info in a styled card
    st.markdown(f"""
        <div class="info-card">
            <strong style="color: #667eea;">📁 Active Portfolio:</strong> 
            <span style="color: #2d3748;">{portfolio.file_source}</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input Section with columns for better layout
    st.markdown('<h2 class="section-header">📝 Input Details</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_input = st.text_input(
            label="🔗 Job Posting URL",
            value="https://www.amazon.jobs/software-development?utm_source=chatgpt.com",
            help="Paste the URL of the job posting page you want to target"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        sender_name = st.text_input(
            label="👤 Your Name",
            value="Your name",
            help="Enter your full name"
        )
    
    with col2:
        organization_name = st.text_input(
            label="🏢 Organization Name",
            value="Your organization name",
            help="Enter your company or organization name"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_btn = st.button("✨ Generate Email")
    
    st.markdown("---")
    
    if submit_btn:
        try:
            with st.spinner("🔄 Analyzing job posting and generating email..."):
                loader = WebBaseLoader(url_input)
                scraped_data = loader.load()
                final_data = clean_text(scraped_data.pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(final_data)
            
            st.markdown('<h2 class="section-header">📨 Generated Emails</h2>', unsafe_allow_html=True)
            
            for idx, job in enumerate(jobs, 1):
                skills = job.get('skills', [])
                
                # Display job info
                st.markdown(f"### 💼 Job Position {idx}")
                
                # Display skills as badges
                if skills:
                    st.markdown("**Required Skills:**")
                    skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in skills])
                    st.markdown(f'<div>{skills_html}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Generate email
                links = portfolio.get_quiery(skills)
                email = llm.write_mail(job=job, links=links, sender_name=sender_name, organization_name=organization_name)
                
                # Display email in styled card
                st.markdown('<div class="email-card">', unsafe_allow_html=True)
                st.markdown("**📧 Generated Cold Email:**")
                st.code(email, language="markdown")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
            
            st.success("✅ All emails generated successfully!")
                        
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.info("💡 Tip: Make sure the URL is valid and accessible.")

if __name__ == "__main__":
    st.set_page_config(
        layout="wide", 
        page_title="Cold Email Generator", 
        page_icon="📧",
        initial_sidebar_state="expanded"
    )
    
    load_custom_css()
    
    chain = Chain()
    DEFAULT_PORTFOLIO_PATH = "app/resources/my_portfolio.csv"

    # Sidebar for portfolio upload
    with st.sidebar:
        st.markdown("### 📂 Portfolio Management")
        st.markdown("---")
        
        uploaded_file = st.file_uploader(
            "Upload Portfolio CSV", 
            type=["csv"],
            help="Upload your organization's portfolio or use the default one"
        )
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.info("""
            - Ensure your portfolio CSV has the required columns
            - Use valid job posting URLs
            - Personalize your name and organization
        """)

    df = None

    # Main content area for portfolio preview
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Portfolio uploaded successfully: **{uploaded_file.name}**")
        
        with st.expander("🔍 Preview Uploaded Portfolio Data", expanded=False):
            st.dataframe(df.head(), use_container_width=True)
            st.caption(f"Showing first {min(5, len(df))} rows of {len(df)} total entries")
            
    elif os.path.exists(DEFAULT_PORTFOLIO_PATH):
        df = pd.read_csv(DEFAULT_PORTFOLIO_PATH)
        st.info(f"ℹ️ Using default portfolio: `{DEFAULT_PORTFOLIO_PATH}`")
        
        with st.expander("🔍 Preview Default Portfolio Data", expanded=False):
            st.dataframe(df.head(), use_container_width=True)
            st.caption(f"Showing first {min(5, len(df))} rows of {len(df)} total entries")
            
    else:
        st.warning(f"⚠️ Default portfolio file not found at: `{DEFAULT_PORTFOLIO_PATH}`")
        st.info("📤 Please upload a CSV file using the sidebar to proceed.")

    if df is not None:
        portfolio = Portfolio(
            data=df,
            file_path=DEFAULT_PORTFOLIO_PATH,
            uploaded_file=uploaded_file
        )
        create_streamlit_app(chain, portfolio, clean_text)
    else:
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #718096;">
                <h3 style="color: #4a5568;">👆 Upload a portfolio CSV to get started</h3>
                <p>Once uploaded, you'll be able to generate personalized cold emails!</p>
            </div>
        """, unsafe_allow_html=True)