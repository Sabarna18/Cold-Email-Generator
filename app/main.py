import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm , portfolio , clean_text):
    st.title("📧 COLD EMAIL GENERATOR")
    url_input = st.text_input(value="https://www.amazon.jobs/software-development?utm_source=chatgpt.com" , label= "Enter URL")
    submit_btn = st.button("submit")
    
    if submit_btn:
        try:
            loader = WebBaseLoader(url_input)
            scraped_data = loader.load()
            final_data = clean_text(scraped_data.pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(final_data)
            
            for job in jobs:
                skills = job.get('skills' , [])
                st.write("Extracted skills:" , skills)
                links = portfolio.get_quiery(skills)
                email = llm.write_mail(job=job , links=links)
                st.code(email , language="markdown")
                        
        except Exception as e:
            st.error(f"An error occurred{e}")
            
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain , portfolio , clean_text)
            