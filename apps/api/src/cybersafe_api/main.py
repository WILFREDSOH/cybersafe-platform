from fastapi import FastAPI

app =  FastAPI(
       	title="CyberSafe API",
	desciption="API backend for the CyberSafe cybersecurity platform.",
	version="0.1.0",
       )


@app.get("/health")
async def health_check() -> dict[str, str]:
	"""Return the current API health status."""
	return {
		"status": "ok",
		"service":"cybersafe-api",
	} 
