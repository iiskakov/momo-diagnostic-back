from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import ell
from back import assess_math_skills, analyze_assessment, create_learning_path 

# Initialize ELL
ell.init(store='./logdir', autocommit=True)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to handle all CORS-related issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's origin if needed
    allow_credentials=True,  # Set to False if you don't need credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/chat")
async def chat_options():
    # Handle preflight requests for CORS
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@app.post("/chat")
async def chat(message: dict):
    try:
        # Extract the message history from the request
        message_history = message.get("history", [])
        print("Received message history:", message_history)  # Add this debug line
        ell_messages = [
            ell.Message(role=msg["role"], content=msg["content"]) 
            for msg in message_history
        ]
        
        # Process the message with assess_math_skills
        response = assess_math_skills(ell_messages)
        
        # Return the response with proper CORS headers
        return JSONResponse(
            content={
                "response": {
                    "role": response.role,
                    "content": response.text
                }
            },
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )
    except Exception as e:
        # Handle exceptions with appropriate HTTP status code
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_results(data: dict):
    try:
        # Extract assessment data from the request
        assessment_data = data.get("assessment_data", "")
        
        if not assessment_data:
            raise HTTPException(status_code=400, detail="Missing assessment data.")

        # Process the assessment data with analyze_assessment
        analysis = analyze_assessment(assessment_data)
        
        # Return the analysis with proper CORS headers
        return JSONResponse(
            content={"analysis": analysis},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )
    except Exception as e:
        # Handle exceptions with appropriate HTTP status code
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_learning_path")
async def learning_path_handler(data: dict):
    try:
        diagnostic_results = data.get("diagnostic_results", "")
        
        if not diagnostic_results:
            raise HTTPException(status_code=400, detail="No Diagnostic results in the request")

        # Process the assessment data with create_learning_path from back.py
        config = create_learning_path(diagnostic_results)
        
        # Return the analysis with proper CORS headers
        return JSONResponse(
            content={"config": config},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )
    except Exception as e:
        # Handle exceptions with appropriate HTTP status code
        raise HTTPException(status_code=500, detail=str(e))
