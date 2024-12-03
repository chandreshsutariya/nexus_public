# Project Assistant

## Overview

This project is a FastAPI-based application designed to assist with project and task management using the OpenAI API. The application offers two main functionalities:

1. **Project Assistant** - Provides guidance for completing a given project description.
2. **Task Assistant** - Offers pathways and small code snippets to complete a task based on the project and task descriptions.

## Features

- Integration with the OpenAI API to generate contextual guidance and code snippets.
- RESTful API endpoints for seamless integration with other systems.
- Configuration through environment variables for security and flexibility.

## Project Structure

- `main.py`: Main application file containing the API endpoints and logic.
- `.env`: Environment file for storing sensitive information such as the OpenAI API key.
- `project_descrtpn.md`: Outlines the steps involved in creating a chatbot.

## Usage

### Prerequisites

- Python 3.7+
- FastAPI
- An OpenAI API key

### Setup

1. Clone the repository.
2. Install the required packages.
3. Set up your `.env` file with your OpenAI API key:

```
OPENAI_API_KEY='your-openai-api-key'
```

### Running the Application

Execute the following command to start the FastAPI application:

```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser to interact with the API.

### API Endpoints

- **POST** `/project_assistant/`: Provide a project description and receive guidance.
- **POST** `/task_assistant/`: Provide a project and task description to get guidance and code snippets.

## Testing

Run tests using the FastAPI TestClient:

```bash
pytest test_main.py
```

## License

This project is open-source and available under the MIT License.

## Contact

For further inquiries or contributions, please contact the project team at [email@example.com].