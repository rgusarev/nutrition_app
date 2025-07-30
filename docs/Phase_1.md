Here is the detailed, step-by-step guide for Phase 1 with all the necessary code. This will get you to a solid first checkpoint where the backend is successfully serving data.

---

# Nutrition App - Phase 1: Project Setup and Backend Basics

**Goal:** To set up a complete project environment and create a basic FastAPI backend that can load nutrition data from a CSV file and serve the list of food names via an API endpoint.

---

### Step 1: Project Initialization

`[LOCAL MAC]`

This step ensures your project is set up correctly with version control and an isolated environment.

1.  **Create GitHub Repository:**
    *   Go to GitHub and create a **new, empty repository** named `nutrition_app`.

2.  **Clone and Set Up Locally:**
    *   In your terminal, navigate to your projects folder (e.g., `cd ~/Projects`).
    *   Clone the repository: `git clone git@github.com:your-username/nutrition_app.git`
    *   Navigate into the new folder: `cd nutrition_app`

3.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(You should see `(venv)` in your terminal prompt).*

4.  **Create `.gitignore` file:**
    *   `touch .gitignore`
    *   Open the file and add the following content to ignore common unnecessary files:
        ```text
        venv/
        __pycache__/
        .DS_Store
        data/
        ```
        *(Note: We are ignoring the `data/` folder because CSV files can sometimes be large and don't always belong in a Git repository. For this small file, it's okay, but this is good practice).*

### Step 2: Install Libraries and Prepare Data

`[LOCAL MAC]`

1.  **Install necessary Python libraries:**
    ```bash
    pip install fastapi "uvicorn[standard]" pandas
    ```

2.  **Prepare the Data:**
    *   Create a `data` folder inside your `nutrition_app` project folder:
        ```bash
        mkdir data
        ```
    *   Download the `nutrition.csv` file from the [Kaggle dataset page](https://www.kaggle.com/datasets/gokulprasantht/nutrition-dataset).
    *   Move the downloaded `nutrition.csv` file into the `data` folder you just created.

### Step 3: Create the Core Backend (`main.py`)

`[LOCAL MAC]`

This is the heart of our application. We will create a single file to handle loading the data and serving our first API endpoint.

1.  **Create the `main.py` file** in the root of your `nutrition_app` folder.
    ```bash
    touch main.py
    ```

2.  **Add the following code to `main.py`:**

    ```python
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

    ```

### Step 4: Run and Test the Backend

`[LOCAL MAC]`

This is the first checkpoint to ensure everything is working as expected.

1.  **Run the Uvicorn Server:**
    *   In your terminal, make sure you are in the directory that **contains** your `nutrition_app` folder (the parent directory).
    *   Run the server:
        ```bash
        uvicorn nutrition_app.main:app --reload
        ```

2.  **Analyze the Server Startup Log:**
    *   You should see lines indicating the server is running, like:
        ```
        INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
        INFO:     Started reloader process [xxxxx]
        INFO:     Started server process [xxxxx]
        INFO:     Waiting for application startup.
        Data loaded successfully.
        INFO:     Application startup complete.
        ```
    *   The `Data loaded successfully.` message confirms that your backend found and read the CSV file.

3.  **Test the API Endpoint:**
    *   Open your web browser and navigate to: **http://127.0.0.1:8000/api/foods**
    *   **Expected Result:** You should see a JSON object containing a single key, "foods", whose value is a long array of all the food names from the CSV file. It will look like this:
        ```json
        {
          "foods": [
            "Cornstarch",
            "Noodles, Japanese, soba, dry",
            "Noodles, Japanese, soba, cooked",
            "Noodles, Chinese, cellophane or long rice (mung beans), dry",
            "Other",
            ...
          ]
        }
        ```

4.  **Test the Interactive Docs:**
    *   Also check out the automatic documentation by navigating to: **http://127.0.0.1:8000/docs**
    *   You will see your `/api/foods` endpoint listed there. You can expand it and click "Try it out" -> "Execute" to get the same result.

### Step 5: Commit Your Progress

`[LOCAL MAC]`

You've successfully completed the first major part of the project. Let's save this progress to Git.

1.  In your terminal, stop the server (`Ctrl + C`).
2.  Navigate into your project folder (`cd nutrition_app`).
3.  Commit and push your work:
    ```bash
    git add .
    git commit -m "Phase 1: Initial setup and API endpoint for food list"
    git push origin main
    ```

---

### Phase 1 Complete

You have now successfully:
*   Set up a clean project structure.
*   Installed the necessary libraries.
*   Created a FastAPI backend that loads data from a CSV file on startup.
*   Exposed that data through a testable JSON API endpoint.

Your backend is now ready and waiting for a frontend to consume its data, which is the goal of Phase 2.