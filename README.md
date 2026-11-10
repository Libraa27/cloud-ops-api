# Cloud Ops API

A containerized HTTP service monitoring application built with Python, FastAPI, Docker Compose, and Nginx.

This project demonstrates practical Cloud Computing and DevOps engineering concepts, including container networking, reverse proxy configuration, service health monitoring, infrastructure troubleshooting, and automated testing.

The application is developed as a hands-on portfolio project for Viettel Digital Talent 2027 — Cloud Track.

## Features

- REST API development using FastAPI.
- Docker-based application containerization.
- Multi-container deployment with Docker Compose.
- Nginx reverse proxy and HTTP request routing.
- Docker DNS and internal service communication.
- On-demand HTTP service health monitoring.
- Response time measurement.
- HTTP error and connection failure handling.
- Automated unit testing using Python unittest.
- Controlled failure simulation and service recovery.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Application development |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Docker | Application containerization |
| Docker Compose | Multi-container deployment |
| Nginx | Reverse proxy and HTTP monitoring target |
| Ubuntu Linux | Development and deployment environment |
| Git & GitHub | Version control and source code hosting |
| unittest | Automated unit testing |
| unittest.mock | HTTP response and failure simulation |

## System Architecture

The application currently consists of three Docker Compose services:

1. **nginx** — Receives HTTP requests and forwards them to FastAPI.
2. **api** — Provides REST endpoints and performs HTTP health checks.
3. **target** — A separate Nginx HTTP server used as a monitoring target.

```text
                   Ubuntu Host
                        |
                        | HTTP
                        | 127.0.0.1:8081
                        v
              +-------------------+
              |   Nginx Proxy     |
              |    Port 80        |
              +-------------------+
                        |
                        | Docker Internal Network
                        | http://api:8000
                        v
              +-------------------+
              |   FastAPI         |
              |   Monitoring API  |
              |    Port 8000      |
              +-------------------+
                        |
                        | HTTP Health Check
                        | http://target:80/
                        v
              +-------------------+
              |   Target Service  |
              |   Nginx HTTP      |
              |    Port 80        |
              +-------------------+
```

### Architecture Design

Docker Compose creates a user-defined network for the application.

Services communicate using Docker DNS and their service names rather than hardcoded container IP addresses.

For example:

```text
http://api:8000
http://target:80
```

Only the Nginx reverse proxy publishes a port to the Ubuntu host.

The FastAPI and target services communicate through the internal Docker network without publishing their ports to the host.

The current setup is intended for local development and infrastructure experimentation.

## Project Structure

```text
cloud-ops-api/
├── main.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── nginx/
│   └── default.conf
├── tests/
│   └── test_monitor.py
├── .dockerignore
├── .gitignore
└── README.md
```

### Main Components

| File | Description |
|---|---|
| `main.py` | FastAPI application and monitoring logic |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | FastAPI container image definition |
| `compose.yaml` | Multi-container service configuration |
| `nginx/default.conf` | Nginx reverse proxy configuration |
| `tests/test_monitor.py` | Automated monitoring unit tests |
| `.dockerignore` | Excludes unnecessary files from Docker build context |
| `.gitignore` | Excludes local development files from Git |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Basic FastAPI application health check |
| GET | `/api/info` | Application information |
| GET | `/api/monitor/target` | Check the availability and health of the target service |

### 1. Health Endpoint

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

This endpoint confirms that the FastAPI application is running and can process requests.

It does not verify external services or infrastructure dependencies.

### 2. Application Information Endpoint

```http
GET /api/info
```

Example response:

```json
{
  "name": "cloud-ops-api",
  "version": "0.1.0",
  "environment": "development"
}
```

### 3. Service Monitoring Endpoint

```http
GET /api/monitor/target
```

This endpoint performs an HTTP request to:

```text
http://target:80/
```

The target hostname is resolved using Docker's internal DNS.

The monitoring function:

1. Records the start time.
2. Sends an HTTP request to the target.
3. Reads the HTTP status code.
4. Measures the elapsed time.
5. Handles HTTP and connection errors.
6. Returns a structured JSON result.

