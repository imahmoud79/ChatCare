import requests

# === API KEYS ===
SERP_API_KEY = "e405fd1bb3abb711a25f58b2866be201b22964670891d72e412c23fc22d92159"
GROQ_API_KEY = "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"

# === SEARCH FUNCTION ===
def search_google(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY
    }

    response = requests.get(url, params=params)
    results = response.json()

    snippets = []
    for result in results.get("organic_results", []):
        if "snippet" in result:
            snippets.append(result["snippet"])
    
    return snippets

# === PROMPT BUILDER ===
def build_search_prompt(query, snippets):
    context = "\n".join(f"- {s}" for s in snippets)
    return f"""You are a helpful assistant. Based on the following internet search results, answer the question below.

Search Results:
{context}

Question: {query}
Answer:"""

# === CALL GROQ MODEL ===
def call_groq_model(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
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

    response = requests.post(url, headers=headers, json=payload)
    
    try:
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            print("API Error:", data)
            return "Error: 'choices' key missing in response."
    except Exception as e:
        print("Failed to parse response:", response.text)
        return f"Exception: {e}"

# === MAIN FLOW ===
def search_and_answer(query):
    #print(f"🔍 Searching for: {query}")
    snippets = search_google(query)
    if not snippets:
        return "No results found or SerpAPI error."

    prompt = build_search_prompt(query, snippets)
    # print("🤖 Asking Groq model...")
    return call_groq_model(prompt)

# === Example Usage ===
if __name__ == "__main__":
    question = "What ai"
    answer = search_and_answer(question)
    #print("\n💡 Answer from Groq model:\n", answer)


    # after the search result ask llm to do post processing 
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    from dotenv import load_dotenv
    import os

    # Load env
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    # Model
    llm = ChatGroq(
        api_key=groq_api_key,
        model="llama3-70b-8192",
        temperature=0.2,
        max_tokens=100,
    )

    # Prompt 
    prompt = answer + "format this answer and remove unneccesary descriptions"

    # Invoke
    response = llm.invoke(prompt)
    print("Answer:", response.content)


