import requests
import os

# Set your Groq API Key
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Fake knowledge base
documents = [
    {"title": "Python", "content": "Python is a programming language that lets you work quickly and integrate systems more effectively."},
    {"title": "LangChain", "content": "LangChain is a framework for developing applications powered by language models."},
    {"title": "Groq", "content": "Groq offers super fast inference for large language models like LLaMA."}
]

# Simple retriever
def retrieve_documents(query):
    return [doc for doc in documents if query.lower() in doc['content'].lower() or query.lower() in doc['title'].lower()]

# Simple prompt
def build_prompt(query, retrieved_docs):
    context = "\n\n".join(f"{doc['title']}: {doc['content']}" for doc in retrieved_docs)
    return f"""You are an AI assistant. Use the context below to answer the question.

Context:
{context}

Question: {query}
Answer:"""

# Invoke Groq model
def call_groq_model(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# === Example RAG call ===
query = "What is LangChain?"
retrieved = retrieve_documents(query)
final_prompt = build_prompt(query, retrieved)
answer = call_groq_model(final_prompt)

print("Answer:", answer)
