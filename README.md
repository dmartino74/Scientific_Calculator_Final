markdown
# 📊 Scientific Calculator - Final Project

## 🧩 Overview
This repository contains a comprehensive FastAPI application implementing:
- **JWT-based authentication** with user registration and login
- **Advanced calculator** with 7 operation types (add, subtract, multiply, divide, power, modulus, sqrt)
- **User profile management** with username/email updates and password changes
- **Calculation history & statistics** with operation counts and usage analytics
- **Full BREAD functionality** (Browse, Read, Edit, Add, Delete) for calculations
- **Comprehensive testing** (unit, integration, and Playwright E2E tests)
- **CI/CD pipeline** with GitHub Actions for automated testing and Docker deployment

## ✨ New Features (Final Project)

### 1. User Profile & Password Management
- **View Profile**: Get current user's profile information (`GET /users/me`)
- **Update Profile**: Change username and/or email (`PUT /users/me`)
- **Change Password**: Securely change password with old password verification (`POST /users/me/change-password`)
- **Frontend**: New `profile.html` page for profile management

### 2. Advanced Calculation Operations
- **Power (Exponentiation)**: Calculate a^b (e.g., 2^3 = 8)
- **Modulus**: Calculate remainder of division (e.g., 10 % 3 = 1)
- **Square Root**: Calculate √a (e.g., √16 = 4)
- All operations include proper error handling (divide by zero, negative square root, etc.)

### 3. Statistics & Analytics
- **View Statistics**: Get comprehensive calculation analytics (`GET /calculations/stats/summary`)
  - Total calculations count
  - Operation counts by type
  - Average values of operands
  - Most frequently used operation
- **Frontend**: Statistics display in `calculations.html`

## ⚙️ Features
- JWT‑based user registration and login with secure password hashing (bcrypt)
- **7 calculation operations**: add, subtract, multiply, divide, power, modulus, sqrt
- **Full BREAD operations** for calculations (Browse, Read, Edit, Add, Delete)
- **User profile management**: view and update username/email
- **Password change**: secure password updates with verification
- **Statistics dashboard**: view calculation history and analytics
- Pydantic schemas for robust input validation
- Static front‑end pages with client‑side validation:
  - `static/register.html` - User registration
  - `static/login.html` - User login
  - `static/calculations.html` - Calculator with BREAD operations and statistics
  - `static/profile.html` - Profile management and password change
- Comprehensive test suite:
  - Unit tests for calculation logic and password handling
  - Integration tests with in-memory database
  - Playwright E2E tests for complete workflows
- GitHub Actions CI/CD workflow for automated testing and Docker deployment

## 📡 API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - Login and get JWT token

### User Profile
- `GET /users/me` - Get current user profile (requires auth)
- `PUT /users/me` - Update username and/or email (requires auth)
- `POST /users/me/change-password` - Change password (requires auth)

### Calculations (All require authentication)
- `GET /calculations` - Browse all user's calculations
- `GET /calculations/{id}` - Read single calculation
- `POST /calculations` - Add new calculation
- `PUT /calculations/{id}` - Edit existing calculation
- `DELETE /calculations/{id}` - Delete calculation
- `GET /calculations/stats/summary` - Get calculation statistics

### Supported Operations
- `add` - Addition (a + b)
- `subtract` - Subtraction (a - b)
- `multiply` - Multiplication (a × b)
- `divide` - Division (a ÷ b)
- `power` - Exponentiation (a^b)
- `modulus` - Modulus (a % b)
- `sqrt` - Square root (√a)

## 🚀 Quick Start (Local Development)
## 🚀 Quick Start (Local Development)

### 1. Clone and Setup
```bash
git clone https://github.com/dmartino74/Scientific_Calculator_Final.git
cd Scientific_Calculator_Final
```

