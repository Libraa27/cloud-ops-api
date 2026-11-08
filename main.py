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
