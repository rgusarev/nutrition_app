import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "nutrition.csv"


# Load the data using the absolute path
df = pd.read_csv(DATA_PATH, delimiter=";")

food_data = df[df['name'] == 'Cornstarch']
weight = 150
nutrition_per_100g = food_data.iloc[0].fillna(0)
multiplier = weight / 100.0

calculated_nutrition = {
    "ID": nutrition_per_100g["ID"],
    "Name": nutrition_per_100g["name"],
    "Weight (g)": weight
}

nutr_colunms = ['calories', 'iron']
# Loop through dedicated columns in the original data

for col_name in nutr_colunms:
    # Get the value, calculate, and add to our result dictionary
    original_value = nutrition_per_100g[col_name]
    # Just a patch for a mg suffux in iron amount
    if isinstance(original_value, str) and 'mg' in original_value:
        original_value = float(original_value.split()[0]) * 1e-3
    calculated_value = round(original_value * multiplier, 6)
    calculated_nutrition[col_name] = calculated_value

print(calculated_nutrition)
print(df[['name', 'calories', 'iron']])
# print(df[[
#     'name',
#     'calories',
#     'protein',
#     'iron']
#     ])
# print(df.iloc[0][[
#     'name',
#     'calories',
#     'protein']
#     ])
# print(df.columns.tolist())