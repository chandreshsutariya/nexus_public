from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
from openai import OpenAI
import json
from dotenv import load_dotenv
import re
from typing import List, Dict, Tuple,Any
import shutil
import tempfile
from pathlib import Path
import uuid
import subprocess
import logging as logger



# Import variables from .env file
load_dotenv()

mongodb_path = os.getenv('mongo_connnection_string')
# print(mongodb_path)
app = FastAPI()

# Set up CORS middleware to allow access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

import pymongo
from bson import ObjectId
# from pymongo import ObjectId

client_mongo = pymongo.MongoClient(mongodb_path)

collection = client_mongo['ELaunch-Nexus']['projects']

def find_project_name(project_id):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})
        try:
            project_name = project['name']
            return project_name
        except Exception as e:
            # # print("43: error extract ing project[name]")
            # print(f"{e}")
            pass
    return "default_project_name"
        
def find_project(project_id, is_tech=None):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})
        try:
            project_name = project['name']
        except Exception as e:
            # # print("43: error extract ing project[name]")
            # print(f"{e}")
            pass
        
        try:
            project_description = project['description']
        except Exception as e:
            # print("49: error extract ing project[description]")
            # print(f"{e}")
            pass

        try:
            if(not(is_tech) and project['tools']):
                # tools = project['tools']
                # print("55: extracted project name, id and tools")
                return project_name, project_description
        except:
            pass

        
        try:
            if(is_tech and project['tools']):
                tools = project['tools']
                # print("64: extracted project name, id and tools")
                return project_name, project_id, tools
        except:
            pass

        # print("line 69: extracted project name, description")
        return project_name, project_description

def find_module(project_id, is_tech=None):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})
        try:
            project_name = project['name']
        except Exception as e:
            # print("error extract ing project[name]")
            # print(f"{e}")
            pass
        
        try:
            project_id = project['description']
        except Exception as e:
            # print("error extract ing project[description]")
            # print(f"{e}")
            pass
        
        try:
            project_module = project['modules']
        except Exception as e:
            # print("error extracting project[modules]")
            # print(f"{e}")
            return(f"PROJECT MODULES ARE NOT AVAILABLE IN THE DATABASE. PLEASE FIRST ADD MODULES, SO ACCORDING TO THAT I CAN ANSWER:G {e}")
        
        try:
            if(not(is_tech) and project['technology']):
                project_technology = project['technology']
                return project_module
        except:
            pass

        return project_module

def find_features(project_id, is_tech=None):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})

        try:
            project_features = project['features']
        except Exception as e:
            # print("error extracting project[features]")
            # print(f"{e}")
            return(f"PROJECT features ARE NOT AVAILABLE IN THE DATABASE. PLEASE FIRST ADD features, SO ACCORDING TO THAT I CAN ANSWER:G {e}")

        return project_features

def find_list_of_tasks(project_id):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})

        try:
            project_list = project['tasks']
        except Exception as e:
            # print("error extracting project[features]")
            # print(f"{e}")
            return(f"TASK-LIST IS NOT AVAILABLE IN THE DATABASE. PLEASE FIRST ADD features, SO ACCORDING TO THAT I CAN ANSWER:G {e}")

        return project_list

def find_file_structure(project_id):
    if not project_id:
        return "project_id is required."
    else:

        project = collection.find_one({'_id': ObjectId(project_id)})

        try:
            project_file_structure = project['setup']
        except Exception as e:
            # print("error extracting project[features]")
            # print(f"{e}")
            return(f"PROJECT STURCTURE IS NOT AVAILABLE IN THE DATABASE. PLEASE FIRST ADD features, SO ACCORDING TO THAT I CAN ANSWER:G {e}")

        return project_file_structure

def get_kickoff(project_id):
    if not project_id:
        return "project_id is required."
    else:

        project = collection.find_one({'_id': ObjectId(project_id)})

        try:
            kickoff = project['kickoff']
        except Exception as e:
            # print("error extracting project[features]")
            # print(f"{e}")
            return(f"KickOff IS NOT AVAILABLE IN THE DATABASE. PLEASE FIRST ADD features, SO ACCORDING TO THAT I CAN ANSWER:G {e}")

        return kickoff

def count_astrick(string):
    count =0
    for i in string:
        if i == "*":
            count+=1
    return count

def extract_tasks_without_asterisks(content):
    tasks = []
    # Match bullet points starting with "-" or numbers like "1."
    content_ = content.split("\n")
    # print("content: ", content)
    for each in content_:
        print(each)
        if(count_astrick(each) == 1):
            trip = each.split("]", 1)[1]
            tasks.append(trip)
    # print("len of content_:", len(content_))
    # pattern = r"(?:\d+\.\s|\s*-\s)(.+)"
    # matches = re.findall(pattern, content)
    # for match in matches:
    #     task = match.strip()
    #     # Exclude lines containing '*'
    #     if '#' not in task:
    #         tasks.append(task)
    return tasks

# Configure your OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ProjectDescription(BaseModel):
    project_id: str

