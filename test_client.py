import requests
import json

def chat_with_server(base_url="http://0.0.0.0:8001"):
    # Initialize empty message history
    message_history = []
    
    print("Math Skills Assessment Chat Client")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYour message: ")
        
        if user_input.lower() == 'quit':
            break
        
        # Add user message to history
        message_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Prepare the request
        payload = {
            "history": message_history
        }
        
        try:
            # Send request to server
            response = requests.post(f"{base_url}/chat", json=payload)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Get the response
            result = response.json()
            assistant_message = result["response"]
            
            # Add assistant's response to history
            message_history.append(assistant_message)
            
            # Print the response
            print("\nAssistant:", assistant_message["content"])
            
        except requests.exceptions.RequestException as e:
            print(f"\nError communicating with server: {e}")
            break
        except json.JSONDecodeError:
            print("\nError: Received invalid JSON from server")
            break

if __name__ == "__main__":
    chat_with_server() 