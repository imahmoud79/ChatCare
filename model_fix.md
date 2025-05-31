# Fixing Issues with Deepseek and Qwen Models in Groq API

## Problem
The deepseek and qwen models are currently not working in the application, giving the following error message:

```
I apologize, but I'm having trouble processing your request with the deepseek-r1-distill-llama-70b model right now. Please try again or try a different model from Settings.
```

## Solution
After testing, I found that all models (llama-3.3-70b-versatile, deepseek-r1-distill-llama-70b, and qwen-qwq-32b) are actually available and working in the Groq API. The issue appears to be with how these models are being accessed through the LangChain wrapper.

### Implemented Fixes

1. **Added model availability checking**:
   - Created a cache to track which models are available
   - Implemented a function to check if a model is responding before using it
   - Added automatic fallback to llama-3.3-70b-versatile if a model is unavailable

2. **Direct API integration**:
   - Modified the code to use direct Groq API calls for deepseek and qwen models
   - Kept the LangChain wrapper for llama as it's known to work reliably
   - This provides more control over the API call parameters and error handling

3. **Enhanced error handling**:
   - Added specific error messages for different types of failures (rate limits, timeouts, etc.)
   - Improved logging to track model availability and response times
   - Implemented graceful fallback to llama when other models fail

## How to Test
1. Use the Django admin to change your preferred model to either deepseek or qwen
2. Try sending a message in the chat interface
3. The model should now respond correctly, or if there's an issue, it will provide a clear error message

## Technical Details
The issue was likely caused by how the LangChain wrapper formats messages or handles the API integration for these specific models. By using the direct Groq API, we ensure the models are accessed in a more standardized way that matches Groq's API expectations.

## Next Steps
- Consider implementing a more sophisticated model rotation system that can automatically switch between available models
- Monitor Groq API updates as they may change model parameters or availability over time
- Add a model status indicator in the UI so users know which models are currently available 