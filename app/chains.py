import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

class Chain():
    
    def __init__(self):
        self.llm = ChatGroq(api_key=api_key , temperature=0.4 , model="llama-3.3-70b-versatile")
    
    def extract_jobs(self , cleaned_text):
        
        prompt_extract = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant in Data Extraction Tasks"),
        ("human", """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """),
    ])

        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={"page_data" : cleaned_text})
        
        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise ("Context too big. Unable to parse jobs")
        return response if isinstance(response , list) else [response]
            
        
    def write_mail(self , job , links):
        prompt_extract = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant in Email generation"),
        ("human", """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Sabarna, a business development executive at Core.sabarna. Core.sabarna is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Core.sabarna 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Core.Sabarna's portfolio: {link_list}
            Remember you are Sabarna, BDE at Core.sabarna. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            
            """),
    ])

        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={"job_description" : str(job),
                                            "link_list" : links})
        final_email = response.content
        return final_email
                