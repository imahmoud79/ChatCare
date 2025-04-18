from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.2,
    max_tokens=900,
)

# Prompt Template
prompt = ChatPromptTemplate.from_template("""
You are a helpful mental health assistant. Based on the following context, answer the user's question.

Context:
{context}

Question:
{question}

Respond ONLY in JSON format like:
{{
  "answer": "your structured response here",
  "guideline": "a short, emotionally supportive principle or recommendation (not a repetition of this instruction)"
}}
""")

# Output parser
parser = JsonOutputParser()

# Create chain
chain = prompt | llm | parser

# Provide test input (as a list for batch processing)
input_data_list = [
    {
        "context": "People often feel overwhelmed by work, school, or personal relationships.",
        "question": "What can I do if I feel constantly stressed?",
        "question": "give me guideline"

    }
]

# Run chain in batch mode
responses = chain.batch(input_data_list)

# Print results
print("\n=== batch() Responses ===")
for i, response in enumerate(responses):
    print(f"\nResponse {i + 1}")
    print("Answer:", response["answer"])
    print("Guideline:", response["guideline"])
