Here is a clear, step-by-step plan to develop this application locally. It's designed to build skills progressively and ensure a successful first experience with FastAPI.

---

### The Plan: A "Learn-by-Doing" Nutrition Calculator

This plan will guide students through creating a dynamic, interactive single-page web application.

**Core Technologies:**
*   **Backend:** Python with FastAPI
*   **Frontend:** Simple HTML with a small amount of JavaScript to make it interactive without page reloads.
*   **Data:** The nutrition `.csv` file from Kaggle.

---

### Phase 1: Project Setup and Backend Basics

**Goal:** To set up the project environment and create a basic backend that can load and serve the nutrition data.

1.  **Project Initialization (Same as Before, but Simpler):**
    *   Create a new GitHub repository named `nutrition_app`.
    *   Clone it to your local Mac.
    *   `cd` into the `nutrition_app` folder.
    *   Create and activate a Python virtual environment (`python3 -m venv venv`, `source venv/bin/activate`).
    *   Create a `.gitignore` file.
    *   Push the initial commit to GitHub.

2.  **Install Necessary Libraries:**
    *   Install FastAPI, Uvicorn, and **Pandas** (for reading the CSV data).
        ```bash
        pip install fastapi "uvicorn[standard]" pandas
        ```

3.  **Prepare the Data:**
    *   Download the `nutrition.csv` file from the Kaggle link.
    *   Create a `data` folder inside your project.
    *   Place the `nutrition.csv` file inside the `data` folder.

4.  **Create the Core Backend File (`main.py`):**
    *   Create a `main.py` file.
    *   Inside `main.py`, write the code to:
        *   Import `pandas` and `FastAPI`.
        *   Load the `nutrition.csv` into a pandas DataFrame when the application starts.
        *   Create a simple API endpoint (e.g., `/api/foods`) that returns the list of all food names as a JSON array. This will be used to populate our dropdown menu.

5.  **First Checkpoint:**
    *   Run the server: `uvicorn nutrition_app.main:app --reload` (from the parent directory).
    *   Go to `http://127.0.0.1:8000/api/foods` in your browser.
    *   You should see a JSON list of all the food names (["Cornstarch", "Noodles, Japanese, soba, dry", ...]). This confirms the backend can read and serve the data.

### Phase 2: Building the Basic User Interface

**Goal:** To create a static webpage with a dropdown menu and an input field, but with no calculation logic yet.

1.  **Install Jinja2 for HTML Templating:**
    ```bash
    pip install jinja2
    ```

2.  **Create the Frontend Structure:**
    *   Create a `templates` folder.
    *   Create an `index.html` file inside `templates`.

3.  **Update `main.py` to Serve the HTML Page:**
    *   Add the necessary Jinja2 configuration to `main.py`.
    *   Create a main endpoint (`@app.get("/")`) that renders and returns `index.html`. This endpoint should also pass the list of food names (from the DataFrame) to the template.

4.  **Build `index.html`:**
    *   Create the basic HTML structure with a title.
    *   Create a `<form>` element.
    *   Inside the form, create a `<select>` dropdown menu. Use a Jinja2 `for` loop to dynamically populate the `<option>` elements with the list of food names passed from the backend.
    *   Add an `<input type="number">` for the user to enter the weight in grams.
    *   Add a "Calculate" button.

5.  **Second Checkpoint:**
    *   Run the server.
    *   Go to `http://127.0.0.1:8000/` in your browser.
    *   You should see your webpage with a fully populated dropdown menu of all the foods and an input box for the weight.

### Phase 3: Implementing the Calculation Logic

**Goal:** To make the application perform the nutrition calculation when the user clicks the button.

1.  **Create a Calculation Endpoint in `main.py`:**
    *   Create a new **`POST`** endpoint (e.g., `/api/calculate`).
    *   This endpoint will accept a JSON payload containing the `food_name` and `weight`.
    *   **Logic:** Inside this endpoint, use the pandas DataFrame to:
        *   Find the row corresponding to the `food_name`.
        *   Get the nutrition values (which are per 100g).
        *   Calculate the actual nutrition for the given `weight` (e.g., `(value / 100) * weight`).
        *   Return the calculated nutrition data as a JSON object.

2.  **Add JavaScript to `index.html`:**
    *   Add a `<script>` tag to your HTML file.
    *   Write JavaScript code that:
        *   Listens for the "submit" event on the form.
        *   Prevents the default form submission (which reloads the page).
        *   Gets the selected `food_name` and the entered `weight` from the form fields.
        *   Uses the `fetch()` API to send this data to your `/api/calculate` endpoint.
        *   When it receives the JSON response from the backend, it dynamically displays the results on the page (e.g., by creating and populating a `<div>` or a `<table>`).

3.  **Third Checkpoint:**
    *   Run the server.
    *   Go to the home page, select a food, enter a weight, and click "Calculate".
    *   You should see the calculated nutrition information appear on the page without a full page reload.

### Phase 4: Adding "Shopping List" Functionality

**Goal:** To allow the user to add multiple foods and see a running total, as well as edit or delete items.

1.  **Backend Changes (State Management):**
    *   The backend will remain mostly **stateless**. It doesn't need to remember the user's list. All state will be managed on the frontend.
    *   We don't need any new endpoints for this phase. The existing `/api/calculate` endpoint is sufficient.

2.  **Major Frontend Changes (JavaScript):**
    *   In your JavaScript code, create an array to act as the "shopping list" (e.g., `let foodList = []`).
    *   When the user adds a food, instead of just displaying the result, create an object containing the name, weight, and calculated nutrition, and push it into the `foodList` array.
    *   Create a `renderList()` function in JavaScript. This function will:
        *   Loop through the `foodList` array.
        *   Dynamically generate HTML for each item in the list (e.g., as list items `<li>` or table rows `<tr>`).
        *   Each item's HTML should include a "Delete" button and an editable weight input.
        *   Calculate and display the **total nutrition** by summing up the values from all items in the array.
    *   **Add Event Handlers:**
        *   Attach event listeners to the "Delete" buttons. When clicked, they should remove the corresponding item from the `foodList` array and then call `renderList()` again to update the UI.
        *   Attach event listeners to the editable weight inputs. When changed, they should update the weight in the corresponding object in the `foodList` array, re-calculate its nutrition (you might not even need a new API call for this, you can do the math client-side!), and then call `renderList()` to update everything.

4.  **Final Checkpoint:**
    *   You can now add multiple foods to your list.
    *   The UI updates to show each item and the running total.
    *   You can delete an item from the list, and the totals update.
    *   You can change the weight of an item, and the totals update.

This plan creates a much more manageable learning curve and results in a fun, interactive, and genuinely useful application.