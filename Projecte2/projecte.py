#py -3.12 projecte.py
#py -3.12 -m pip install roboflow

# import os
# from roboflow import Roboflow
from ultralytics import YOLO

# DATASET_DIR = "Projecte2/Matriculas-Españolas-1"
# if not os.path.exists(DATASET_DIR):
#     rf = Roboflow(api_key="gYrCTgWXR4d5Wi9dChio")
#     project = rf.workspace("vc").project("matriculas-espanolas")
#     version = project.version(1)
#     dataset = version.download("yolov12")
#     print("Dataset descargado.")
# else:
#     print(f"La carpeta '{DATASET_DIR}' ya existe. No se descarga nuevamente.")

model = YOLO("yolo12n.pt")
results = model.train(data="Matriculas-Españolas-1/data.yaml", epochs=100, imgsz=640)
results = model("path/to/bus.jpg")