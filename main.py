from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
from dotenv import load_dotenv

# import variables from .env file
load_dotenv()

app = FastAPI()

# Set up CORS middleware to allow access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure your OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post('/project_assistant/')
async def project_assistant(project_description: str):
    # Use OpenAI API to process the descriptions and output solution
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides guidance for project."},
            {"role": "user", "content": f"Project Description: {project_description}. \\n                                            According to the project description assist me with completing the project."}
        ],
        model="gpt-4o"
    )
    sln = chat_completion.choices[0].message.content
    print(sln)
    return sln

@app.post('/task_assistant/')
async def task_assistant(project_description: str, task_description: str):
    # Use OpenAI API with `ChatCompletion` to generate small code snippets
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides guidance for project."},
            {"role": "user", "content": f"Given the project description: {project_description}, and the \\n                                            task description: {task_description}, provide path-way including code snippets\\n                                                to complete the task."}
        ],
        model="gpt-4o"
    )
    sln = chat_completion.choices[0].message.content
    print(sln) 
    return sln