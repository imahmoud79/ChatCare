#!/usr/bin/env python3
"""
Simple test script for Groq models using direct API
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq API
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    groq_api_key = "gsk_NamlAyVEFhkxXjsN2lxdATpPGGXYZzY1Gx7v4BfN4TRLAhDq"  # Fallback API key

# Initialize the Groq client
client = Groq(api_key=groq_api_key)

def test_model(model_name):
    """Test if a model works with a simple message"""
    print(f"\nTesting {model_name}...")
    try:
        # Simple messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one short sentence."}
        ]
        
        # Make API call
        print("Sending request...")
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=20,  # Very short response
            temperature=0.7
        )
        
        # Print response
        content = response.choices[0].message.content
        print(f"SUCCESS! Response: {content}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

# Test the models
print("=== Testing Groq Models ===")
print(f"Using API key: {groq_api_key[:5]}...{groq_api_key[-4:]}")

# Test llama first as a baseline
test_model("llama-3.3-70b-versatile")

# Test the problematic models
test_model("deepseek-r1-distill-llama-70b")
test_model("qwen-qwq-32b")

print("\nDone!") 