### 2. Create Virtual Environment
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m playwright install --with-deps
```

### 4. Start the Application
```bash
uvicorn app.main:app --reload
```

### 5. Access the Application
- **Calculator & BREAD**: http://127.0.0.1:8000/static/calculations.html
- **Profile Management**: http://127.0.0.1:8000/static/profile.html
- **Registration**: http://127.0.0.1:8000/static/register.html
- **Login**: http://127.0.0.1:8000/static/login.html
- **API Docs**: http://127.0.0.1:8000/docs

## 🧪 Running Tests

### Unit Tests (Fast)
Test calculation logic, password hashing, and data validation:
```bash
pytest tests/unit -v
```

### Integration Tests
Test API endpoints with database:
```bash
pytest tests/integration -v
```

### E2E Playwright Tests
Test complete user workflows via browser:
```bash
# Make sure application is running first
pytest tests/e2e -v
```

### Run All Tests
```bash
pytest -v
```

### Run Specific Test Files
```bash
# Test advanced features
pytest tests/unit/test_advanced_features.py -v
pytest tests/integration/test_advanced_features.py -v
pytest tests/e2e/test_advanced_features_playwright.py -v
```

### Test Coverage
```bash
pytest --cov=app --cov-report=html
# View coverage report: open htmlcov/index.html
```

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t yourusername/scientific-calculator:latest .
```

### Run with Docker
```bash
docker run -p 8000:8000 \
  --env DATABASE_URL="postgresql://user:pass@host:5432/dbname" \
  yourusername/scientific-calculator:latest
```

### Docker Hub
Pre-built images available at: `dmartino74/scientific-calculator`

## 🔄 CI/CD Pipeline (GitHub Actions)

The `.github/workflows/ci.yml` workflow automatically:
1. **Runs on**: Push/PR to `main` branch
2. **Sets up**: Python 3.12, PostgreSQL service, Playwright browsers
3. **Tests**: Runs complete test suite (unit + integration + E2E)
4. **Builds**: Creates Docker image on test success
5. **Deploys**: Pushes image to Docker Hub with authentication

### Required GitHub Secrets
Configure these in your repository Settings → Secrets:
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

## 📁 Project Structure
```
Scientific_Calculator_Final/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── db.py                # Database configuration
│   ├── security.py          # Password hashing & JWT
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── calculation.py   # Calculation model
│   ├── routes/
│   │   ├── users.py         # Auth & profile endpoints
│   │   └── calculations.py  # Calculator & stats endpoints
│   └── operations/schemas/
│       ├── user_schemas.py         # User validation schemas
│       └── calculation_schemas.py  # Calculation schemas
├── static/
│   ├── register.html        # Registration page
│   ├── login.html          # Login page
│   ├── calculations.html   # Calculator with BREAD & stats
│   └── profile.html        # Profile management
├── tests/
│   ├── unit/
│   │   ├── test_calculator.py          # Basic calc tests
│   │   └── test_advanced_features.py   # Advanced feature tests
│   ├── integration/
│   │   ├── test_users.py                    # Auth tests
│   │   ├── test_fastapi_calculator.py       # Calc API tests
│   │   └── test_advanced_features.py        # Advanced API tests
│   └── e2e/
│       ├── test_calculations_playwright.py       # BREAD E2E
│       └── test_advanced_features_playwright.py  # Advanced E2E
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── create_tables.py        # Database initialization
└── README.md              # This file
```

## 🎯 Learning Outcomes Demonstrated

### CLO3: Python Applications with Automated Testing
- ✅ Comprehensive unit tests for calculation logic and security functions
- ✅ Integration tests for API endpoints with database
- ✅ E2E tests for complete user workflows

### CLO4: GitHub Actions CI/CD
- ✅ Automated test execution on every push/PR
- ✅ Docker build and deployment pipeline
- ✅ PostgreSQL service integration in CI

### CLO9: Containerization with Docker
- ✅ Dockerfile for application containerization
- ✅ Docker Compose for multi-container setup
- ✅ Docker Hub image publishing

