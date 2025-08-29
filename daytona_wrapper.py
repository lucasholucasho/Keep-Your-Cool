from daytona import Daytona, DaytonaConfig

# -----------------------------
# 1. Initialize Daytona
# -----------------------------
config = DaytonaConfig(api_key="dtn_4a440368d8e67bf85cee72c23873fc32f4f26cff50c572f43df864075fa66339")
daytona = Daytona(config)
sandbox = daytona.create()

# -----------------------------
# 2. Upload files into sandbox
# -----------------------------
with open("food-recognizer-470408-759e0949b168.json", "rb") as f:
    content = f.read()
sandbox.fs.upload_file(content, "service_account.json")

with open("cut down.jpg", "rb") as f:
    content = f.read()
sandbox.fs.upload_file(content, "cut down.jpg")

with open("other cut.jpg", "rb") as f:
    content = f.read()
sandbox.fs.upload_file(content, "other cut.jpg")

with open("food_pipeline.py", "rb") as f:
    content = f.read()
sandbox.fs.upload_file(content, "food_pipeline.py")

# -----------------------------
# 3. Run your pipeline as a file
# -----------------------------
sandbox.process.exec("pip install daft")
sandbox.process.exec("pip install google-cloud-vision")
response = sandbox.process.exec("python food_pipeline.py")

print(response.result)

# -----------------------------
# 4. Clean up sandbox
# -----------------------------
sandbox.delete()