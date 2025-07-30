Phase 3.

This version incorporates all the lessons learned from our previous attempts, including:
*   Fixing the `KeyError: 'Name'` by using the correct column name.
*   Fixing the `ValueError` by handling missing data (`NaN`) with `.fillna(0)`.
*   Using a Pydantic `response_model` to ensure the API response is predictable and valid.
*   Correcting the JavaScript to match the new, smaller response from the API.

This guide should provide a smooth, error-free path to completing the interactive part of your application.

---

# Nutrition App - Phase 3 (Final Corrected Version): Implementing Calculation Logic

**Goal:** To make the application interactive by creating a robust backend endpoint that cleans and calculates nutrition data, and then using frontend JavaScript to call this endpoint and display the results dynamically.

**Prerequisites:**
*   You have completed Phase 2. Your application serves a webpage with a populated food dropdown.
*   You are on your local machine with the virtual environment activated.

---

### Step 1: Create a Pydantic Schema for the API Response

`[LOCAL MAC]`

Before building the backend logic, we must first define the exact "shape" of the data we want our API to return. This is a best practice that prevents validation errors later.

1.  **Open `schemas.py` in VS Code.**
2.  **Add a new `NutritionResult` class.** This model will represent the final, calculated data we send to the frontend.

    ```python
    # schemas.py
    from pydantic import BaseModel

    # --- ADD THIS NEW SCHEMA ---
    class NutritionResult(BaseModel):
        # Pydantic field names must be valid Python variable names.
        # No spaces, parentheses, or hyphens.
        ID: int
        Name: str
        Weight_g: float  # We use an underscore instead of parentheses
        Calories: float
        Protein_g: float
        Fat_g: float
        Carbohydrates_g: float
    ```
    *(Note: We are selecting a few key nutrients for this example. You can add as many as you like, as long as the field name is a valid Python variable name and matches the data you will return from the backend).*

### Step 2: Create the Backend Calculation Endpoint

`[LOCAL MAC]`

Now we will build the API endpoint. It will use our new `NutritionResult` schema as a contract for its response.

1.  **Open `main.py` in VS Code.**
2.  **Define the data model for the request.** Add the `FoodRequest` class at the top of the file if it's not already there.
    ```python
    # main.py
    from pydantic import BaseModel
    # ... other imports ...

    class FoodRequest(BaseModel):
        food_name: str
        weight: float
    ```
3.  **Add the new `/api/calculate` endpoint** to `main.py`. This version is corrected to use proper column names, handle missing data, and return a dictionary that matches our new `NutritionResult` schema.

    ```python
    # main.py
    # Make sure 'schemas' is imported correctly at the top of the file:
    # from . import schemas

    # ... (add this after your /api/foods endpoint) ...

    @app.post("/api/calculate", response_model=schemas.NutritionResult, tags=["Calculation"])
    def calculate_nutrition(request: FoodRequest):
        """
        Calculates key nutritional content for a given food and weight.
        """
        food_name = request.food_name
        weight = request.weight

        # Find the row in the DataFrame using the correct column name 'Name'
        food_data = df[df['Name'] == food_name]

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


        # FastAPI will automatically validate this dictionary against NutritionResult
        return result_data
    ```

### Step 3: Test the New Endpoint with the Docs

`[LOCAL MAC]`

Always verify your backend logic before touching the frontend.

1.  **Run the Uvicorn Server** from the parent directory: `uvicorn nutrition_app.main:app --reload`
2.  **Open the interactive docs:** **http://127.0.0.1:8000/docs**
3.  Find and expand the `POST /api/calculate` endpoint.
4.  **Test it:**
    *   Click **"Try it out"**.
    *   Edit the "Request body": `{ "food_name": "Cornstarch", "weight": 200 }`
    *   Click **"Execute"**.
5.  **Analyze the Response:**
    *   **Expected Result:** You should get a `200` success response. The response body will be a clean JSON object with exactly the fields defined in `NutritionResult` (e.g., `"Protein_g": 0.52`). There should be no `NaN` values or validation errors.

### Step 4: Update JavaScript to Handle the New Response

`[LOCAL MAC]`

Now we will write the JavaScript to connect our HTML form to our new backend endpoint and display the clean data.

1.  **Open `templates/index.html` in VS Code.**
2.  Add a placeholder `div` for our results, right below the `<form>` tag.
    ```html
    <!-- Add this line right after the </form> tag -->
    <div id="results-container">
        <!-- Calculation results will be displayed here -->
    </div>
    ```
3.  **Put `<script>` section** at the bottom of the file with this corrected version.

    ```javascript
        <script>
            const form = document.getElementById('nutrition-form');
            const resultsContainer = document.getElementById('results-container');

            form.addEventListener('submit', async function(event) {
                // Prevent the default browser behavior of reloading the page
                event.preventDefault();

                resultsContainer.innerHTML = '<p>Calculating...</p>';

                const foodName = document.getElementById('food-select').value;
                const weight = parseFloat(document.getElementById('weight-input').value);

                // Basic frontend validation
                if (!foodName || !weight || weight <= 0) {
                    resultsContainer.innerHTML = '<p style="color: red;">Please select a food and enter a valid weight.</p>';
                    return;
                }

                // --- Make the API Call to our Backend ---
                try {
                    const response = await fetch('/api/calculate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ food_name: foodName, weight: weight })
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'An unknown error occurred.');
                    }

                    const nutritionData = await response.json();
                    displayResults(nutritionData);

                } catch (error) {
                    resultsContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                }
            });

            function displayResults(data) {
                // This function now expects the clean data from our NutritionResult schema
                let html = `<h2>Nutrition for ${data.Name} (${data.Weight_g}g)</h2>`;
                html += '<table border="1" style="width:100%; border-collapse: collapse; margin-top: 1rem;">';
                html += '<thead><tr><th>Nutrient</th><th>Amount</th></tr></thead>';
                html += '<tbody>';

                // We explicitly display the fields we know exist in our response model
                html += `<tr><td>Calories</td><td>${data.Calories}</td></tr>`;
                html += `<tr><td>Protein (g)</td><td>${data.Protein_g}</td></tr>`;
                html += `<tr><td>Fat (g)</td><td>${data.Fat_g}</td></tr>`;
                html += `<tr><td>Carbohydrates (g)</td><td>${data.Carbohydrates_g}</td></tr>`;
                
                html += '</tbody></table>';
                resultsContainer.innerHTML = html;
            }
        </script>
    ```

### Step 5: Final Test of the Interactive UI

`[LOCAL MAC]`

1.  Make sure your `uvicorn` server is running.
2.  Go to **http://127.0.0.1:8000/** in your browser and do a hard refresh (Cmd+Shift+R) to ensure you have the latest JavaScript.
3.  **Test the full flow:**
    *   Select a food (e.g., "Cornstarch").
    *   Enter a weight (e.g., `200`).
    *   Click the button.
    *   **Expected Result:** A clean, 4-row table should appear showing the calculated values for Calories, Protein, Fat, and Carbohydrates for 200g of cornstarch.

### Step 6: Commit Your Progress

`[LOCAL MAC]`

1.  Stop the server (`Ctrl + C`).
2.  Commit and push your work:
    ```bash
    git add .
    git commit -m "Phase 3: Implement robust calculation endpoint and UI"
    git push origin main
    ```

---

### Phase 3 Complete

You have successfully debugged and implemented the core functionality of your application. You now have a robust system that cleans data, performs calculations, and displays the results interactively. You are now ready to build on this foundation in Phase 4.