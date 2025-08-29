#look99102@gmail.com
from google.cloud import vision

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
print(detected_foods_list)