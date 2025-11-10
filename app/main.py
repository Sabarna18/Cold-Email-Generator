# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader
# from chains import Chain
# from portfolio import Portfolio
# from utils import clean_text
# import pandas as pd

# def create_streamlit_app(llm , portfolio ,  clean_text):
#     st.title("📧 COLD EMAIL GENERATOR")
#     url_input = st.text_input(value="https://www.amazon.jobs/software-development?utm_source=chatgpt.com" , label= "Enter URL of any job posting page")
    

#     submit_btn = st.button("submit")
    
#     if submit_btn:
#         try:
#             loader = WebBaseLoader(url_input)
#             scraped_data = loader.load()
#             final_data = clean_text(scraped_data.pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(final_data)
            
#             for job in jobs:
#                 skills = job.get('skills' , [])
#                 st.write("Extracted skills:" , skills)
#                 links = portfolio.get_quiery(skills)
#                 email = llm.write_mail(job=job , links=links)
#                 st.code(email , language="markdown")
                        
#         except Exception as e:
#             st.error(f"An error occurred{e}")
            
# if __name__ == "__main__":
#     chain = Chain()  
#     uploaded_file = st.file_uploader("Upload your organization's portfolio in .csv" , type=["csv"])
    
#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
#         st.success(f"Portfolio uploaded successfully!{uploaded_file.name}")
#         st.subheader("🔍 Preview of Data")
#         st.dataframe(df.head())
#         portfolio = Portfolio(file_path=uploaded_file if uploaded_file is not None else "app/resources/my_portfolio.csv")
#         st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#         create_streamlit_app(chain , portfolio , clean_text)
#     else:
#         st.info("Please upload a CSV file to proceed.")  

            
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import pandas as pd
import os

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 COLD EMAIL GENERATOR")
    
    # Display which portfolio is being used
    st.info(f"Using portfolio: {portfolio.file_source}")
    
    url_input = st.text_input(
        value="https://www.amazon.jobs/software-development?utm_source=chatgpt.com",
        label="Enter URL of any job posting page"
    )
    
    submit_btn = st.button("submit")
    
    if submit_btn:
        try:
            loader = WebBaseLoader(url_input)
            scraped_data = loader.load()
            final_data = clean_text(scraped_data.pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(final_data)
            
            for job in jobs:
                skills = job.get('skills', [])
                st.write("Extracted skills:", skills)
                links = portfolio.get_quiery(skills)
                email = llm.write_mail(job=job, links=links)
                st.code(email, language="markdown")
                        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    chain = Chain()
    DEFAULT_PORTFOLIO_PATH = "app/resources/my_portfolio.csv"

    uploaded_file = st.file_uploader(
        "Upload your organization's portfolio in .csv (or use default)", 
        type=["csv"]
    )

    df = None

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Portfolio uploaded successfully! {uploaded_file.name}")
        st.subheader("🔍 Preview of Uploaded Data")
        st.dataframe(df.head())
    elif os.path.exists(DEFAULT_PORTFOLIO_PATH):
        df = pd.read_csv(DEFAULT_PORTFOLIO_PATH)
        st.info(f"ℹ️ Using default portfolio: {DEFAULT_PORTFOLIO_PATH}")
        st.subheader("🔍 Preview of Default Data")
        st.dataframe(df.head())
    else:
        st.warning(f"⚠️ Default portfolio file not found at: {DEFAULT_PORTFOLIO_PATH}")
        st.info("Please upload a CSV file to proceed.")

    if df is not None:
        portfolio = Portfolio(
            data=df,
            file_path=DEFAULT_PORTFOLIO_PATH,
            uploaded_file=uploaded_file
        )
        create_streamlit_app(chain, portfolio, clean_text)
