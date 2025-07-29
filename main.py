# main.py
import pandas as pd
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pathlib import Path

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

    # Load the data using the absolute path
    df = pd.read_csv(DATA_PATH, delimiter=";")

    # We only need the first column for the food names list
    food_names = df.iloc[:, 1].tolist()
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