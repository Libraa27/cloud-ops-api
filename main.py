import time
import urllib.error
import urllib.request

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/info")
def get_app_info():
    return {
        "name": "cloud-ops-api",
        "version": "0.1.0",
        "environment": "development"
    }


@app.get("/api/monitor/target")
def monitor_target():
    start = time.perf_counter()

    reachable = False
    status_code = None
    error_message = None

    try:
        with urllib.request.urlopen(
            "http://target:80/", timeout=3
        ) as response:
            status_code = response.status
            reachable = True

    except urllib.error.HTTPError as exc:
        reachable = True
        status_code = exc.code
        error_message = str(exc)

    except (urllib.error.URLError, TimeoutError) as exc:
        error_message = str(exc)

    response_time_ms = round(
        (time.perf_counter() - start) * 1000, 2
    )

    return {
        "service": "target",
        "reachable": reachable,
        "healthy": status_code == 200,
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        "error": error_message
    }
