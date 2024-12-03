from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

# Import variables from .env file
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

class ProjectDescription(BaseModel):
    project_description: str

class TaskDescription(BaseModel):
    project_description: str
    task_description: str

@app.post('/project_assistant/')
async def project_assistant(body: ProjectDescription):
    try:
        # Use OpenAI API to process the descriptions and output solution
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides guidance for project."},
                {"role": "user", "content": f"Project Description: {body.project_description}. \
                                            According to the project description assist me with completing the project."}
            ],
            model="gpt-4o"
        )
        sln = chat_completion.choices[0].message.content
        print(sln)
        return JSONResponse(content={"solution": sln})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/task_assistant/')
async def task_assistant(body: TaskDescription):
    try:
        # Use OpenAI API with `ChatCompletion` to generate small code snippets
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides guidance for project."},
                {"role": "user", "content": f"Given the project description: {body.project_description}, and the \
                                            task description: {body.task_description}, provide path-way including code snippets\
                                                to complete the task."}
            ],
            model="gpt-4o"
        )
        sln = chat_completion.choices[0].message.content
        print(sln)
        return JSONResponse(content={"solution": sln})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
