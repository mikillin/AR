from ultralytics import YOLO
from roboflow import Roboflow
import torch


import os

# Retrieve the API key
api_key = os.getenv("API_KEY")

# Check if the API key is loaded
if api_key:
    print("API key loaded successfully")
else:
    print("API key not found")


rf = Roboflow(api_key=api_key)
project = rf.workspace("prj1-rfizb").project("prj1-z80sa")
version = project.version(1)
dataset = version.download("yolov11")

# Load a pretrained model
model = YOLO("yolo11n.pt")

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Train the model on M1/M2 chip
results = model.train(data=dataset.location + "/data.yaml", epochs=100, imgsz=640, device=device)