class TaskDescription(BaseModel):
    project_id: str
    task_description: str
    comment: str

class ModuleRequest(BaseModel):
    project_id: str

class TaskRequest(BaseModel):
    project_id: str

class FeatureAssistant(BaseModel):
    project_id: str
    # module: str

class ToolsAndLibSuggestions(BaseModel):
    project_id: str

class Panels(BaseModel):
    project_id: str

class TaskList(BaseModel):
    project_id: str

class Setup(BaseModel):
    project_id: str
    user_input: str

class Kickoff(BaseModel):
    project_id: str
    user_input: str = None


class DownloadProject(BaseModel):
    project_id: str
    user_input: Any
    project_type: str           # shall be from "flutter", "react"

class DownloadProject_test(BaseModel):
    project_id: str
    user_input: str

# 1 :: TECHNOLOGY STACK
# @app.post('/technology_suggestion/')
# async def tech_assistant(body: TaskRequest):
#     try:
#         # Use OpenAI API to generate the technology stack
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "Please provide concise and specific information about the project"},
#                 {"role": "user", "content": f"Using the project example context: {find_project(body.project_id)}, suggest technology stack."}
#             ],
#             model="gpt-4o"
#         )
#         tech_stack = chat_completion.choices[0].message.content
#         print(tech_stack)
#         result = collection.update_one(
#             {'_id': ObjectId(body.project_id)},  # Filter by _id
#             {'$set': {'technology_suggestions': tech_stack}}  # Add/Update the technology field
#         )
#         if result.modified_count > 0:
#             print("Technology field added successfully.")
#         else:
#             print("No document found or no changes made.")
#         return JSONResponse(content={"technology_suggestions": tech_stack})
#     except Exception as e:
#         print(f"Error when suggesting technology stack: {e}")  # Logging the error
#         raise HTTPException(status_code=500, detail="An error occurred while generating the technology suggestion.")

# 2 :: SUGGESTION FOR PLATFORMS

# @app.post('/project_explaination')
# async def project_explanation(body: ProjectDescription):
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "You are a highly intelligent assistant with expertise in understanding and elaborating on project descriptions. \
#                                         You analyze provided descriptions carefully and generate detailed explanations, \
#                                         tailoring each response uniquely to match the project's objectives and scope."},
#                 {"role": "user", "content": f"Based on the project description: {find_project(body.project_id, is_tech=True)}, provide a comprehensive explanation of the project. Your response should include: \
#                                         1. **Project Overview**: A concise summary of the project's objectives, purpose, and key features.  \
#                                         2. **Detailed Working Flow**: Break down the workflow into clear steps, explaining how the system components interact and the sequence of operations. Highlight any unique technologies, algorithms, or methods used in the project. \
#                                         3. **Database and Data Handling**: If applicable, describe the data structures or databases involved, including how data is stored, processed, and retrieved.  \
#                                         4. **Security Features**: Explain any security measures implemented in the project, such as password protection, encryption, or access control.  \
#                                         5. **User Interaction**: Highlight how users interact with the system, including interfaces, input methods, and output formats.  \
#                                         6. **Deployment Suggestions**: Recommend deployment platforms (e.g., web, mobile, cloud) suitable for the project, considering its requirements. \
#                                         7. **Advantages and Benefits**: Summarize the key benefits of the project, focusing on usability, performance, security, and scalability.  \
#                                         Ensure your explanation is unique to the project description provided and does not follow a generic structure unless required by the nature of the project."}
#             ],
#             model="gpt-4o"
#         )

#         project_explanation = chat_completion.choices[0].message.content
#         # print(platforms)
#         result = collection.update_one(
#             {'_id': ObjectId(body.project_id)},  # Filter by _id
#             {'$set': {'project_explanation': project_explanation}}  # Add/Update the technology field
#         )
#         if result.modified_count > 0:
#             # print("Platform field added successfully.")
#             pass
#         else:
#             # print("No document found or no changes made.")
#             pass
#         return JSONResponse(content={"project_explanation":project_explanation})
#     except Exception as e:
#         # print(f"Error when suggesting platforms: {e}")  # Logging the error
#         raise HTTPException(status_code=500, detail="An error occurred while generating the platform suggestion.")
    
@app.post('/platform_suggestion/')
async def platform_suggestion(body: ProjectDescription):
    try:
        # Use OpenAI API to generate platform suggestions based on the project description
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Based on the project description: {find_project(body.project_id, is_tech=True)}, \
                                        platforms for deployment. If you are giving suggestion for mobile platform, adivse Native or Hybrid."}
            ],
            model="gpt-4o"
        )
        platforms = chat_completion.choices[0].message.content
        # print(platforms)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'platform': platforms}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("Platform field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"platform_suggestions": platforms})
    except Exception as e:
        # print(f"Error when suggesting platforms: {e}")  # Logging the error
        raise HTTPException(status_code=500, detail="An error occurred while generating the platform suggestion.")
    
