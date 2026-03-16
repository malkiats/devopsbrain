"""
Vercel serverless entry point for DevOpsBrain.

Vercel invokes this file for all requests matched by vercel.json rewrites.
Mangum adapts the FastAPI ASGI app to the Vercel / AWS Lambda runtime.
"""

import os
import sys
from pathlib import Path

# Make the backend package importable from the project root structure.
_repo_root = Path(__file__).resolve().parent.parent
_backend_dir = _repo_root / "backend"
sys.path.insert(0, str(_backend_dir))

from api.app import app  # noqa: E402
from mangum import Mangum  # noqa: E402

handler = Mangum(app, lifespan="off")