#### Example: Healthy Target

```json
{
  "service": "target",
  "reachable": true,
  "healthy": true,
  "status_code": 200,
  "response_time_ms": 12.0,
  "error": null
}
```

The response time is measured dynamically and varies between requests.

#### Example: Unreachable Target

```json
{
  "service": "target",
  "reachable": false,
  "healthy": false,
  "status_code": null,
  "response_time_ms": 4005.97,
  "error": "<urlopen error [Errno -3] Temporary failure in name resolution>"
}
```

This example is based on a controlled failure simulation in which the target container was stopped.

The exact error message and elapsed time depend on the network conditions and failure mechanism.

### Understanding Monitoring Results

| Condition | reachable | healthy | status_code |
|---|---|---|---|
| Target returns HTTP 200 | true | true | 200 |
| Target returns HTTP 500 | true | false | 500 |
| Target cannot be reached | false | false | null |

**Reachable** indicates whether an HTTP response was received.

**Healthy** indicates whether the HTTP status code equals 200.

An HTTP error response such as 500 still indicates that the server was reachable, even though the health check failed.

### Monitoring API HTTP Status

The monitoring endpoint may return HTTP 200 even when the target is unhealthy.

This is because the monitoring endpoint successfully processed the request and reported the target's condition.

Clients should inspect the JSON fields `reachable` and `healthy` instead of relying only on the monitoring endpoint's own HTTP status code.

### Current Monitoring Limitations

- Monitoring is performed on demand when the endpoint is called.
- The application does not perform background or scheduled checks.
- The target URL is predefined in the application code.
- Health is currently determined by HTTP status 200.
- Monitoring results are not stored in a database.
- No alerting or historical monitoring dashboard is implemented.
- The request timeout does not guarantee a strict upper bound on total DNS resolution time.

These features may be developed in future milestones.

---

## Getting Started — Local Development

This section describes how to run FastAPI directly on Ubuntu without Docker.

### Prerequisites

- Ubuntu Linux
- Python 3.10
- Python virtual environment support
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Libraa27/cloud-ops-api.git
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

### 5. Start FastAPI

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Application URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Test the Local API

Open another terminal and run:

```bash
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/api/info
```

Both endpoints should return HTTP 200 responses.

**Important:** The monitoring endpoint depends on the predefined hostname `target`, which is normally available through Docker Compose networking.

When running FastAPI directly on Ubuntu, this hostname may not resolve. Use the Docker Compose deployment below to test the monitoring functionality.

---

## Running with Docker

Docker packages the Python runtime, application dependencies, and source code into a container image.

### Prerequisites

Docker Engine must be installed and running.

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

The application is accessible at:

```text
http://127.0.0.1:8001
```

Interactive documentation:

```text
http://127.0.0.1:8001/docs
```

### 3. Verify Container Status

```bash
docker ps
```

### 4. Test Basic API Endpoints

```bash
curl -i http://127.0.0.1:8001/health
curl -i http://127.0.0.1:8001/api/info
```

This standalone Docker deployment is intended for basic application testing.

The monitoring target is not included in this single-container setup.

### 5. Stop the Container

```bash
docker stop cloud-ops-api-dev
```

### 6. Start the Existing Container

```bash
docker start cloud-ops-api-dev
```

If a container with the same name already exists, do not run the original `docker run` command again without first removing or renaming the existing container.

---

## Running with Docker Compose

Docker Compose is the recommended method for running the complete monitoring application.

It manages all three services and their internal network.

### 1. Build and Start the Services

From the project directory:

```bash
docker compose up -d --build
```

This command:

- Builds the FastAPI image.
- Creates the Docker Compose network when needed.
- Starts the FastAPI service.
- Starts the Nginx reverse proxy.
- Starts the monitoring target service.

### 2. Check Container Status

```bash
docker compose ps
```

Expected services:

```text
api
nginx
target
```

All three services should be running.

### 3. Test API Endpoints

```bash
curl -i http://127.0.0.1:8081/health
curl -i http://127.0.0.1:8081/api/info
curl -i http://127.0.0.1:8081/api/monitor/target
```

### 4. Access Interactive API Documentation

