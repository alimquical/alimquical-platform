"""Launcher script - sets env vars and starts the server."""
import os
import sys
import subprocess

os.environ.setdefault("DATABASE_URL", "sqlite:///./alimquical.db")
os.environ.setdefault("SECRET_KEY", "dev-secret-key-1234567890abcdef")
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DEBUG", "true")

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
