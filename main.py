from fastapi import FastAPI
import os
from openai import OpenAI
from dotenv import load_dotenv

# import variables from .env file
load_dotenv()

app = FastAPI()

# Configure your OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post('/project_assistant/')
async def project_assistant(project_description: str):
    # Use OpenAI API to process the descriptions and output solution
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides guidance for project."},
            {"role": "user", "content": f"Project Description: {project_description}. \
                                            According to the project description assist me with completing the project."}
        ],
        model="gpt-4o"
    )
    # solution = chat_completion['choices'][0]['message']['content']
    sln = chat_completion.choices[0].message.content
    print(sln)
    return sln



@app.post('/task_assistant/')
async def task_assistant(project_description: str, task_description: str):
    # Use OpenAI API with `ChatCompletion` to generate small code snippets
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides guidance for project."},
            {"role": "user", "content": f"Given the project description: {project_description}, and the \
                                            task description: {task_description}, provide path-way including code snippets\
                                                to complete the task."}
        ],
        model="gpt-4o"
    )
    sln = chat_completion.choices[0].message.content
    print(sln) 
    return sln