From the Ubuntu host:

```text
http://127.0.0.1:8081/docs
```

### 5. Inspect Logs

```bash
docker compose logs --tail=20 nginx api target
```

To follow logs in real time:

```bash
docker compose logs -f nginx api target
```

Press `Ctrl + C` to stop following logs.

### 6. Stop and Remove Compose Resources

```bash
docker compose down
```

This stops and removes the Compose containers and default network.

It does not remove the application's source code, Git history, or Docker images.

To recreate the application:

```bash
docker compose up -d --build
```

---

## Docker Networking

### Reverse Proxy Port Mapping

The Nginx container listens on TCP port 80.

Docker publishes this port on the Ubuntu host's loopback interface:

```text
127.0.0.1:8081 -> nginx:80
```

This allows requests originating on the Ubuntu host to reach Nginx.

### Internal Service Networking

The FastAPI service listens on port 8000 inside its container.

The target service listens on port 80 inside its container.

Neither service publishes its port to the host in the Docker Compose deployment.

Services communicate through the default Docker Compose network.

### Docker DNS

Docker Compose provides service-name resolution through Docker's internal DNS.

For example, Nginx forwards requests to:

```text
http://api:8000
```

FastAPI checks the target service at:

```text
http://target:80/
```

Container IP addresses can change when containers are recreated.

Using service names avoids hardcoding those addresses in the application configuration.

### Nginx Reverse Proxy

The reverse proxy configuration is defined in:

```text
nginx/default.conf
```

The relevant upstream directive is:

```nginx
proxy_pass http://api:8000;
```

This forwards matching HTTP requests to the FastAPI service.

---

## Automated Testing

The project uses Python's built-in `unittest` framework and `unittest.mock` for automated testing.

Tests are located in:

```text
tests/test_monitor.py
```

### Current Test Scenarios

| Test | Scenario | Expected Result |
|---|---|---|
| `test_healthy_target` | Target returns HTTP 200 | Reachable and healthy |
| `test_unhealthy_target` | Target returns HTTP 500 | Reachable but unhealthy |
| `test_unreachable_target` | Target encounters a DNS-related error | Unreachable and unhealthy |

### How Mocking Works

Unit tests replace the outgoing HTTP request function with a mock object.

This allows the monitoring logic to be tested without making actual network requests.

Benefits include:

- Fast execution.
- Predictable results.
- Independence from target container availability.
- Easier testing of error scenarios.

### Run Unit Tests

From the project directory:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

If the virtual environment has not been created, follow the Local Development setup instructions first.

### Verified Results

The initial test suite completed successfully:

```text
test_healthy_target ... ok
test_unhealthy_target ... ok
test_unreachable_target ... ok

Ran 3 tests

OK
```

### Testing Limitations

The current tests validate the monitoring function using mocked responses.

They do not fully test:

- Nginx-to-FastAPI request forwarding.
- Real Docker networking failures.
- All HTTP error codes.
- Every timeout condition.
- Complete application integration.

Additional integration tests and automated CI workflows are planned.

---

## Troubleshooting

Infrastructure troubleshooting is an important part of this project.

Several controlled failures have been simulated and investigated during development.

### 1. Check Container Status

For Docker Compose:

```bash
docker compose ps -a
```

For all Docker containers:

```bash
docker ps -a
```

### 2. Inspect Application Logs

```bash
docker compose logs --tail=50 api
```

### 3. Inspect Nginx Logs

```bash
docker compose logs --tail=50 nginx
```

### 4. Inspect Target Logs

```bash
docker compose logs --tail=50 target
```

### 5. Verify Docker DNS

```bash
docker compose exec nginx getent hosts api
```

This checks whether the Nginx container can resolve the FastAPI service name.

### 6. Check Docker Networks

```bash
docker network ls
```

Inspect the default Compose network:

```bash
docker network inspect cloud-ops-api_default
```

### 7. Inspect Linux Routing

```bash
ip -br addr
ip route
```

### 8. Inspect TCP Listening Sockets

```bash
sudo ss -lntp
```

### Common Problems

