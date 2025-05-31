import os
import sys
import logging
import time
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Groq API
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    groq_api_key = "gsk_NamlAyVEFhkxXjsN2lxdATpPGGXYZzY1Gx7v4BfN4TRLAhDq"  # Fallback API key

# Model-specific configurations
MODEL_CONFIGS = {
    "llama-3.1-8b-instant": {
        "max_tokens": 8192,
        "context_window": 128000,
        "timeout": 30,
        "rate_limit_tokens": 50000  # Higher rate limits
    },
    "llama3-8b-8192": {
        "max_tokens": 8192,
        "context_window": 8192,
        "timeout": 30,
        "rate_limit_tokens": 6000  # Lower rate limits
    },
    "llama-3.3-70b-versatile": {
        "max_tokens": 32767,
        "context_window": 128000,
        "timeout": 60,
        "rate_limit_tokens": 10000  # Medium rate limits
    }
}

def get_model_config(model_name):
    """Get configuration for a specific model"""
    return MODEL_CONFIGS.get(model_name, {
        "max_tokens": 32767,  # Default values
        "context_window": 32767,
        "timeout": 60
    })

def test_model(model_name):
    """Test a specific model's availability and functionality"""
    logger.info(f"Testing model: {model_name}")
    
    try:
        # Get model configuration
        model_config = get_model_config(model_name)
        
        # Initialize the model
        llm = ChatGroq(
            api_key=groq_api_key,
            model=model_name,
            temperature=0.7,
            max_tokens=min(100, model_config["max_tokens"]),  # Use smaller tokens for testing
            timeout=model_config["timeout"],
            max_retries=3
        )
        
        # Test message
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Say hello and tell me what model you are.")
        ]
        
        # Time the response
        start_time = time.time()
        response = llm.invoke(messages)
        end_time = time.time()
        
        # Log results
        logger.info(f"Model {model_name} response time: {end_time - start_time:.2f} seconds")
        logger.info(f"Response: {response.content}")
        
        return True
    except Exception as e:
        logger.error(f"Error testing model {model_name}: {str(e)}")
        return False

def main():
    # Test all models
    models = [
        "llama-3.1-8b-instant",
        "llama3-8b-8192",
        "llama-3.3-70b-versatile"
    ]
    
    results = {}
    for model in models:
        success = test_model(model)
        results[model] = success
    
    # Print summary
    print("\nTest Results Summary:")
    print("-" * 50)
    for model, success in results.items():
        status = "✅ Working" if success else "❌ Failed"
        print(f"{model}: {status}")
    
    # Print recommendations
    print("\nRecommendations:")
    print("-" * 50)
    if all(results.values()):
        print("All models are working correctly!")
    else:
        print("Some models are not working. Please check the following:")
        for model, success in results.items():
            if not success:
                print(f"- {model} failed to respond. Check if the model name is correct and the API key has access.")
        print("\nRecommendation: Use llama-3.1-8b-instant as your default model as it has the best rate limits.")

if __name__ == "__main__":
    main() 