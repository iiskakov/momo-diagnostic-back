from os import getenv
from openai import OpenAI


# Initialize OpenAI client with OpenRouter's base URL and API key
def get_openrouter_client():
    openrouter_client = OpenAI(
        api_key=getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )
    
    # OpenRouter-specific request parameters passed via `extra_body` (optional)
    extra_body = {
        "provider": {
            "allow_fallbacks": True,
        },
        # Additional OpenRouter parameters can be added here, e.g.:
        # "transforms": ["middle-out"]
    }
    
    return openrouter_client, extra_body 
