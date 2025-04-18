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

# Prompt (ask to respond in JSON)
prompt = ChatPromptTemplate.from_template("Answer the following in JSON format with an 'answer' key: What is the capital of Japan?")

# Use JsonOutputParser
parser = JsonOutputParser()

# Chain
chain = prompt | llm | parser

# Invoke
response = chain.invoke({})
print("Answer:", response["answer"])