Submission checklist and screenshot guidance

Files to include in your assignment upload or repository link:

- Source code: the repository root (contains `app/`, `static/`, `tests/`, etc.)
- `README.md`: instructions to run the app and tests (updated for Module 14)
- `reflection.md`: narrative reflection of work and challenges
- `screenshots/*`: screenshots described below (or attach separately when submitting)

Required screenshots (save in `screenshots/` or attach separately):

- `ci_success.png`: GitHub Actions workflow run page showing both `test` and `docker` jobs completed successfully. Capture the run summary and the expanded job list showing the test and docker stages.
- `docker_push.png`: Docker Hub repository page showing the newly pushed image tag (e.g., `youruser/scientific_calculator_final:latest`). Include the repository name and timestamp visible.
- `bread_frontend_create.png`: The `calculations.html` page after creating a calculation showing the created ID or result.
- `bread_frontend_list.png`: The `calculations.html` page showing the browse/list view with multiple calculations.
- `bread_frontend_edit_delete.png`: Evidence of editing and deleting a calculation (before/after or the UI message confirming deletion).

How to capture the screenshots

1. GitHub Actions: After you push and the workflow completes, open the run on GitHub -> click the workflow run -> take a screenshot of the run page showing job success. Save as `ci_success.png`.
2. Docker Hub: After CI pushes the image, go to `https://hub.docker.com/repository/docker/<youruser>/scientific_calculator_final/tags` and capture the tags list showing `latest` (or the commit SHA tag). Save as `docker_push.png`.
3. Frontend interactions: Run the app locally (`uvicorn app.main:app --reload`), open `http://127.0.0.1:8000/static/calculations.html`, perform the Create/List/Edit/Delete flows and capture the browser window showing the result messages and list views. Save as the filenames above.

Packaging for submission

1. Put the screenshots in `screenshots/` in the repo OR save them locally for upload.
2. Ensure `README.md` and `reflection.md` are up-to-date with links and explanations.
3. Zip or push the repo and include the screenshot files when uploading to the assignment portal.

Notes

- If you prefer CI to run Playwright E2E, set the repository secret `RUN_E2E` to `true` before pushing. Otherwise, CI will skip the Playwright E2E steps and run only unit/integration tests.
- To enable Docker image pushes in CI, add `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets in GitHub repository settings.
