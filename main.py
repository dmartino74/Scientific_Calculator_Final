from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from typing import List

from operations import get_operation
from models.calculation import Base, Calculation
from db import engine, get_db
from schemas import CalculationRead  # ✅ Uses your existing schema
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ✅ Create tables at startup
Base.metadata.create_all(bind=engine)

OPERATION_MAP = {
    "add": "Add",
    "addition": "Add",
    "plus": "Add",
    "sub": "Sub",
    "subtract": "Sub",
    "minus": "Sub",
    "multiply": "Multiply",
    "times": "Multiply",
    "mul": "Multiply",
    "divide": "Divide",
    "div": "Divide"
}

class CalculationRequest(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")
    type: str = Field(..., description="Operation type")

    @field_validator('a', 'b')
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Operands must be numeric.")
        return value

    @field_validator('type')
    def validate_type(cls, value):
        if value.lower() not in OPERATION_MAP:
            raise ValueError(f"Unsupported operation type: {value}")
        return value

class CalculationResponse(BaseModel):
    result: float

class ErrorResponse(BaseModel):
    error: str

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(status_code=400, content={"error": error_messages})

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_model=CalculationResponse, responses={400: {"model": ErrorResponse}})
async def calculate(operation: CalculationRequest, db: Session = Depends(get_db)):
    try:
        normalized_type = OPERATION_MAP.get(operation.type.lower())
        op = get_operation(normalized_type)
        result = op.compute(operation.a, operation.b)

        # ✅ Save to database
        calc = Calculation(a=operation.a, b=operation.b, type=normalized_type, result=result)
        db.add(calc)
        db.commit()
        db.refresh(calc)

        return CalculationResponse(result=result)
    except ValueError as e:
        logger.error(f"Calculation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ New route to list all records
@app.get("/records", response_model=List[CalculationRead])
async def get_all_records(db: Session = Depends(get_db)):
    return db.query(Calculation).all()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