# 2.1 :: PANELS
@app.post('/panels/')
async def panels(body: Panels):
    try:
        # Use OpenAI API to generate platform suggestions based on the project description
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Based on the project description: {find_project(body.project_id)}, tell the panels required for the project like user panel, admin panel, merchant panel etc.."}
            ],
            model="gpt-4o"
        )
        panels = chat_completion.choices[0].message.content
        # print(panels)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'panels': panels}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("Panel field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"panels": panels})
    except Exception as e:
        # print(f"Error when suggesting platforms: {e}")  # Logging the error
        raise HTTPException(status_code=500, detail="An error occurred while generating the platform suggestion.")

    
# 3 :: TOOLS & LIBRARIES
@app.post('/tools_and_lib_suggestions/')
async def tools_and_lib_suggestions(body: ToolsAndLibSuggestions):
    try:
        # Use OpenAI API to generate platform suggestions based on the project description
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Based on the project description: {find_project(body.project_id)}, tell tools and library to use."}
            ],
            model="gpt-4o"
        )
        tools_lib = chat_completion.choices[0].message.content
        # print(tools_lib)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'tools': tools_lib}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("Tools & Lib field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"tools_lib": tools_lib})
    except Exception as e:
        # print(f"Error when suggesting platforms: {e}")  # Logging the error
        raise HTTPException(status_code=500, detail="An error occurred while generating the platform suggestion.")

# 4 :: MODULES
@app.post('/module_assistant/')
async def module_assistant(body: ModuleRequest):
    try:
        # Use OpenAI API to generate the list of possible modules
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Using the project example context: {find_project(body.project_id, )} list the modules\
                 that could be used."}
            ],
            model="gpt-4o"
        )
        modules = chat_completion.choices[0].message.content
        # print(modules)
        # Add/update the technology field in the project document
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'module': modules}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("Modules field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"modules": modules})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 5 :: FEATURES OF EACH MODULE
@app.post('/feature_assistant/')
async def feature_assistant(body: FeatureAssistant):
    try:
        # Use OpenAI API to generate the list of possible modules
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Using the project example context: {find_project(body.project_id)}, provide\
                 modeul wise feature/s of following modules: {find_module(body.project_id, is_tech=True)}"}
            ],
            model="gpt-4o"
        )
        features = chat_completion.choices[0].message.content
        # print(features)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'features': features}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("features field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"features": features})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post('/feature_assistant/')
# async def feature_assistant(body: FeatureAssistant):
#     try:
#         # Use OpenAI API to generate the list of possible modules
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "Please provide concise and specific information about the project"},
#                 {"role": "user", "content": f"Using the project example context: {find_project(body.project_id)}, provide\
#                  modeul wise feature/s of following modules: {find_module(body.project_id, is_tech=True)}"}
#             ],
#             model="gpt-4o"
#         )
#         features = chat_completion.choices[0].message.content
#         # print(features)
#         result = collection.update_one(
#             {'_id': ObjectId(body.project_id)},  # Filter by _id
#             {'$set': {f'features_{body.module}': features}}  # Add/Update the technology field
#         )
#         if result.modified_count > 0:
#             # print("features field added successfully.")
#         else:
#             # print("No document found or no changes made.")
#         return JSONResponse(content={"features": features})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# 6 :: TASK LIST
@app.post('/task_list/')
async def task_assistant(body: TaskList):
    try:
        # Use OpenAI API with `ChatCompletion` to generate small code snippets
        chat_completion = client.chat.completions.create(
            messages=[
        {
            "role": "system",
            "content": """You are an expert technical project planner who breaks down features into comprehensive development tasks. 

            Core Task Generation Rules:
            1. Format: * [TaskNumber] [Label] Specific task description
               Labels: [UI/UX], [AUTH], [API], [DB], [SECURITY], [TESTING], [INTEGRATION], [FEATURE]
            2. Tasks MUST follow documentation order, NOT label order
            3. Each feature requires:
               - Essential UI/UX tasks (only where user interaction is needed)
               - All implementation tasks (backend, frontend, database)
               - Security and validation tasks
               - Testing tasks for critical features
            4. Use AI intelligence to:
               - Add necessary tasks not explicitly mentioned
               - Identify dependencies
               - Include industry best practices
               - Consider edge cases
               - Add essential security measures

            Task Generation Process:
            1. Read feature and description completely
            2. Break into smallest possible tasks
            3. Include ALL implementation details
            4. Add necessary UI tasks only where needed
            5. Consider full development lifecycle
            6. Add intelligent suggestions
            7. Maintain sequential order based on natural development flow
            8. Never group or order by labels

            ALWAYS generate detailed tasks, never summarize."""
        },
        {
            "role": "user",
            "content": f"""Using this dating app documentation: {find_project(body.project_id)}

            Create a comprehensive task list that:

            1. Processes features IN DOCUMENTATION ORDER
            2. For each feature and description:
               - Generate multiple atomic tasks
               - Include essential UI/UX tasks where needed
               - Cover all implementation details
               - Add security and validation
               - Include testing for critical features
               - Use AI intelligence to add necessary tasks
               
            3. Each task must:
               - Start with sequential number
               - Include appropriate label
               - Be specific and actionable
               - Be completable in 1-2 days
               - Follow natural implementation order
               
            4. Requirements:
               - Never skip any implementation detail
               - Never group by labels
               - Always maintain full coverage
               - Include intelligent additions
               - Consider user experience
               - Add essential security measures
               - Include necessary integrations
               
            Generate comprehensive task list now, Don't skip any backend related task ensuring COMPLETE feature coverage with intelligent additions."""
        }
                                            #             "Given the project description: {find_project(body.project_id)}, and the \
                                            # features list: {find_features(body.project_id)}, give me the list of coding\
                                            #     tasks in series to implement features in list format. Please note that\
                                            #         I want the tasks in series and at granular level such that I can\
                                            #             use agile method while developement."
            ],
            model="gpt-4o" #gpt-4o-mini
        )
        task_list = chat_completion.choices[0].message.content
        # # print(task_list)
        # # print("################################################################")
        extracted_tasks = extract_tasks_without_asterisks(task_list)
        # print(extracted_tasks)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'tasks': extracted_tasks}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("tasks field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"tasks": extracted_tasks})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 6 :: TASK DETAILS
