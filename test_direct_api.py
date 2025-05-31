#!/usr/bin/env python3
"""
Test script to compare direct Groq API calls vs. langchain wrapper
for different models (llama, deepseek, qwen)
"""

import os
import sys
import time
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from groq import Groq

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Groq API
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    groq_api_key = "gsk_NamlAyVEFhkxXjsN2lxdATpPGGXYZzY1Gx7v4BfN4TRLAhDq"  # Fallback API key

# Available models
MODELS = [
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "qwen-qwq-32b",
]

def test_langchain(model_name, system_prompt, messages):
    """Test model using langchain wrapper"""
    start_time = time.time()
    try:
        llm = ChatGroq(
            api_key=groq_api_key,
            model=model_name,
            temperature=0.7,
            max_tokens=50,  # Reduced tokens for faster response
            timeout=20,
            max_retries=1,
        )
        
        # Format messages for langchain
        langchain_messages = [
            SystemMessage(content=system_prompt),
        ]
        
        # Add conversation history
        for role, content in messages:
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
        
        # Invoke model
        response = llm.invoke(langchain_messages)
        elapsed = time.time() - start_time
        logger.info(f"LangChain ({model_name}) response time: {elapsed:.2f}s")
        logger.info(f"LangChain response: {response.content[:50]}...")
        return {
            "success": True,
            "content": response.content,
            "elapsed": elapsed
        }
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"LangChain ({model_name}) error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "elapsed": elapsed
        }

def test_direct_api(model_name, system_prompt, messages):
    """Test model using direct Groq API call"""
    start_time = time.time()
    try:
        client = Groq(api_key=groq_api_key)
        
        # Format messages for Groq API
        groq_messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for role, content in messages:
            if role in ["user", "assistant"]:
                groq_messages.append({"role": role, "content": content})
        
        # Make API call
        response = client.chat.completions.create(
            model=model_name,
            messages=groq_messages,
            max_tokens=50,  # Reduced tokens for faster response
            temperature=0.7,
            timeout=20
        )
        
        elapsed = time.time() - start_time
        content = response.choices[0].message.content
        logger.info(f"Direct API ({model_name}) response time: {elapsed:.2f}s")
        logger.info(f"Direct API response: {content[:50]}...")
        return {
            "success": True,
            "content": content,
            "elapsed": elapsed
        }
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Direct API ({model_name}) error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "elapsed": elapsed
        }

def test_model(model_name):
    """Test a specific model with both methods"""
    
    # Test parameters - simplified for quicker tests
    system_prompt = "You are a helpful assistant."
    messages = [
        ("user", "Tell me a quick joke.")
    ]
    
    print(f"\n=== Testing {model_name} ===")
    
    # Test with LangChain
    print(f"\nTesting with LangChain wrapper...")
    langchain_result = test_langchain(model_name, system_prompt, messages)
    
    # Test with direct API
    print(f"\nTesting with direct Groq API...")
    direct_result = test_direct_api(model_name, system_prompt, messages)
    
    # Print comparison
    print("\n--- Results ---")
    lc_status = "✅ SUCCESS" if langchain_result["success"] else f"❌ FAILED: {langchain_result['error']}"
    api_status = "✅ SUCCESS" if direct_result["success"] else f"❌ FAILED: {direct_result['error']}"
    
    print(f"LangChain: {lc_status}")
    print(f"Direct API: {api_status}")
    
    if langchain_result["success"] and direct_result["success"]:
        lc_time = langchain_result["elapsed"]
        api_time = direct_result["elapsed"]
        print(f"Time comparison: LangChain {lc_time:.2f}s vs Direct API {api_time:.2f}s")
    
    # Recommendations
    print("\n--- Recommendation ---")
    if not langchain_result["success"] and direct_result["success"]:
        print(f"For {model_name}, use direct Groq API instead of LangChain wrapper")
    elif langchain_result["success"] and not direct_result["success"]:
        print(f"For {model_name}, use LangChain wrapper instead of direct Groq API")
    elif not langchain_result["success"] and not direct_result["success"]:
        print(f"{model_name} appears to be unavailable or having issues with both methods")
    else:
        faster_method = "Direct API" if direct_result["elapsed"] < langchain_result["elapsed"] else "LangChain"
        print(f"Both methods work for {model_name}. {faster_method} is slightly faster.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test a specific model if provided
        model_name = sys.argv[1]
        if model_name in MODELS:
            test_model(model_name)
        else:
            print(f"Error: Unknown model '{model_name}'")
            print(f"Available models: {', '.join(MODELS)}")
    else:
        # No model specified, just test deepseek
        test_model("deepseek-r1-distill-llama-70b") 