### CLO10: REST API Creation & Testing
- ✅ RESTful endpoints with proper HTTP methods
- ✅ JWT-based authentication
- ✅ Comprehensive API testing

### CLO11: SQL Database Integration
- ✅ SQLAlchemy ORM for database operations
- ✅ User and Calculation models with relationships
- ✅ CRUD operations with proper data persistence

### CLO12: JSON Serialization with Pydantic
- ✅ Request/response validation schemas
- ✅ Email validation and custom validators
- ✅ Type safety and data validation

### CLO13: Security Best Practices
- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Secure password change workflow
- ✅ User-scoped data access

## 📝 Testing Examples

### Example: Test Advanced Calculations
```python
# Unit test
def test_power_operation():
    assert 2 ** 3 == 8

# Integration test
def test_power_calculation_api(client, auth_headers):
    response = client.post("/calculations", json={
        "a": 2, "b": 3, "type": "power"
    }, headers=auth_headers)
    assert response.json()["result"] == 8

# E2E test
def test_power_calculation_ui(page, unique_user):
    # Register, create power calc, verify result
    ...
```

### Example: Test Password Change
```python
# Integration test
def test_change_password_and_relogin(client):
    # Register user
    # Change password
    # Login with new password
    # Assert success
    ...
```

### Example: Test Statistics
```python
# Integration test
def test_statistics_with_calculations(client, auth_headers):
    # Create multiple calculations
    response = client.get("/calculations/stats/summary", 
                         headers=auth_headers)
    data = response.json()
    assert data["total_calculations"] == 5
    assert data["most_used_operation"] == "add"
    ...
```

## 🌐 Frontend Features

### Calculations Page (`calculations.html`)
- Registration and login forms
- Calculator with 7 operations
- BREAD operations (list, edit, delete)
- Statistics dashboard
- Real-time result display

### Profile Page (`profile.html`)
- View current profile information
- Update username and email
- Change password with verification
- Secure re-login after password change

## 🔒 Security Features
- Passwords hashed with bcrypt (72-byte limit enforced)
- JWT tokens with expiration
- User-scoped data access (calculations isolated per user)
- Input validation with Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM
- HTTPS-ready configuration

## 📊 Statistics Features
- Total calculations count
- Operation breakdown by type
- Average operands (a and b)
- Most frequently used operation
- Real-time updates after new calculations

## 🛠️ Development

### Adding New Operations
1. Update valid_types list in `app/routes/calculations.py`
2. Add calculation logic in add_calculation and edit_calculation
3. Update front-end dropdowns in HTML files
4. Write unit, integration, and E2E tests

### Database Migrations (Optional with Alembic)
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new field"

# Apply migration
alembic upgrade head
```

## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License
See LICENSE file for details.

## 👤 Author
**David Martino**
- GitHub: [@dmartino74](https://github.com/dmartino74)
- Repository: [Scientific_Calculator_Final](https://github.com/dmartino74/Scientific_Calculator_Final)

## 🙏 Acknowledgments
- FastAPI framework for excellent API development
- SQLAlchemy for robust ORM
- Playwright for reliable E2E testing
- GitHub Actions for seamless CI/CD

---

**Note**: This project demonstrates comprehensive full-stack development with Python, covering backend APIs, database management, frontend integration, security, testing, and DevOps practices.
- If you prefer to run CI without Playwright browser installation, I can make Playwright optional in the workflow.

Reflection & Submission Checklist
- Implemented: BREAD endpoints for calculations (user-scoped), frontend demo page, integration & Playwright tests, CI workflow that runs tests and builds Docker image.
- Still to collect: screenshots of a successful GitHub Actions run and a Docker Hub image push (these require the workflow to run with `DOCKER_*` secrets configured).

If you want, I can now:
- Update `reflection.md` with a narrative reflection (I will add that next),
- Add placeholders for screenshots and guidance on how to capture them,
- Or trigger additional changes you prefer.