@app.post('/task_assistant/')
async def task_assistant(body: TaskDescription):
    try:
        # Use OpenAI API with `ChatCompletion` to generate small code snippets
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Given the project description: {find_project(body.project_id)}, and the \
                                            task description: {body.task_description} and comment: {body.comment}, provide path-way including a small code snippets\
                                                to complete the task."}
            ],
            model="gpt-4o-mini"
        )
        task_assistant = chat_completion.choices[0].message.content
        # print(task_assistant)
        ################################################################ we are not storing the response in the database #########################################################################
        # result = collection.update_one(
        #     {'_id': ObjectId(body.project_id)},  # Filter by _id
        #     {'$set': {f'task_{body.task_description}': task_assistant}}  # Add/Update the technology field
        # )
        # if result.modified_count > 0:
        #     # print("task_assistant field added successfully.")
        # else:
        #     # print("No document found or no changes made.")
        return JSONResponse(content={"task_assistant": task_assistant})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/setup/')
async def setup(body: Setup):
    try:
        # Use OpenAI API with `ChatCompletion` to generate small code snippets
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Given the project description: {find_project(body.project_id, is_tech = True)}, and the \
                                             user input {body.user_input} help me setup project for the first time."} #help me setup the project for coding"}
            ],
            model="gpt-4o-mini"
        )
        setup = chat_completion.choices[0].message.content
        # print(setup)
        extract_bash_commands(setup)
        ################################################################ we are storing the response in the database #########################################################################
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'setup': setup}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            # print("task_assistant field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"setup": setup})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/kickoff/')
async def setup(body: Kickoff):
    try:
        # Use OpenAI API with `ChatCompletion` to generate small code snippets
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Given the project description: {find_project(body.project_id, is_tech = False)}, and the \
                                             list of tasks: {find_list_of_tasks(body.project_id)}, and the file structure \
                                                {find_file_structure(body.project_id)}, and user input:{body.user_input} \
                                                    help me kickoff the coding by giving code."} #help me setup the project for coding"}
            ],
            model="gpt-4o-mini"
        )
        kickoff = chat_completion.choices[0].message.content
        # print(kickoff)
        ################################################################ we are storing the response in the database #########################################################################
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'kickoff': kickoff}}  # /Update the technology field
        )
        if result.modified_count > 0:
            # print("kickoff field added successfully.")
            pass
        else:
            # print("No document found or no changes made.")
            pass
        return JSONResponse(content={"kickoff": kickoff})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post('/kickoff/')
# async def setup(body: Kickoff):
#     try:
#         generator = DirectoryGenerator(body)

#         project_user_input = body.user_input

#         generator.create_structure(f"./{body.project_id}", project_user_input)

#         return JSONResponse(content={"kickoff": project_user_input})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# to download any directory structure.






# Example usage
# if __name__ == "__main__":
#     # Test structure
#     input_structure = """
# FRS/
# │
# ├── frontend/                 # Frontend files
# │   ├── public/               # Public assets (index.html, images, etc.)
# │   ├── src/                  # Source files (React/Vue components)
# │   │   ├── components/       # Reusable UI components
# │   │   ├── App.js            # Main application file
# │   │   └── index.js          # Entry point for the application
# │   └── package.json          # Frontend dependencies and scripts
# │
# ├── backend/                  # Backend files
# │   ├── app/                  # Main application module
# │   │   ├── __init__.py       # Initialize the Flask/Django app
# │   │   ├── routes.py         # API routes for handling requests
# │   │   └── models.py         # Database models using SQLAlchemy
# │   ├── tests/                # Test cases for backend
# │   ├── requirements.txt      # Backend dependencies (Flask/Django, etc.)
# │   ├── config.py             # Configuration settings
# │   └── run.py                # Main entry point to run the backend server
# │
# ├── data/                     # Folder for storing uploaded event photos
# │   └── temp/                 # Temporary storage for uploads
# │
# ├── database/                 # Database files/configuration
# │   └── init_db.py            # Script to initialize the SQLite database
# │
# ├── security/                 # Security configurations
# │   └── auth.py               # Authentication and password handling
# │
# ├── requirements.txt          # Combined requirements for both frontend and backend
# ├── README.md                 # Project documentation
# └── .gitignore                # Files/directories to ignore in version control
# """

