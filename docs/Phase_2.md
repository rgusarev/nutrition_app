Here is the detailed, step-by-step guide for Phase 2, complete with all the necessary code.

This phase focuses on creating the user interface. We will build a basic HTML page and use FastAPI's templating engine to populate a dropdown menu with the food names we prepared in our Phase 1 API.

---

# Nutrition App - Phase 2: Building the Basic User Interface

**Goal:** To create a user-facing webpage served by our FastAPI application. This page will display a dropdown menu dynamically populated with all the food names from our dataset, an input for weight, and a button.

---

### Step 1: Install Jinja2 Templating Engine

`[LOCAL MAC]`

FastAPI uses Jinja2 to render HTML templates. Let's install it.

1.  **Activate your virtual environment** if it's not already active.
    ```bash
    # Navigate into your project folder if you aren't already
    cd nutrition_app
    source venv/bin/activate
    ```

2.  **Install Jinja2:**
    ```bash
    pip install jinja2
    ```

### Step 2: Create the Frontend Structure

`[LOCAL MAC]`

We need a place to store our HTML files.

1.  **Create a `templates` folder** in the root of your `nutrition_app` project.
    ```bash
    mkdir templates
    ```

2.  **Create an `index.html` file** inside this new `templates` folder.
    ```bash
    touch templates/index.html
    ```

### Step 3: Update `main.py` to Serve HTML

`[LOCAL MAC]`

Now we need to configure FastAPI to know about our templates and create an endpoint to serve our `index.html` page.

1.  **Open `main.py` in VS Code.**

2.  **Add the necessary imports and configuration** at the top of the file. We will use `pathlib` again to make sure the path to our templates is always correct.

    ```python
    # main.py
    import pandas as pd
    from fastapi import FastAPI, Request # <--- Add Request
    from fastapi.exceptions import HTTPException
    from fastapi.responses import HTMLResponse # <--- Add HTMLResponse
    from fastapi.templating import Jinja2Templates # <--- Add Jinja2Templates
    from pathlib import Path

    # --- Application Setup ---

    app = FastAPI(
        title="Nutrition API",
        description="An API for getting nutrition information about food.",
        version="1.0.0",
    )

    # --- Path and Template Configuration ---
    BASE_DIR = Path(__file__).resolve().parent
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates")) # <--- Configure Jinja2

    # --- Data Loading ---
    # (This section remains unchanged)
    try:
        DATA_PATH = BASE_DIR / "data" / "nutrition.csv"
        df = pd.read_csv(DATA_PATH)
        food_names = df['Food Name'].tolist() # Use the correct column name
        print("Data loaded successfully.")
    except FileNotFoundError:
        # (Error handling remains unchanged)
        # ...
        food_names = []

    # --- API Endpoints ---
    # (The /api/foods endpoint remains unchanged)
    @app.get("/api/foods", tags=["Foods"])
    # ...

    # --- Frontend UI Endpoint ---

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
    ```

    **Key Changes:**
    *   We added imports for `Request`, `HTMLResponse`, and `Jinja2Templates`.
    *   We configured `Jinja2Templates` using our `BASE_DIR` absolute path.
    *   We created a new endpoint for the root URL (`/`). This function uses `TemplateResponse` to render `index.html`.
    *   Crucially, we pass a context dictionary `{"request": request, "food_names": food_names}` to the template. This makes our Python list `food_names` available inside the HTML file.

### Step 4: Build the `index.html` Page

`[LOCAL MAC]`

Now we will write the HTML and use Jinja2's templating syntax to build our form.

1.  **Open `templates/index.html` in VS Code.**

2.  **Add the following code:**

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nutrition Calculator</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                margin: 0;
                padding: 2rem;
                background-color: #f4f4f9;
                color: #333;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
                color: #4a4a4a;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            label {
                font-weight: bold;
            }
    
            /* Making the dropdown searchable requires a library, but we can make it look good */
            select, input, button {
                padding: 0.75rem;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 1rem;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                cursor: pointer;
                transition: background-color 0.2s;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Nutrition Calculator</h1>
            <form id="nutrition-form">
                <div>
                    <label for="food-select">Select a Food:</label>
                    <select name="food" id="food-select" required>
                        <option value="">-- Please choose a food --</option>
                        
                        <!-- This is the Jinja2 Templating Part -->
                        {% for name in food_names %}
                            <option value="{{ name }}">{{ name }}</option>
                        {% endfor %}
                        
                    </select>
                </div>
                <div>
                    <label for="weight-input">Weight (in grams):</label>
                    <input type="number" id="weight-input" name="weight" min="1" required>
                </div>
                
                <button type="submit">Add Food</button>
            </form>
        </div>
    </body>
    </html>
    ```

    **How the Jinja2 Part Works:**
    *   `{% for name in food_names %}`: This starts a loop. `food_names` is the list we passed from `main.py`.
    *   `<option value="{{ name }}">{{ name }}</option>`: Inside the loop, this line is repeated for every food name. `{{ name }}` is the syntax to print the value of the `name` variable.
    *   `{% endfor %}`: This ends the loop.

### Step 5: Run and Test the Application

`[LOCAL MAC]`

1.  **Run the Uvicorn Server** from the parent directory of your project.
    ```bash
    uvicorn nutrition_app.main:app --reload
    ```

2.  **Test the Webpage:**
    *   Open your web browser and navigate to: **http://127.0.0.1:8000/**
    *   **Expected Result:** You should see a styled webpage with the title "Nutrition Calculator". The main feature is a dropdown menu. When you click it, you should see the full list of all food names, starting with "Cornstarch". You will also see an input box for weight and an "Add Food" button.
    *   The button won't do anything yet—we'll add that functionality in Phase 3.

### Step 6: Commit Your Progress

`[LOCAL MAC]`

1.  Stop the server (`Ctrl + C`).
2.  Commit and push your work:
    ```bash
    git add .
    git commit -m "Phase 2: Build basic UI with dynamic food dropdown"
    git push origin main
    ```

---

### Phase 2 Complete

You have successfully:
*   Configured FastAPI to serve HTML pages using the Jinja2 templating engine.
*   Created a clean, user-friendly frontend interface.
*   Passed data (the list of food names) from your Python backend to your HTML frontend to dynamically generate content.

Your application now has a visible front door, ready for you to wire up the calculation logic in Phase 3.