#look99102@gmail.com
import daft
from google.cloud import vision

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# -----------------------------
# Step 1: Google Vision setup
# -----------------------------
vision_client = vision.ImageAnnotatorClient()
IGNORED_LABELS = {
    "food", "ingredient", "tableware", "food storage",
    "food preservation", "pickling", "produce", "vegetable",
    "food storage containers"
}

image_paths = ["cut down.jpg", "other cut.jpg"]
detected_foods_list = []

# Example fridge temperature (°F)
fridge_temp = 40

# Detect foods
for path in image_paths:
    with open(path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    food_labels = [
        label.description
        for label in labels
        if label.description.lower() not in IGNORED_LABELS
    ]
    detected_foods_list.append(food_labels)

# -----------------------------
# Step 2: Filter relevant labels & assign min safe temp
# -----------------------------
def min_safe_temp(food):
    """Returns minimum safe storage temperature in °F"""
    if food == "Cucumber":
        return 45
    elif food == "Leaf vegetable":
        return 32
    else:
        return None

def check_alert(food, temperature):
    """Returns True if temperature is below min safe temp"""
    return temperature < min_safe_temp(food)

filtered_image_paths = []
filtered_foods = []
min_temp_list = []
alert_list = []

for path, foods in zip(image_paths, detected_foods_list):
    relevant_foods = [f for f in foods if f in ["Cucumber", "Leaf vegetable"]]
    if relevant_foods:
        filtered_image_paths.append(path)
        filtered_foods.append(relevant_foods)
        temps = [min_safe_temp(f) for f in relevant_foods]
        min_temp_list.append(temps)
        alerts = [check_alert(f, fridge_temp) for f in relevant_foods]
        alert_list.append(alerts)

# -----------------------------
# Step 3: Create Daft DataFrame
# -----------------------------
alert_column_name = f"alert if the fridge temp is {fridge_temp}°F"
df = daft.from_pydict({
    "image name": filtered_image_paths,
    "detected foods": filtered_foods,
    "unsafe if temp beneath": min_temp_list,
    alert_column_name: alert_list
})

results = df.collect()
print(results)

flat_temps = [temp for sublist in min_temp_list for temp in sublist]
print(f"Recommended alert threshold: {max(flat_temps)}°F")