#     base_ = DownloadProject_test(project_id="678797c65a09e185574412ec", user_input=input_structure)
#     generator = DirectoryGenerator(base_)

#     # print("Creating directory structure...")
#     generator.create_structure(f"{base_.project_id}", input_structure)


def extract_directory_structure(text):
    print("Started Direcory extraction")
    uuid_str = str(uuid.uuid4())
    try:
        with open(f"{uuid_str}", "w") as f:
            # print("1121: ", text)

            f.write(text)
    except Exception as e:
        # print(f"799: Error writing to file: {e}")
        pass
    
    try:
        with open(f"{uuid_str}", "r") as f:
            # file_content = f.read()
            structure = ""
            one = f.readline()
            backtick=0
            while(one):
                # # print(one)
                if "```" in one:
                    backtick+=1
                    one = f.readline()
                    # # print(one)
                if backtick == 1:
                    structure += one
                    # # print(one)
                one = f.readline()
        # # print("structure: \n:", structure)
    except Exception as e:
        return None
    
    # delete the file
    try:
        os.remove(f"{uuid_str}")
    except Exception as e:
        # print(f"799: Error deleting file: {e}")
        pass
    
    # structure = structure.split("\n", 1)[1]
    print("structure created")
    return structure

def extract_bash_commands(text):
    uuid_str = str(uuid.uuid4())
    try:
        with open(f"{uuid_str}", "w") as f:
            # print("1121: ", text)
           
            f.write(text)
    except Exception as e:
        # print(f"799: Error writing to file: {e}")
        pass
    
    try:
        with open(f"{uuid_str}", "r") as f:
            # file_content = f.read()
            structure = ""
            one = f.readline()
            backtick=0
            while(one):
                # print('776:',one)
                if "```bash" in one:
                    backtick=1
                    one=f.readline()
                    structure+=one
                    # print('771: ',one)
                    one=f.readline()
                    continue
                
                if backtick == 1 and "```" in one:
                    backtick=0
                    # print('777:', one)
                elif backtick==1:
                    structure+=one
                    # print('774:', one)
                one = f.readline()
        # # print("structure: \n:", structure)
    except Exception as e:
        return None
    
    # delete the file
    try:
        os.remove(f"{uuid_str}")
        pass
    except Exception as e:
        # print(f"799: Error deleting file: {e}")
        pass
    
    print("structure: \n:", structure)
    return structure

# Example usage
# text = """..."""  # Replace this with your project structure text
# directory_structure = extract_directory_structure(find_file_structure("677e76c21eb70fc947b11686"))
# # print(directory_structure)

def get_middleware_file_content(path: str) -> str:
        """Fetch content for middleware files or return an empty string for others."""
        print('866',path)
        try:
            # Check if the path corresponds to a middleware file
            base_middleware_dir = os.getenv('middleware_files')  # Default for Linux
            print('870',base_middleware_dir)

            filename = os.path.basename(path)
            middleware_files = ["auth.middleware.ts", "decryption.middleware.ts", "encryption.middleware.ts"]

            if filename in middleware_files:
                # Read content from the corresponding file in the local `middleware_files` folder
                local_file_path = os.path.join(base_middleware_dir, filename)
                with open(local_file_path, "r") as f:
                    return f.read()

            # For other files, return empty content
            return ""
        except Exception as e:
            print(f"Error reading content for {path}: {e}")
            return ""


