from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from openai import OpenAI
import json
from dotenv import load_dotenv
import re
from typing import List, Dict, Tuple

# Import variables from .env file
load_dotenv()

mongodb_path = os.getenv('mongo_connnection_string')
print(mongodb_path)
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

def find_project(project_id, is_tech=None):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})
        try:
            project_name = project['name']
        except Exception as e:
            print("43: error extract ing project[name]")
            print(f"{e}")
        
        try:
            project_description = project['description']
        except Exception as e:
            print("49: error extract ing project[description]")
            print(f"{e}")

        try:
            if(not(is_tech) and project['tools']):
                # tools = project['tools']
                print("55: extracted project name, id and tools")
                return project_name, project_description
        except:
            pass

        
        try:
            if(is_tech and project['tools']):
                tools = project['tools']
                print("64: extracted project name, id and tools")
                return project_name, project_id, tools
        except:
            pass

        print("line 69: extracted project name, description")
        return project_name, project_description

def find_module(project_id, is_tech=None):
    if not project_id:
        return "project_id is required."
    else:
        project = collection.find_one({'_id': ObjectId(project_id)})
        try:
            project_name = project['name']
        except Exception as e:
            print("error extract ing project[name]")
            print(f"{e}")
        
        try:
            project_id = project['description']
        except Exception as e:
            print("error extract ing project[description]")
            print(f"{e}")
        
        try:
            project_module = project['modules']
        except Exception as e:
            print("error extracting project[modules]")
            print(f"{e}")
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
            print("error extracting project[features]")
            print(f"{e}")
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
            print("error extracting project[features]")
            print(f"{e}")
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
            print("error extracting project[features]")
            print(f"{e}")
            return(f"PROJECT STURCTURE IS NOT AVAILABLE IN THE DATABASE. PLEASE FIRST ADD features, SO ACCORDING TO THAT I CAN ANSWER:G {e}")

        return project_file_structure

def extract_tasks_without_asterisks(content):
    tasks = []
    # Match bullet points starting with "-" or numbers like "1."
    pattern = r"(?:\d+\.\s|\s*-\s)(.+)"
    matches = re.findall(pattern, content)
    for match in matches:
        task = match.strip()
        # Exclude lines containing '*'
        if '#' not in task:
            tasks.append(task)
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
    directory_structure: str

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
        print(platforms)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'platform': platforms}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("Platform field added successfully.")
        else:
            print("No document found or no changes made.")
        return JSONResponse(content={"platform_suggestions": platforms})
    except Exception as e:
        print(f"Error when suggesting platforms: {e}")  # Logging the error
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
        print(panels)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'panels': panels}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("Panel field added successfully.")
        else:
            print("No document found or no changes made.")
        return JSONResponse(content={"panels": panels})
    except Exception as e:
        print(f"Error when suggesting platforms: {e}")  # Logging the error
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
        print(tools_lib)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'tools': tools_lib}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("Tools & Lib field added successfully.")
        else:
            print("No document found or no changes made.")
        return JSONResponse(content={"tools_lib": tools_lib})
    except Exception as e:
        print(f"Error when suggesting platforms: {e}")  # Logging the error
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
        print(modules)
        # Add/update the technology field in the project document
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {'module': modules}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("Modules field added successfully.")
        else:
            print("No document found or no changes made.")
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
        print(features)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'features': features}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("features field added successfully.")
        else:
            print("No document found or no changes made.")
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
#         print(features)
#         result = collection.update_one(
#             {'_id': ObjectId(body.project_id)},  # Filter by _id
#             {'$set': {f'features_{body.module}': features}}  # Add/Update the technology field
#         )
#         if result.modified_count > 0:
#             print("features field added successfully.")
#         else:
#             print("No document found or no changes made.")
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
        # print(task_list)
        # print("################################################################")
        extracted_tasks = extract_tasks_without_asterisks(task_list)
        print(extracted_tasks)
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'tasks': extracted_tasks}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("tasks field added successfully.")
        else:
            print("No document found or no changes made.")
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
        print(task_assistant)
        ################################################################ we are not storing the response in the database #########################################################################
        # result = collection.update_one(
        #     {'_id': ObjectId(body.project_id)},  # Filter by _id
        #     {'$set': {f'task_{body.task_description}': task_assistant}}  # Add/Update the technology field
        # )
        # if result.modified_count > 0:
        #     print("task_assistant field added successfully.")
        # else:
        #     print("No document found or no changes made.")
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
        print(setup)
        ################################################################ we are storing the response in the database #########################################################################
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'setup': setup}}  # Add/Update the technology field
        )
        if result.modified_count > 0:
            print("task_assistant field added successfully.")
        else:
            print("No document found or no changes made.")
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
        print(kickoff)
        ################################################################ we are storing the response in the database #########################################################################
        result = collection.update_one(
            {'_id': ObjectId(body.project_id)},  # Filter by _id
            {'$set': {f'kickoff': kickoff}}  # /Update the technology field
        )
        if result.modified_count > 0:
            print("kickoff field added successfully.")
        else:
            print("No document found or no changes made.")
        return JSONResponse(content={"kickoff": kickoff})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/download_project/')
