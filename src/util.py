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
import os
from langchain.docstore.document import Document
import pandas as pd
import api_keys

#anthropic
import anthropic
import PyPDF2
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

api_key = os.getenv("OPENAI_API_KEY")
def summarise(path_to_pdf = 'data/a_pro-innovation_approach_to_AI_regulation.pdf'):
    llm = OpenAI(temperature=0, openai_api_key=api_key) 
    # llm = Claude()

    # Extract text from PDF
    pdf_path = path_to_pdf
    text = extract_text(pdf_path)

    text_splitter = TokenTextSplitter(chunk_size= 4000 - 256, chunk_overlap=0)

    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)

def fake_data():
    data = {
    'Headline': ['AI regulation: pro-innovation, responsible growth.', 'Event 1', 'Event 1', 'Event 1'],
    'Sentiment': [1, 1, -1, 3],
    'Date': ['2020-01-01', '2021-03-01', '2022-04-01', '2022-05-01'],
    'Relevance': [0.7, 0.4, 0.8, 0.95],
    'Color': ['blue', 'blue', 'red', 'green'],
    'Topic' :['Submissions', 'Submissions', 'Internal sources', 'Public'],
    'Summary': [
    ' The UK government has proposed a new AI regulatory framework that includes five values-focused cross-sectoral principles to guide regulator responses to AI risks and opportunities. This framework is designed to provide clarity and coherence to the AI regulatory landscape, build the evidence base, and ensure risks are identified and addressed while also supporting innovation. It includes a set of functions to support implementation of the framework, such as monitoring, assessment and feedback, and cross-sectoral risk assessment. The government has opened a consultation to receive feedback from stakeholders, and plans to establish a regulatory sandbox for AI and engage with the public to build trust in the technology.', 
    'something', 'else', 'else']
    }
    return pd.DataFrame(data)

def get_related_data(submission):
    # return data from Luke
    related_data = None
    if related_data is None:
        related_data = fake_data()
    return related_data


def get_position(submission):
    position = None
    # do something
    if position is None:
        position = 'We do not have any position on this submission at the moment.'
    return position

def doc_to_json(path):
    system="""
    You are an AI assistant that converts document text into valid json in the following format:

    {
        "Type": <type of document, this could be an email, meeting minutes, submission>,
        "Title": <title of the document>,
        "Topic": <overall topic discussed in the document>,
        "Summary": <summary of the document content>,
        "Content": null,
        "Relevant People": <list of people mentioned in the document, inlcuding sender and recipients, format as: Forname Surname>,
        "Director": <director mentioned in the document>,
        "Team": <teams mentioned in the document that need to give clearance, where a name is provided>,
        "Sentiment": <sentiment analysis of the document, should be a floating point number between -1.00 and 1.00, with -1.00 being negative and 1.00 being positive and 0.00 being neutral, must be filled>,
        "Deadline": <deadline of any actions mentioned in the document, format as exactly as shown in the document>,
        "Actions": <any follow-up actions mentioned in the document, with added deadline as per "Deadline" field>,
        "Notes": <any notes attached to the document>,
        "Date": <date of the document in the format: YYYY-MM-DD, if no date is found then null>
    }

    You must extract this information from the document accuractly.
    """

    prompt = extract_text(path)

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
    )

    print(response['choices'][0]['message']['content'])

def summary_with_claude(fine_name='regulations.pdf'):
    print(f'The sentiment is: {sentiment}')