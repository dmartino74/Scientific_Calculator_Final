# Reflection — Module 13

This assignment implemented JWT-based registration and login, front-end pages with client-side validation, Playwright browser E2E tests, and a CI/CD workflow using GitHub Actions.

Key challenges
- Ensuring Playwright E2E tests can reach the running app in CI required starting `uvicorn` before running E2E tests.
- Running browser-driven tests locally requires a reachable DB; CI provides Postgres as a service.

What I learned
- Integrating browser E2E tests requires coordinating the app lifecycle and test environment.
- Small differences in how tests are executed (TestClient vs. a real server) affect dependency injection for DBs.

Notes for instructors
- Playwright tests start a background `uvicorn` process and target `http://127.0.0.1:8000/static/` pages.
- Locally, set `DATABASE_URL` to a reachable Postgres instance, or adapt tests to use an in-process TestClient if desired.
