import cv2
from ultralytics import YOLO
import easyocr
import os
import re
import matplotlib.pyplot as plt

ruta_base = os.path.dirname(__file__)
ruta_modelo_yolo = os.path.join(ruta_base, "runs/detect/train7/weights/best.pt")
ruta_imagenes_test = os.path.join(ruta_base, "test/images")
ruta_resultados = os.path.join(ruta_base, "test/images_detectadas")
os.makedirs(ruta_resultados, exist_ok=True)

model_yolo = YOLO(ruta_modelo_yolo)
reader = easyocr.Reader(['en'])

def preprocess_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    return gray

def format_plate_text(text):
    clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
    numbers = re.sub(r'[^0-9]', '', clean_text)
    letters = re.sub(r'[^A-Z]', '', clean_text)
    if len(numbers) >= 4 and len(letters) >= 3:
        return f"{numbers[:4]}{letters[:3]}"
    return clean_text

for filename in os.listdir(ruta_imagenes_test):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        ruta_imagen = os.path.join(ruta_imagenes_test, filename)
        image = cv2.imread(ruta_imagen)
        orig_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = model_yolo(ruta_imagen)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                class_name = model_yolo.names[cls_id] if model_yolo.names and cls_id < len(model_yolo.names) else f"cls_{cls_id}"
                color = (0, 255, 0)
                thickness = 2
                cv2.rectangle(orig_img, (x1, y1), (x2, y2), color, thickness)
                label = f"{class_name} {conf:.2f}"
                (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(orig_img, (x1, y1 - th - baseline), (x1 + tw, y1), color, -1)
                cv2.putText(orig_img, label, (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                plate_img = image[y1:y2, x1:x2]
                processed_plate = preprocess_plate(plate_img)
                ocr_results = reader.readtext(
                    processed_plate,
                    detail=0,
                    paragraph=True,
                    allowlist='0123456789BCDFGHJKLMNPQRSTVWXYZ',
                    batch_size=1,
                    width_ths=2.0
                )
                raw_text = "".join(ocr_results).upper()
                formatted_text = format_plate_text(raw_text)
                print(f"\nArchivo: {filename}")
                print(f"Texto crudo: {raw_text}")
                print(f"Texto formateado: {formatted_text}")
                print(f"Coordenadas: ({x1}, {y1}) - ({x2}, {y2})")
                print(f"Confianza: {conf:.2f}")
                text_label = f"Plate: {formatted_text}"
                cv2.putText(orig_img, text_label, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        output_path = os.path.join(ruta_resultados, f"result_{filename}")
        cv2.imwrite(output_path, cv2.cvtColor(orig_img, cv2.COLOR_RGB2BGR))
        plt.figure(figsize=(16, 9))
        plt.imshow(orig_img)
        plt.axis('off')
        plt.title(f"Resultados para {filename}")
        plt.show()