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

- `requirements.txt`: Lists the Python packages required for the project.
- `main.py`: Main application file containing the API endpoints and logic.
- `test_main.py`: Contains tests for the API endpoints.
- `.env`: Environment file for storing sensitive information such as the OpenAI API key.
- `project_descrtpn.md`: Outlines the steps involved in creating a chatbot.
- `example.txt`: Example usage of OpenAI API.
- `to_make.txt`: Contains information on the internal task management system.
- `current_error.txt`: Placeholder for error logging.
- `ecosystem.config.js`: `pm2` configuration file to run the application.

## Usage

### Prerequisites

- Python 3.7+
- FastAPI
- An OpenAI API key
- `pm2` for process management

### Setup

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Set up your `.env` file with your OpenAI API key:

```
OPENAI_API_KEY='your-openai-api-key'
```

### Running the Application

To start the FastAPI application using `pm2`, use the following command:

```bash
pm2 start ecosystem.config.js
```

To start the FastAPI application directly on the desired port (1003), execute the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 1003
```

Visit `http://127.0.0.1:1003` in your browser to interact with the API.

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