# rag_setup_groq.py

import os
import sys
import shutil
import torch
import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from googlesearch import search

# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# === Define fallback data ===
FALLBACK_DATA = """
Feeling sad? Practice deep breathing to regulate emotions or journal your thoughts to process them.
Stressed out? Try progressive muscle relaxation or a brief mindfulness exercise to reduce tension.
Anxious? Use grounding techniques like the 5-4-3-2-1 method to stay present.
Low energy? Take a short walk or hydrate to boost your mood gently.
Overwhelmed? Break tasks into small steps and focus on one at a time.
Angry? Practice slow breathing and reflect on triggers to manage your response.
"""

# === Web content fetching ===
def fetch_web_content(query, num_results=3):
    try:
        web_texts = []
        for url in search(query + " site:*.edu | site:*.org | site:*.gov -inurl:(signup | login)", num_results=num_results):
            response = requests.get(url, timeout=5, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join(p.get_text() for p in soup.find_all("p"))
            text = re.sub(r'(Home|Contact Us|Quick Links|More »|Courses|Online|PD Hours|\|)', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > 50:
                web_texts.append(text[:300])
        result = " ".join(web_texts)
        if not result:
            print("Web fetch empty—using fallback data.")
            return FALLBACK_DATA
        print(f"Web fetched: {result[:100]}...")
        return result
    except Exception as e:
        print(f"Web search failed: {e}—using fallback data.")
        return FALLBACK_DATA

# === Setup vector store ===
def setup_vector_store(data_file="mental_health_data.txt", use_web=False, web_query="mental health coping strategies"):
    persist_dir = "./chroma_db_web" if use_web else "./chroma_db_local"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    if use_web:
        print("Fetching mental health strategies from the web...")
        text = fetch_web_content(web_query)
    else:
        if os.path.exists(data_file):
            print(f"Using local data from {data_file}...")
            with open(data_file, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            print("No local data—using fallback strategies.")
            text = FALLBACK_DATA

    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50, separator="\n", length_function=len)
    chunks = splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(chunks, embeddings, persist_directory=persist_dir)
    print(f"Vector store initialized with {len(chunks)} chunks.")
    return vector_store

# === LLM using Groq ===
llm = ChatGroq(
    api_key=groq_api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7,
    max_tokens=1000,
)

# === Prompt Template for JSON output ===
structured_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful mental health assistant. Based on the following context, answer the user's question.

Context:
{context}

Question:
{question}

Respond ONLY in JSON format like:
{{
  "answer": "your structured response here",
  "guideline": "provide the answer in an empathic and emotionally supportive way"
}}
"""
)

# === Setup Vector Store ===
use_web = "--web" in sys.argv
vector_store = setup_vector_store(use_web=use_web)

# === Output Parser ===
# parser = JsonOutputParser()

# === Create RAG Chain ===
# === Create RAG Chain ===
def create_rag_chain():
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        input_key="question",
        chain_type="stuff",
        chain_type_kwargs={"prompt": structured_prompt},
        return_source_documents=False
    )
    return chain  # ⬅️ no parser piping here


# === Main Interaction ===
if __name__ == "__main__":
    print(f"Welcome! I'm your AI mental health assistant powered by Groq & LLaMA. Ask me anything!")

    user_input = "What can I do if I feel constantly stressed?"

    rag_chain = create_rag_chain()


    if user_input.lower() in ["exit", "quit"]:
        print("Take care! I'm here whenever you need support.")
    else:
        try:
            raw_response = rag_chain.invoke(user_input)
            #parsed_response = parser.parse(raw_response)  # 👈 manually parse here
            print("Answer:", raw_response)
        except Exception as e:
            print("Error:", e)
