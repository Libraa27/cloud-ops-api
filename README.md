# Cloud Ops API

Cloud Ops API is a simple Python REST API project designed for learning and practicing Cloud Computing and DevOps fundamentals.

The project focuses on HTTP endpoints, Python dependency management, and preparing applications for future containerization and cloud deployment.

## Tech Stack

- **Python 3.10** – Main programming language.
- **FastAPI** – Web framework for building REST APIs.
- **Uvicorn** – ASGI server for running the FastAPI application.

## Getting Started

Follow these steps to set up and run the application locally on Ubuntu.

### 1. Navigate to the Project Directory

After cloning or downloading the repository, navigate to the project directory:

```bash
cd cloud-ops-api
```

### 2. Create a Virtual Environment

```bash
python3.10 -m venv .venv
```

### 3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the Application

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Returns a basic application health response. |
| GET | `/api/info` | Returns basic information about the application. |

### Testing the Endpoints

Open another terminal on the same Ubuntu environment and run:

**Health endpoint:**

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status": "ok"}
```

**Application information endpoint:**

```bash
curl http://127.0.0.1:8000/api/info
```

This endpoint returns basic application information in JSON format.

**Note:** The `/health` endpoint currently provides a basic application-level response. It does not check databases, external services, or other system dependencies.

## Project Status

**Current Status: Basic API Completed**

The initial version includes:

- REST API development using FastAPI.
- Basic health and application information endpoints.
- Python virtual environment and dependency management.
- Local API execution using Uvicorn.
- Basic HTTP endpoint testing using curl.

### Future Improvements

- Containerize the application using Docker.
- Deploy the application to Kubernetes.
- Implement Kubernetes Liveness and Readiness Probes.
- Add application monitoring and logging.
- Explore CI/CD automation.

This project is part of my hands-on learning journey in Cloud Computing and DevOps Engineering.
