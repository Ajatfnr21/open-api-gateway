#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from typing import Dict
import click

app = FastAPI()

services: Dict[str, str] = {
    "users": "http://localhost:8001",
    "orders": "http://localhost:8002"
}

@app.get("/gateway/{service}/{path:path}")
async def gateway(service: str, path: str):
    if service not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"service": service, "path": path, "backend": services[service]}

@app.get("/health")
async def health():
    return {"status": "healthy", "services": list(services.keys())}

@click.command()
@click.option('--port', default=8080)
def serve(port):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    serve()
