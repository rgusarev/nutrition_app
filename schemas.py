# schemas.py
from pydantic import BaseModel

# --- ADD THIS NEW SCHEMA ---
class NutritionResult(BaseModel):
    # Pydantic field names must be valid Python variable names.
    # No spaces, parentheses, or hyphens.
    ID: int
    Name: str
    Weight: float  # We use an underscore instead of parentheses
    Calories: float
    Iron: float