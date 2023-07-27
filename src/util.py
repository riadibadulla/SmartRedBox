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
import api_keys

#anthropic
import anthropic
import PyPDF2
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


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

def summary_with_claude(fine_name='regulations.pdf'):
    Anthropic(api_key=api_keys.API_CLAUDE)
    with open(fine_name, 'rb') as pdf_file:
        # Initialize a PDF file reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize a string to hold all the text
        pdf_text = ''

        # Loop through each page in the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the text from the page and add it to the total text
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()

    # Now `pdf_text` contains all the text from the PDF
    prompt = " '"+pdf_text+"' summarise this document "


    res = anthropic_client.completions.create(prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}", model="claude-v1.3-100k", max_tokens_to_sample=40000)

    return res.completion

    def analyze_sentiment(text):
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other engines like "text-curie-003"
            prompt=f"The following text is: '{text}'. The sentiment of this text is",
            temperature=0.3,
            max_tokens=60
        )

        return response.choices[0].text.strip()

    # Test the sentiment analysis
    text = "I am very happy today!"
    sentiment = analyze_sentiment(text)
    print(f'The sentiment is: {sentiment}')