async def download_project(body: DownloadProject):
    try:
        generator = DirectoryGenerator(body)

        project_directory_structure = {body.directory_structure}        # user input

        generator.create_structure(f"./{body.project_id}", project_directory_structure)

        return JSONResponse(content={"kickoff": kickoff})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# to download any directory structure.

class DirectoryGenerator:
    def __init__(self, body):
        self.paths = []
        self.body = body
        
    def _get_level(self, line: str) -> int:
        """Get the nesting level of a line"""
        # Count the number of │ and spaces to determine level
        return line.count('│') + line.count('    ')
        
    def _parse_path(self, line: str) -> str:
        """Extract the file/directory name from a tree line"""
        # Remove tree symbols and whitespace
        name = re.sub(r'^[├└│──\s]+', '', line).strip()
        return name
        
    def parse_structure(self, text: str) -> None:
        """Parse the directory structure text into paths"""
        lines = [line for line in text.split('\n') if line.strip()]
        path_stack: List[Tuple[int, str]] = []  # Stack to keep track of (level, name)
        
        for line in lines:
            if not any(char in line for char in '├└│'):
                continue
                
            level = self._get_level(line)
            name = self._parse_path(line)
            
            # Remove any paths from stack that are at a higher or equal level
            while path_stack and path_stack[-1][0] >= level:
                path_stack.pop()
            
            # Add current path to stack
            path_stack.append((level, name))
            
            # Construct full path from stack
            full_path = '/'.join(component[1] for component in path_stack)
            self.paths.append(full_path)

    def create_structure(self, base_path: str, text: str) -> None:
        """Create the directory structure"""
        self.paths = []  # Reset paths before parsing
        self.parse_structure(text)
        
        # First create all directories (paths ending with /)
        for path in self.paths:
            full_path = os.path.join(base_path, path)
            if path.endswith('/'):
                os.makedirs(full_path, exist_ok=True)
                print(f"Created directory: {full_path}")
                
        # Then create all files
        for path in self.paths:
            if not path.endswith('/'):
                full_path = os.path.join(base_path, path)
                dir_path = os.path.dirname(full_path)
                # Ensure directory exists
                os.makedirs(dir_path, exist_ok=True)
                # Create file
                content = get_content(full_path)
                with open(full_path, 'w') as file:
                    file.write(content)
                print(f"Created file: {full_path}")
    
    def get_content(self, path, body = self.body):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Please provide concise and specific information about the project"},
                {"role": "user", "content": f"Given the project description: {find_project(body.project_id, is_tech = False)}, and the \
                                             list of tasks: {find_list_of_tasks(body.project_id)}, and the file structure \
                                                {find_file_structure(body.project_id)}, give me 'only' code of this file:{path}."} #help me setup the project for coding"}
            ],
            model="gpt-4o-mini"
        )
        content = chat_completion.choices[0].message.content
        return content

# Example usage
if __name__ == "__main__":
    generator = DirectoryGenerator()
    
    # Test structure
    input_structure = """
    ni3singh-stock_price_forcasting/
    ├── README.md
    ├── ACGL_DATA.csv
    ├── Time_Series_Forcasting_Keras.ipynb
    ├── Time_Series_Forcasting_Pytorch.ipynb
    ├── Time_Series_Forcasting_Tensorflow.ipynb
    ├── microsoft_stocks.csv
    └── Statsmodel_Forecasting/
        ├── Cleaned_ACGL_data2.csv
        ├── app.py
        ├── model.py
        └── requirements.txt"""


    print("Creating directory structure...")
    generator.create_structure("./test_complex4", input_structure)