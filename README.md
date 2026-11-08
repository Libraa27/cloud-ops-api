# Cloud Ops API

A lightweight REST API built with Python and FastAPI, designed to demonstrate fundamental Cloud Computing and DevOps engineering practices.

This project focuses on API development, containerization, Linux networking, container lifecycle management, and infrastructure troubleshooting.

The application can run directly on Ubuntu or inside a Docker container.

## Tech Stack

- **Python 3.10** — Application programming language.
- **FastAPI** — REST API framework.
- **Uvicorn** — ASGI application server.
- **Docker** — Application containerization.
- **Linux (Ubuntu)** — Development and deployment environment.
- **Git** — Version control.

## Project Structure

```text
cloud-ops-api/
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Returns a basic application health response. |
| GET | `/api/info` | Returns application name, version, and environment. |

### Health Endpoint

Request:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Application Information Endpoint

Request:

```bash
curl http://127.0.0.1:8000/api/info
```

Expected response:

```json
{
  "name": "cloud-ops-api",
  "version": "0.1.0",
  "environment": "development"
}
```

**Note:** The `/health` endpoint currently provides a basic application-level response. It does not verify databases, external services, or other infrastructure dependencies.

---

## Getting Started — Local Development

These instructions describe how to run the application directly on Ubuntu without Docker.

### 1. Navigate to the Project Directory

After cloning or downloading the repository:

```bash
cd cloud-ops-api
```

### 2. Create a Python Virtual Environment

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

The API is available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Test the Application

Open another terminal and run:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/api/info
```

Both endpoints should return HTTP 200 responses with JSON bodies.

---

## Running with Docker

Docker provides a consistent application runtime by packaging Python, application dependencies, and source code into an image.

**Prerequisite:** Docker Engine must be installed and running.

### 1. Build the Docker Image

From the project directory:

```bash
docker build -t cloud-ops-api:0.1 .
```

### 2. Run the Container

```bash
docker run -d \
  --name cloud-ops-api-dev \
  -p 127.0.0.1:8001:8000 \
  cloud-ops-api:0.1
```

The application is now accessible from the Ubuntu host at:

```text
http://127.0.0.1:8001
```

Interactive API documentation:

```text
http://127.0.0.1:8001/docs
```

### 3. Verify Container Status

```bash
docker ps
```

### 4. Test the Containerized API

```bash
curl -i http://127.0.0.1:8001/health
```

```bash
curl -i http://127.0.0.1:8001/api/info
```

Both endpoints should return HTTP 200 responses.

---

## Docker Networking

The FastAPI application listens on TCP port `8000` inside the container.

Docker publishes this port on TCP port `8001` of the Ubuntu host's loopback interface.

```text
Ubuntu Host
127.0.0.1:8001
       |
       | Docker Port Publishing
       v
Docker Container
0.0.0.0:8000
       |
       v
FastAPI Application
```

The container uses Docker bridge networking.

The application binds to `0.0.0.0` inside the container so that connections forwarded to its network interface can reach Uvicorn.

The published host port is bound to `127.0.0.1`, limiting access to the host's IPv4 loopback interface.

The container's internal IP address is assigned by Docker and should not be hardcoded into application configuration.

---

## Container Management

### View Running Containers

```bash
docker ps
```

### View Container Logs

```bash
docker logs cloud-ops-api-dev
```

### Follow Container Logs

```bash
docker logs -f cloud-ops-api-dev
```

### Stop the Container

```bash
docker stop cloud-ops-api-dev
```

### Start an Existing Container

```bash
docker start cloud-ops-api-dev
```

### Restart the Container

```bash
docker restart cloud-ops-api-dev
```

**Note:** Use `docker start` to restart an existing stopped container. Running `docker run` again with the same container name will produce a name conflict unless the old container has been removed or renamed.

---

## Troubleshooting

The following checks are useful when diagnosing application or container connectivity issues.

### Check Container Status

```bash
docker ps -a
```

### Inspect Application Logs

```bash
docker logs --tail 50 cloud-ops-api-dev
```

### Inspect Docker Port Mapping

```bash
docker port cloud-ops-api-dev
```

### Inspect Container Network Configuration

```bash
docker inspect cloud-ops-api-dev
```

### Check Host TCP Listening Sockets

```bash
sudo ss -lntp
```

### Inspect Docker Bridge Networking

```bash
ip -br addr show docker0
ip route
docker network inspect bridge
```

### Common Issues

| Issue | Possible Cause | Initial Investigation |
|---|---|---|
| Connection refused | No listener or unavailable published port | Container status and TCP sockets |
| Connection timeout | Network path, firewall, or forwarding issue | Routing, Docker bridge, and logs |
| HTTP 404 | Endpoint not found | Application routes and request URL |
| HTTP 500 | Application or dependency error | Application logs and traceback |
| Container exits immediately | Main process terminates | Container status and logs |
| Port already allocated | Host port is already in use | Docker port mappings and `ss` |

---

## Project Status

**Current Status: Basic API and Docker Containerization Completed**

### Completed Features

- Developed a REST API using FastAPI.
- Implemented health and application information endpoints.
- Configured Python virtual environment and dependency management.
- Built a Docker image using a custom Dockerfile.
- Deployed FastAPI inside a Docker container.
- Configured Docker bridge networking and port publishing.
- Tested HTTP endpoints using curl.
- Practiced container lifecycle management.
- Diagnosed and recovered a Docker bridge routing issue.
- Managed source code using Git.

### Planned Improvements

- Docker Compose for multi-container deployment.
- Nginx reverse proxy integration.
- Kubernetes deployment using k3d.
- Kubernetes Liveness and Readiness Probes.
- Application monitoring and structured logging.
- CI/CD automation using GitHub Actions.
- Improved container security and deployment documentation.

---

## Learning Objectives

This project is developed as a hands-on Cloud/DevOps portfolio project.

Its primary objectives are to demonstrate practical skills in:

- Linux Administration.
- Computer Networking.
- Docker Containerization.
- Cloud-native Application Deployment.
- Infrastructure Troubleshooting.
- Version Control and Automation.

The project is being developed as part of my preparation for Viettel Digital Talent 2027 — Cloud Track.

## License

No license has been selected yet.
