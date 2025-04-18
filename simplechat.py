"""
Scenario: Filtering Messages in a Chatbot
Imagine you're building a chatbot that interacts with users. 
The system keeps track of various types of messages, but before sending 
them to the Groq model, we filter only user (HumanMessage) 
and assistant (AIMessage) responses.
"""

import os
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, filter_messages
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq API
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    max_tokens=32767,
    timeout=10,
    max_retries=2,
)

# Define a list of messages
messages = [
    SystemMessage(content="You are a helpful chatbot.", id="sys1"),
    HumanMessage(content="Hello, can you help me?", id="user1", name="John"),
    AIMessage(content="Of course! What do you need help with?", id="ai1", name="ChatBot"),
    HumanMessage(content="What is the capital of France?", id="user2", name="John"),
    AIMessage(content="The capital of France is Paris.", id="ai2", name="ChatBot"),
]

# Filter messages: Only include HumanMessage and AIMessage
filtered_messages = filter_messages(messages, include_types=[HumanMessage, AIMessage])

# Pass filtered messages to Groq model
response = llm.invoke(filtered_messages)

# Print the filtered messages and response
print("\n--- Filtered Messages ---")
for msg in filtered_messages:
    print(f"{msg.name}: {msg.content}")

print("\n--- Groq Model Response ---")
print(response)