import subprocess
import time
import socket
import os
import signal
import pytest


@pytest.fixture(scope="session")
def server_url():
    """Start a uvicorn server in the background and yield the base URL.

    Note: This starts a separate process that serves the full app (uses DATABASE_URL env).
    In CI the workflow provides Postgres; locally you may need to run Postgres or adapt DATABASE_URL.
    """
    env = os.environ.copy()
    # If no DATABASE_URL is provided in the environment, use a local sqlite file
    if not env.get("DATABASE_URL"):
        env["DATABASE_URL"] = f"sqlite:///{os.path.abspath('test_playwright.db')}"
    # Use port 8000 (matches CI workflow)
    port = int(env.get("PORT", 8000))
    cmd = [
        env.get("PYTHON", "python"),
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ]

    # Start server process
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for port to be ready
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                break
        except OSError:
            time.sleep(0.1)
    else:
        proc.kill()
        raise RuntimeError("Uvicorn server did not start in time")

    yield f"http://127.0.0.1:{port}"

    # Teardown
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
