from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import math

from app.db import get_db
from app.models.calculation import Calculation
from app.models.user import User
from app.operations.schemas.calculation_schemas import CalculationCreate, CalculationRead, CalculationStatistics
from app.security import decode_access_token

# HTTP bearer security for extracting JWT
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Depends = Depends(get_db)) -> User:
    """Dependency to get the currently authenticated user from the Authorization header."""
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("user_id") or payload.get("sub")
    # If sub is username, prefer explicit user_id; otherwise use user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    # If user_id is username (string), try to find by username
    if isinstance(user_id, str):
        user = db.query(User).filter(User.username == user_id).first()
    else:
        user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# IMPORTANT: Use /calculations (plural) not /calculate
router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.get("", response_model=List[CalculationRead])
def browse_calculations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    BROWSE: Get all calculations (GET /calculations)
    """
    calculations = db.query(Calculation).filter(Calculation.user_id == current_user.id).all()
    return calculations


@router.get("/{calculation_id}", response_model=CalculationRead)
def read_calculation(calculation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    READ: Get a single calculation by ID (GET /calculations/{id})
    """
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id, Calculation.user_id == current_user.id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation


@router.post("", response_model=CalculationRead, status_code=200)
def add_calculation(calc: CalculationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    ADD: Create a new calculation (POST /calculations)
    Supports: add, subtract, multiply, divide, power, modulus, sqrt
    """
    # Validate operation type
    valid_types = ["add", "subtract", "multiply", "divide", "power", "modulus", "sqrt"]
    if calc.type.lower() not in valid_types:
        raise HTTPException(
            status_code=422, 
            detail=f"Invalid operation type '{calc.type}'. Must be one of: {valid_types}"
        )
    
    # Perform calculation
    op_type = calc.type.lower()
    
    try:
        if op_type == "add":
            result = calc.a + calc.b
        elif op_type == "subtract":
            result = calc.a - calc.b
        elif op_type == "multiply":
            result = calc.a * calc.b
        elif op_type == "divide":
            if calc.b == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = calc.a / calc.b
        elif op_type == "power":
            result = calc.a ** calc.b
        elif op_type == "modulus":
            if calc.b == 0:
                raise HTTPException(status_code=400, detail="Cannot perform modulus with zero")
            result = calc.a % calc.b
        elif op_type == "sqrt":
            if calc.a < 0:
                raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")
            result = math.sqrt(calc.a)
            # For sqrt, we store 'b' as 0 or as provided
        else:
            raise HTTPException(status_code=422, detail="Invalid operation type")
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Save to database
    new_calc = Calculation(
        a=calc.a,
        b=calc.b,
        type=op_type,
        result=result,
        user_id=current_user.id
    )
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    
    return new_calc


@router.put("/{calculation_id}", response_model=CalculationRead)
def edit_calculation(calculation_id: int, calc: CalculationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    EDIT: Update an existing calculation (PUT /calculations/{id})
    """
    # Find existing calculation
    db_calc = db.query(Calculation).filter(Calculation.id == calculation_id, Calculation.user_id == current_user.id).first()
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    
    # Validate operation type
    valid_types = ["add", "subtract", "multiply", "divide", "power", "modulus", "sqrt"]
    op_type = calc.type.lower()
    
    if op_type not in valid_types:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid operation type '{calc.type}'. Must be one of: {valid_types}"
        )
    
    # Recalculate
    try:
        if op_type == "add":
            result = calc.a + calc.b
        elif op_type == "subtract":
            result = calc.a - calc.b
        elif op_type == "multiply":
            result = calc.a * calc.b
        elif op_type == "divide":
            if calc.b == 0:
                raise HTTPException(status_code=400, detail="Cannot divide by zero")
            result = calc.a / calc.b
        elif op_type == "power":
            result = calc.a ** calc.b
        elif op_type == "modulus":
            if calc.b == 0:
                raise HTTPException(status_code=400, detail="Cannot perform modulus with zero")
            result = calc.a % calc.b
        elif op_type == "sqrt":
            if calc.a < 0:
                raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")
            result = math.sqrt(calc.a)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Update fields
    db_calc.a = calc.a
    db_calc.b = calc.b
    db_calc.type = op_type
    db_calc.result = result
    
    db.commit()
    db.refresh(db_calc)
    
    return db_calc


@router.delete("/{calculation_id}")
def delete_calculation(calculation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    DELETE: Remove a calculation (DELETE /calculations/{id})
    """
    db_calc = db.query(Calculation).filter(Calculation.id == calculation_id, Calculation.user_id == current_user.id).first()
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found or not owned by current user")
    
    db.delete(db_calc)
    db.commit()
    
    return {"message": "Calculation deleted successfully", "id": calculation_id}


@router.get("/stats/summary", response_model=CalculationStatistics)
def get_calculation_statistics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get statistics about user's calculations including totals, operation counts, and averages
    """
    # Get all calculations for the user
    calculations = db.query(Calculation).filter(Calculation.user_id == current_user.id).all()
    
    if not calculations:
        return CalculationStatistics(
            total_calculations=0,
            operation_counts={},
            average_a=0.0,
            average_b=0.0,
            most_used_operation=None
        )
    
    # Calculate statistics
    total = len(calculations)
    operation_counts = {}
    sum_a = 0.0
    sum_b = 0.0
    
    for calc in calculations:
        # Count operations
        op = calc.type
        operation_counts[op] = operation_counts.get(op, 0) + 1
        sum_a += calc.a
        sum_b += calc.b
    
    # Find most used operation
    most_used = max(operation_counts.items(), key=lambda x: x[1])[0] if operation_counts else None
    
    return CalculationStatistics(
        total_calculations=total,
        operation_counts=operation_counts,
        average_a=sum_a / total,
        average_b=sum_b / total,
        most_used_operation=most_used
    )