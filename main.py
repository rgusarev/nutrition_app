# main.py
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import BaseModel
from . import schemas

# --- Data Models for API ---
class FoodRequest(BaseModel):
    food_name: str
    weight: float


# --- Application Setup ---

# Create the FastAPI app instance
app = FastAPI(
    title="Nutrition API",
    description="An API for getting nutrition information about food.",
    version="1.0.0",
)

# --- Data Loading ---

# Load the nutrition data from the CSV file into a pandas DataFrame.
# This happens once when the application starts up.
try:
    print(f"Start loading nutrition database...")
    # Get the directory of the current file (main.py)
    BASE_DIR = Path(__file__).resolve().parent 
    # Define the path to the CSV file
    DATA_PATH = BASE_DIR / "data" / "nutrition.csv"

    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

    # Load the data using the absolute path
    df = pd.read_csv(DATA_PATH, delimiter=";")

    # We only need the first column for the food names list
    # print(df.columns)
    food_names = df['name'].tolist()
    print("Data loaded successfully.")
except FileNotFoundError:
    print("ERROR: data/nutrition.csv not found. Please make sure the file exists.")
    # In a real app, you might want to exit or handle this more gracefully.
    df = pd.DataFrame() # Create an empty DataFrame to avoid further errors
    food_names = []


# --- API Endpoints ---

@app.get("/api/foods", tags=["Foods"])
def get_food_names():
    """
    Returns a list of all available food names from the dataset.
    This is useful for populating a dropdown menu on the frontend.
    """
    if not food_names:
        raise HTTPException(status_code=404, detail="Food list not available. Check server data.")
    
    return {"foods": food_names}

@app.post("/api/calculate", response_model=schemas.NutritionResult, tags=["Calculation"])
def calculate_nutrition(request: FoodRequest):
    """
    Calculates key nutritional content for a given food and weight.
    """
    food_name = request.food_name
    weight = request.weight

    # Find the row in the DataFrame using the correct column name 'Name'
    food_data = df[df['name'] == food_name]

    if food_data.empty:
        raise HTTPException(status_code=404, detail=f"Food '{food_name}' not found.")

    # Select the first row and immediately fill any missing values with 0
    nutrition_per_100g = food_data.iloc[0].fillna(0)
    
    multiplier = weight / 100.0

    # --- Build the dictionary to match the NutritionResult schema ---

    # Patch for the "iron" colunms explicitly to convert to milligrams
    iron_data = float(nutrition_per_100g.get("iron", 0).split()[0])
    
    # Using .get(key, 0) is a safe way to access data that might be missing
    result_data = {
        "ID": int(nutrition_per_100g.get("ID", 0)),
        "Name": nutrition_per_100g.get("name", "Unknown"),
        "Weight": weight,
        "Calories": round(nutrition_per_100g.get("calories", 0) * multiplier, 2),
        "Iron": round(iron_data * 1e-3 * multiplier, 6)
    }

    # FastAPI will automatically validate this dictionary against NutritionResult (see schema.py)
    return result_data

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def serve_home_page(request: Request):
    """
    Serves the main HTML page of the application.
    It passes the list of food names to the template to populate the dropdown.
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "food_names": food_names}
    )