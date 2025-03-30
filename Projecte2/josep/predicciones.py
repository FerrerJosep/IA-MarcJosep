import cv2
from ultralytics import YOLO

# Cargar modelo entrenado
model = YOLO("./runs/detect/train7/weights/best.pt")

# Imagen de prueba

image_path = "./test/images/1668451259841_jpg.rf.cbe950aebcf18df81e30b2bfa62ac6cc.jpg"

ruta_cmax= "./test/images/guillem.jpeg"

results = model(ruta_cmax)

# Mostrar resultados
image = cv2.imread(ruta_cmax)
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas del bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Detección de Matrícula", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
