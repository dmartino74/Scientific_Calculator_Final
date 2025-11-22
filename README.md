markdown
# 📊 Module 13: JWT Login/Registration with Client-Side Validation & Playwright E2E

## 🧩 Overview
This repository contains a FastAPI application that implements JWT‑based user registration and login, front‑end pages for registration and login, automated tests (unit, integration, and Playwright E2E), and a GitHub Actions CI/CD pipeline that runs tests and builds/pushes a Docker image.

## ⚙️ Features
- JWT‑based registration and login endpoints (`/users/register`, `/users/login`)
- Secure password hashing with bcrypt and JWT token creation/verification
- Pydantic schemas for input validation (email format, password length, etc.)
- Static front‑end pages (`static/register.html`, `static/login.html`) with client‑side validation
- Playwright browser E2E tests covering positive and negative flows
- GitHub Actions workflow to run tests and build/push Docker images to Docker Hub

## 🚀 How to Run Locally
1. **Clone the Repository**
   ```bash
   git clone https://github.com/dmartino74/module13_is601.git
   cd module13_is601
Create and Activate Virtual Environment

bash
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate.bat  # Windows
Install Dependencies

bash
pip install -r requirements.txt
python -m pip install pytest-playwright
python -m playwright install --with-deps
Start the App

bash
uvicorn app.main:app --reload
The app will serve static pages at http://localhost:8000/static/.

🧪 Run Tests
Run all tests (unit, integration, E2E):

bash
pytest -q
Unit and integration tests run against an in‑memory SQLite DB by default.

Playwright E2E tests require a running database. In CI, a Postgres service is used. Locally, set DATABASE_URL to a running Postgres instance or adjust to your environment.

🐳 Docker
Build and run the image locally:

bash
docker build -t module13_is601:latest .
docker run -d -p 8000:8000 --name module13_container module13_is601:latest
🔁 CI/CD Pipeline
GitHub Actions automates:

🧪 Test job: runs pytest (unit, integration, Playwright E2E) on each push/PR

🐳 Docker job: builds and pushes image to Docker Hub if tests pass

📎 Submission Checklist
[x] JWT registration & login endpoints

[x] Pydantic validation for user inputs

[x] Front‑end register.html and login.html with client‑side validation

[x] Playwright browser E2E tests added (positive and negative flows)

[x] GitHub Actions workflow runs tests and builds Docker image

[x] Coverage report generated (htmlcov)

🧠 Reflection
This module reinforced key backend and DevOps skills:

Implemented secure authentication with bcrypt and JWT

Integrated client‑side validation with front‑end pages

Automated testing across unit, integration, and browser E2E layers

Used GitHub Actions to automate CI/CD and Docker deployment

Debugged flaky Playwright tests and applied xfail markers to keep the pipeline green

Challenges included aligning client‑side validation with Playwright expectations, handling bcrypt’s 72‑byte password limit, and ensuring reproducible CI/CD runs with Postgres in GitHub Actions.

Code

---

This version is streamlined: no leftover Module 12 content, clear instructions, and a reflection section that matches your actual experience (bcrypt limit, Playwright flakiness, CI/CD).  

You can now add screenshots (GitHub Actions run, Playwright output, front‑end pages) and your Docker Hub link to finalize submission.  

Would you like me to also draft the **reflection document** in a narrative style (separate