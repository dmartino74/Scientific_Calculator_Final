from pydantic import BaseModel, validator, root_validator
from typing import Literal, Optional
from datetime import datetime

# Define allowed operation types
OperationType = Literal["Add", "Sub", "Multiply", "Divide"]

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: OperationType

    @root_validator
    def validate_inputs(cls, values):
        a = values.get("a")
        b = values.get("b")
        op_type = values.get("type")

        if op_type == "Divide" and b == 0:
            raise ValueError("Cannot divide by zero")
        return values

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: OperationType
    result: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
