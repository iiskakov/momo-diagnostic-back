# Momo Kids Math Assessment API

A FastAPI application that provides math assessment capabilities for kids using AI.

## Local Development

1. Create a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example` and fill in your OPENROUTER_API_KEY.

4. Run the development server:
   ```
   uvicorn app:app --reload
   ```

## Deploying to Railway

1. Create a Railway account and install the Railway CLI:
   ```
   npm i -g @railway/cli
   ```

2. Log in to Railway:
   ```
   railway login
   ```

3. Create a new project:
   ```
   railway init
   ```

4. Set up environment variables in Railway dashboard:
   - OPENROUTER_API_KEY
   - ALLOWED_ORIGINS (comma-separated list of frontend origins)

5. Deploy your project:
   ```
   railway up
   ```

The application will automatically deploy using the Procfile configuration.

## API Endpoints

- `/chat` - Handles the math assessment conversation
- `/analyze` - Analyzes assessment results
- `/create_learning_path` - Creates a learning path based on diagnostic results
- `/health` - Simple health check endpoint

## Environment Variables

- `OPENROUTER_API_KEY`: API key for OpenRouter service
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins
- `PORT`: Port for the application (provided by Railway in production) 