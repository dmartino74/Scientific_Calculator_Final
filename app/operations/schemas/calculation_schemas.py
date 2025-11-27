from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CalculationCreate(BaseModel):
    """Schema for creating a new calculation"""
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number (optional for unary operations)")
    type: str = Field(..., description="Operation type: add, subtract, multiply, divide, power, modulus, sqrt")
    
    class Config:
        json_schema_extra = {
            "example": {
                "a": 10.0,
                "b": 5.0,
                "type": "add"
            }
        }


class CalculationRead(BaseModel):
    """Schema for reading a calculation from database"""
    id: int
    a: float
    b: float
    type: str
    result: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Backwards compatibility aliases
CalculationRequest = CalculationCreate
CalculationResponse = CalculationRead


class CalculationStatistics(BaseModel):
    """Schema for calculation statistics"""
    total_calculations: int
    operation_counts: dict[str, int]
    average_a: float
    average_b: float
    most_used_operation: str | None = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_calculations": 42,
                "operation_counts": {"add": 15, "multiply": 10, "divide": 8, "subtract": 9},
                "average_a": 25.5,
                "average_b": 12.3,
                "most_used_operation": "add"
            }
        }