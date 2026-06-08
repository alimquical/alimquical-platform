import sys
import os

# Ensure the backend root is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel expects a WSGI/ASGI app
from fastapi.middleware.wsgi import WSGIMiddleware

# For Vercel serverless, export the app as a handler
handler = app