@app.post('/downloadproject/')
async def download_project(body: DownloadProject):
    try:
        cwd = os.getcwd()

        # Step 1: Create 'projects' folder and navigate into it
        print("Creating projects folder...")
        projects_dir = os.path.join(cwd, "projects")
        os.makedirs(projects_dir, exist_ok=True)
        os.chdir(projects_dir)
        print(f"Current working directory: {os.getcwd()}")

        # Step 2: Fetch the directory structure and generate it
        print("Fetching generated directory structure...")
        dir_structure = extract_directory_structure(find_file_structure(body.project_id))
        generator = DirectoryGenerator(body)
        base_name = f"./{body.project_id}"
        generator.create_structure(base_name, dir_structure)


        projects_dir = os.path.join(projects_dir, body.project_id)
        # Step 3: Search for 'backend' folder
        backend_dir = None
        for line in dir_structure.splitlines():
            if "backend" in line:
                backend_dir = os.path.join(projects_dir, "backend")
                break

        # Create 'backend' folder if not found
        if not backend_dir:
            backend_dir = os.path.join(projects_dir, "backend")
            os.makedirs(backend_dir, exist_ok=True)
            print(f"'backend' directory created at: {backend_dir}")
        else:
            print(f"'backend' directory found in structure at: {backend_dir}")

        # # Step 4: Navigate into the 'backend' folder
        # os.chdir(backend_dir)
        # print(f"Current working directory: {os.getcwd()}")

        # Step 5: Run Node commands (if project type is 'node')
        # if body.project_type == "node":
        #     os.chdir(backend_dir)
        #     print(f"Current working directory: {os.getcwd()}")
        #     print("Running Node.js commands...")
        #     result = subprocess.run("npm init -y", shell=True, check=False, text=True)
        #     if result.returncode != 0:
        #         print(f"Warning: Command 'npm init -y' failed. Continuing...")
        #     print("Completed 'npm init -y'")

        #     result = subprocess.run("npm install express", shell=True, check=False, text=True)
        #     if result.returncode != 0:
        #         print(f"Warning: Command 'npm install express' failed. Continuing...")
        #     print("Completed 'npm install express'")
        # Step 5: Run Node commands (if project type is 'node')
        if body.project_type == "node":
            # Change working directory to 'backend'
            print('backend_dir: ', backend_dir)
            os.chdir(backend_dir)
            print(f"Changed working directory to: {os.getcwd()}")

            # Run Node.js commands
            print("Running Node.js commands...")

            def is_package_json_present(projects_dir):
                for root, dirs, files in os.walk(projects_dir):
                    if "package.json" in files:
                        return True
                return False
            
            if is_package_json_present(backend_dir):
                print("package.json file already exists in the structure. Skipping 'npm init -y'.")
            else:
                result = subprocess.run("npm init -y", shell=True, check=True, text=True)
                if result.returncode == 0:
                    print("Completed 'npm init -y'")
                else:
                    print(f"Warning: Command 'npm init -y' failed with return code {result.returncode}")

            result = subprocess.run("npm install express", shell=True, check=True, text=True)
            if result.returncode == 0:
                print("Completed 'npm install express'")
            else:
                print(f"Warning: Command 'npm install express' failed with return code {result.returncode}")


        elif(body.project_type == "flutter"):
            project_path = os.path.join(projects_dir)
            print("downloading structure for flutter")

            full_project_path = os.path.join(project_path, body.project_id)

            if os.path.exists(full_project_path):
                print(f"Deleting existing directory: {full_project_path}")
                shutil.rmtree(full_project_path)

            os.chdir(project_path)

            result = subprocess.run(f"flutter create {body.project_id}", shell=True, check=False, text=True)
            if result.returncode !=0:
                print(f"Warning: Command 'flutter create {body.project_id}' failed with return code {result.returncode}. Continuing...")
                print("processing completed for flutter")

        elif(body.project_type == "react"):
            project_path = os.path.join(projects_dir)

            print("downlaoding started for react")

            full_project_path = os.path.join(project_path, body.project_id)

            if os.path.exists(full_project_path):
                print(f"Deleting existing directory: {full_project_path}")
                shutil.rmtree(full_project_path)

            os.chdir(project_path)

            result = subprocess.run(f"npx create-react-app {body.project_id}", shell=True, check=False, text=True)
            if result.returncode !=0:
                print(f"Warning: Command 'npx create-react-app {body.project_id}' failed with return code {result.returncode}. Continuing...")
                print("processing completed for react")
        
        middleware_dir = None
        # for line in dir_structure.splitlines():
        #     if "middleware" in line and "backend" and "src" in line:
        #         middleware_dir = os.path.join(backend_dir or src_dir, "middleware")
        #         break

        # Create 'middleware' folder if not found
        # if not middleware_dir:
        #     middleware_dir = os.path.join(backend_dir, "middleware")
        #     os.makedirs(middleware_dir, exist_ok=True)
        #     print(f"'middleware' directory created at: {middleware_dir}")
        # else:
        #     print(f"'middleware' directory found in structure at: {middleware_dir}")

        src_dir = os.path.join(backend_dir, "src")
        if os.path.exists(src_dir) and os.path.isdir(src_dir):
            # If 'src' directory exists, create 'middleware' inside 'src'
            middleware_dir = os.path.join(src_dir, "middleware")
        else:
            # Otherwise, create 'middleware' directly inside 'backend'
            middleware_dir = os.path.join(backend_dir, "middleware")

        # Create 'middleware' folder if not found
        os.makedirs(middleware_dir, exist_ok=True)
        print(f"'middleware' directory created at: {middleware_dir}")

        # Step 7: Navigate into the 'middleware' folder
        os.chdir(middleware_dir)
        print(f"Current working directory: {os.getcwd()}")

        # Step 8: Fetch or generate middleware files with content
        for filename in ["auth.middleware.ts", "decryption.middleware.ts", "encryption.middleware.ts"]:
            target_path = os.path.join(middleware_dir, filename)
            try:
                # Fetch the content using the provided function
                content = get_middleware_file_content(target_path)

                # Write the content to the target path
                with open(target_path, "w") as target_file:
                    target_file.write(content)
                print(f"Copied file: {filename} to {target_path}")
            except FileNotFoundError:
                print(f"Source file not found for: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

        os.chdir(backend_dir)
        print(f"Returned to backend directory: {os.getcwd()}")

        # Check if 'middleware' folder exists
        middleware_dir = os.path.join(backend_dir, "middleware")
        if os.path.exists(middleware_dir) and os.path.isdir(middleware_dir):
            # If the folder exists, delete it along with its contents
            shutil.rmtree(middleware_dir)
            print(f"'middleware' directory and its contents have been deleted from: {middleware_dir}")
        else:
            print(f"'middleware' directory not found in: {backend_dir}")

        os.chdir(cwd)
        # Initialize generator and create structure in temp directory
        # generator = DirectoryGenerator(body)
        # base_name = f"./projects/{body.project_id}"
        # generator.create_structure(base_name, dir_structure)

        base_name = f'./projects/{body.project_id}'
        shutil.make_archive(
            base_name=base_name,
            format='zip',
            root_dir='./projects',
            base_dir=body.project_id
        )
        zip_path = f"./projects/{body.project_id}.zip"

        return FileResponse(
            path=zip_path,
            media_type='application/zip',
            filename=f"./projects/{body.project_id}.zip",
            headers={
                "Content-Disposition": f"attachment; filename={body.project_id}.zip"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



class DirectoryGenerator:
    def __init__(self,body):
        self.paths = []
        self.body = body

    def _get_level(self, line: str) -> int:
        """Get the nesting level of a line"""
        # Count the actual indentation level based on │ and spaces
        indent = len(line) - len(line.lstrip('│ '))
        return indent // 2

    def _parse_path(self, line: str) -> str:
        """Extract the file/directory name from a tree line, removing comments and special symbols"""
        # Remove tree symbols and whitespace
        name = re.sub(r'^[├└│─\s]+', '', line)

        # Remove any comments (everything after and including #)
        name = name.split('#')[0].strip()

        # Remove special symbols and their contents
        name = re.sub(r'\([^)]*\)', '', name)  # Remove anything in parentheses ()
        name = re.sub(r'\{[^}]*\}', '', name)  # Remove anything in curly braces {}
        name = re.sub(r'\[[^\]]*\]', '', name)  # Remove anything in square brackets []
        name = re.sub(r"'''.*?'''", '', name)   # Remove triple quotes and their contents
        name = re.sub(r'""".*?"""', '', name)   # Remove triple double quotes and their contents
        name = re.sub(r':\s*$', '', name)       # Remove colons at the end
        name = re.sub(r'^/+', '', name)  # Remove leading slashes


        return name.strip()

    def parse_structure(self, text: str) -> None:
        """Parse the directory structure text into paths"""
        self.paths = []  # Reset paths
        lines = text.split('\n')
        path_stack: List[Tuple[int, str]] = []
        last_valid_level = 0

        for line in lines:
            # Skip completely empty lines
            if not line.strip():
                continue

            # Check if line only contains vertical separators and spaces
            if re.match(r'^[\s│|]*$', line):
                continue

            level = self._get_level(line)
            name = self._parse_path(line)

            # Skip if after removing comments and tree symbols there's nothing left
            if not name:
                continue

            # Handle root directory specially
            if level == 0:
                name = name.lstrip('/')
                path_stack = [(0, name)]
                self.paths.append(name)
                last_valid_level = 0
                continue

            # Maintain the path stack based on the last valid level
            while path_stack and path_stack[-1][0] >= level:
                path_stack.pop()

            # If there's a gap in levels, use the last valid parent
            if not path_stack:
                # If somehow we lost the stack but have a valid path, 
                # treat it as a child of root
                if self.paths:
                    path_stack = [(0, self.paths[0])]

            path_stack.append((level, name))
            last_valid_level = level

            # Construct full path
            full_path = os.path.join(*[p[1] for p in path_stack])
            if full_path not in self.paths:
                self.paths.append(full_path)

    
    # The rest of the class remains the same...
    def create_structure(self, base_path: str, text: str) -> None:
        # remove directory if it exists
        try:
            # shutil.rmtree(base_path)
            pass
        except:
            pass

        # default_structure = """\
        # middleware/
        # ├── auth.middleware.ts
        # ├── decryption.middleware.ts
        # └── encryption.middleware.ts
        # """
        # combined_structure = default_structure + "\n" + text
        # """Create the directory structure"""
        # self.parse_structure(combined_structure)
        self.parse_structure(text)

        # Sort paths to ensure directories are created before files
        sorted_paths = sorted(self.paths, key=lambda x: (len(x.split(os.sep)), not x.endswith('/')))

        for path in sorted_paths:
            if not path.strip():  # Skip empty paths
                continue

            full_path = os.path.join(base_path, path)

            # Normalize path separators
            full_path = os.path.normpath(full_path)

            if path.endswith('/'):
                # Handle directory creation
                try:
                    os.makedirs(full_path, exist_ok=True)
                    # print(f"Created directory: {full_path}")

                except PermissionError:
                    # print(f"Permission denied: Cannot create directory {full_path}")
                    pass
            else:
                try:
                    # Ensure parent directory exists
                    parent_dir = os.path.dirname(full_path)
                    os.makedirs(parent_dir, exist_ok=True)
                    # content = self.get_content(full_path, self.body)
                    # if "middleware/auth.middleware.ts" in full_path:
                    #     content = self.get_middleware_file_content("auth.middleware.ts")
                    # elif "middleware/decryption.middleware.ts" in full_path:
                    #     content = self.get_middleware_file_content("decryption.middleware.ts")
                    # elif "middleware/encryption.middleware.ts" in full_path:
                    #     content = self.get_middleware_file_content("encryption.middleware.ts")
                    # else:
                        # Handle other files normally
                    content = self.get_content(full_path, self.body)

                    # Create file only if it doesn't exist
                    if not os.path.exists(full_path):
                        with open(full_path, 'w') as f:
                            # print("1121: ", content)
                            # print('1126', full_path)
                            if content == None:
                                content =""
                            f.write(content)
                        # print(f"Created file: {full_path}")

                except PermissionError:
                    # print(f"Permission denied: Cannot create file {full_path}")
                    pass

    # def get_content(self, path, body):
    #     dir_structure = extract_directory_structure(find_file_structure(body.project_id))
    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {"role": "system", "content": "Please provide concise and specific information about the project"},
    #             {"role": "user", "content": f"Given the project description: {find_project(body.project_id, is_tech = False)}, and the \
    #                                          list of tasks: {find_list_of_tasks(body.project_id)}, and the file structure \
    #                                             {dir_structure}, and kick-off code: {get_kickoff(body.project_id)} give me 'only' code of this file:{path}."} #help me setup the project for coding"}
    #         ],
    #         model="gpt-4o"
    #     )
    #     content = chat_completion.choices[0].message.content
    #     trimmed = extract_directory_structure(content)
    #     print("trimmed:",trimmed)
    #     return trimmed

    def get_content(self, path, body):
        """
        Get the code content for a specific file based on project description and structure.
        
        Args:
            path (str): File path to generate code for
            body: Request body containing project_id
        
        Returns:
            str: Generated code content for the specified file
        """
        try:
            # Get project metadata
            project_info = find_project(body.project_id, is_tech=False)
            tasks = find_list_of_tasks(body.project_id)
            dir_structure = extract_directory_structure(find_file_structure(body.project_id))
            kickoff_code = get_kickoff(body.project_id)
            
            # Extract file type and context
            file_extension = path.split('.')[-1] if '.' in path else ''
            file_context = self._get_file_context(path, dir_structure)
            
            # Create enhanced prompt
            messages = [
                {"role": "system", "content": """You are an expert software developer. Generate production-ready code that:
                    - Follows best practices and design patterns for the specific language/framework
                    - Includes proper error handling and input validation
                    - Is well-documented with comments explaining complex logic
                    - Maintains consistency with the project's architecture
                    Do not include any explanations - provide only the code content."""},
                {"role": "user", "content": f"""
                    Project Context:
                    - Description: {project_info}
                    - Tasks: {tasks}
                    - File Structure: {dir_structure}
                    - Kickoff Code: {kickoff_code}
                    
                    Generate code for: {path}
                    File Type: {file_extension}
                    File Context: {file_context}
                    
                    Additional Requirements:
                    - Ensure code integrates with existing project structure
                    - Follow consistent naming conventions
                    - Include necessary imports
                    - Handle edge cases appropriately
                    
                    Return only the code content without any markdown or explanations.
                """}
            ]
            
            # Make API call with enhanced parameters
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="gpt-4",  # Corrected model name
                temperature=0.2,  # Lower temperature for more focused output
                max_tokens=4000,  # Adjust based on your needs
                presence_penalty=-0.1,  # Slightly discourage repetition
                frequency_penalty=0.1   # Slightly encourage variety in language
            )
            
            # Extract and process content
            content = chat_completion.choices[0].message.content
            trimmed = self._process_content(content, file_extension)
            
            return trimmed
            
        except Exception as e:
            logger.error(f"Error generating content for {path}: {str(e)}")
            raise

    def _get_file_context(self, path, dir_structure):
        """
        Extract context about the file based on its location in the project.
        """
        # Get parent directory and nearby files
        parent_dir = '/'.join(path.split('/')[:-1])
        nearby_files = [f for f in dir_structure if f.startswith(parent_dir)]
        
        return {
            'parent_directory': parent_dir,
            'nearby_files': nearby_files,
            'depth': len(path.split('/')) - 1
        }

    def _process_content(self, content, file_extension):
        """
        Process and validate the generated content based on file type.
        """
        # Remove any markdown code block indicators
        content = content.replace('```' + file_extension, '').replace('```', '').strip()
        
        # Basic validation based on file type
        if file_extension in ['py', 'js', 'java']:
            # Ensure proper indentation
            lines = content.split('\n')
            if any(line.startswith('    ') for line in lines):
                content = '\n'.join(lines)
        
        return content