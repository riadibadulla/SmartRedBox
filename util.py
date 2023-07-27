import langchain
from langchain.llms import OpenAI
# from langchain.llms.claude import Claude
from pdfminer.high_level import extract_text
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import openai
from langchain.chains.summarize import load_summarize_chain
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter

def summarise(path_to_pdf = 'data/a_pro-innovation_approach_to_AI_regulation.pdf'):
    llm = OpenAI(temperature=0) 
    # llm = Claude()

    # Extract text from PDF
    pdf_path = path_to_pdf
    text = extract_text(pdf_path)


    text_splitter = TokenTextSplitter(chunk_size= 4000 - 256, chunk_overlap=0)

    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]



    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)