| Problem | Possible Cause | Initial Investigation |
|---|---|---|
| Connection refused | Missing TCP listener or unavailable published port | Container status and `ss` |
| Connection timeout | Routing, firewall, forwarding, or upstream connectivity issue | Docker network, routes, and logs |
| HTTP 502 | Reverse proxy cannot obtain a valid upstream response | Nginx logs and backend status |
| HTTP 504 | Reverse proxy upstream timeout | Nginx timeout configuration and logs |
| HTTP 404 | Requested endpoint not found | Request URL and application routes |
| HTTP 500 | Application or upstream processing error | Application logs and traceback |
| DNS resolution failure | Service name cannot be resolved | Container status and Docker DNS |
| Container exits immediately | Main process terminates | Container logs and exit code |
| Port already allocated | Host port is already in use | Docker port mappings and TCP listeners |

---

## Troubleshooting Exercises

### Exercise 1 — FastAPI Backend Failure

During the Docker Compose and Nginx deployment milestone, the FastAPI service was stopped while Nginx remained running.

Command:

```bash
docker compose stop api
```

An HTTP request through Nginx timed out at the client after 10 seconds.

After restarting FastAPI:

```bash
docker compose start api
```

HTTP 200 responses were restored.

This exercise demonstrated reverse proxy dependency failures and service recovery.

### Exercise 2 — Monitoring Target Failure

During the service monitoring milestone, the target service was stopped:

```bash
docker compose stop target
```

The monitoring API reported:

```json
{
  "service": "target",
  "reachable": false,
  "healthy": false,
  "status_code": null,
  "response_time_ms": 4005.97,
  "error": "<urlopen error [Errno -3] Temporary failure in name resolution>"
}
```

After restarting the target:

```bash
docker compose start target
```

The monitoring API detected that the target was healthy again.

This exercise demonstrated:

- Service availability monitoring.
- DNS resolution failure handling.
- Error reporting.
- Service recovery verification.

### Exercise 3 — Docker Bridge Routing Issue

During initial Docker deployment, a connectivity problem occurred between the Ubuntu host and a running container.

Investigation showed that the default Docker bridge had lost its expected IPv4 address, causing incorrect routing toward the container network.

The bridge address was temporarily restored, after which the application returned HTTP 200.

The underlying cause of the address loss has not yet been established.

This exercise provided practical experience with:

- Linux interface configuration.
- Docker bridge networking.
- Routing table inspection.
- Host-to-container connectivity troubleshooting.

---

## Project Status

**Current Status: Docker Compose Deployment, HTTP Service Monitoring, and Initial Unit Testing Completed**

### Completed Features

- FastAPI REST API development.
- Basic health and application information endpoints.
- Python dependency and virtual environment management.
- Docker image creation using a custom Dockerfile.
- Container lifecycle management.
- Docker Compose multi-container deployment.
- Nginx reverse proxy configuration.
- Docker DNS and internal networking.
- HTTP monitoring for a predefined target service.
- Response time measurement.
- HTTP error and connection failure handling.
- Controlled service failure simulations.
- Service recovery verification.
- Three automated unit tests using unittest and mocks.
- Git and GitHub version control.

### Planned Improvements

- Additional automated tests and integration tests.
- More configurable monitoring targets and health criteria.
- Structured application logging.
- Persistent monitoring history.
- Prometheus metrics collection.
- Grafana monitoring dashboards.
- Kubernetes deployment using k3d.
- Kubernetes Liveness and Readiness Probes.
- Resource requests and limits.
- Automated CI/CD using GitHub Actions.
- Container security improvements.
- More comprehensive failure simulation and operational documentation.

---

## Learning Objectives

This project is being developed to strengthen practical skills in:

- Linux Administration.
- Computer Networking.
- Docker Containerization.
- Docker Compose and service networking.
- HTTP and Reverse Proxy architecture.
- Python application development.
- Service Monitoring and Troubleshooting.
- Automated Testing.
- Kubernetes Fundamentals.
- CI/CD and Infrastructure Automation.

The long-term goal is to build, deploy, monitor, and troubleshoot a small cloud-native application infrastructure.

---

## License

No license has been selected yet.
