from ultralytics import YOLO

# Cargar YOLO
model = YOLO("yolov8n.pt")

# Entrenar con el archivo data.yaml corregido
model.train(data="./datasets/data.yaml", epochs=50, imgsz=640)
