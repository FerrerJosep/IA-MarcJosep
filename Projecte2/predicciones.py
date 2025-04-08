import cv2
from ultralytics import YOLO
import os
from roboflow import Roboflow

# Configuración de Roboflow
rf = Roboflow(api_key="gYrCTgWXR4d5Wi9dChio")
project = rf.workspace("car-plate-number-detection").project("alphanumeric-character-detection")
version = project.version(1)
dataset = version.download("yolov12")

ruta_base = os.path.dirname(__file__)
ruta_final = os.path.join(ruta_base, "runs/detect/train7/weights/best.pt")
model = YOLO(ruta_final)

ruta_cmax = os.path.join(ruta_base, "test/images")
ruta_detectadas = os.path.join(ruta_base, "test/images_detectadas")

if not os.path.exists(ruta_detectadas):
    os.makedirs(ruta_detectadas)

for filename in os.listdir(ruta_cmax):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_cmax, filename)

        results = model(ruta_imagen)

        image = cv2.imread(ruta_imagen)

        letters = []
        numbers = []

        for result in results:
            for idx, box in enumerate(result.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cropped_img = image[y1:y2, x1:x2]

                gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray, 11, 17, 17)
                thresh = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY_INV, 31, 15
                )

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                thresh = cv2.erode(thresh, kernel, iterations=1)
                thresh = cv2.dilate(thresh, kernel, iterations=1)

                nombre_base = os.path.splitext(filename)[0]
                ruta_preprocesada = os.path.join(ruta_detectadas, f"{nombre_base}_crop{idx}_thresh.png")
                cv2.imwrite(ruta_preprocesada, thresh)

                # Usar el modelo Roboflow para detectar texto en la imagen preprocesada
                predictions = dataset.predict(ruta_preprocesada).json()
                for prediction in predictions['predictions']:
                    ocr_text = prediction['class']
                    if ocr_text.isdigit():
                        numbers.append(ocr_text)
                    elif ocr_text.isalpha():
                        letters.append(ocr_text)

        all_text = ''.join(numbers) + ''.join(letters)
        print(f'Todo el texto detectado en {filename} (letras primero, luego números):\n{all_text}')

        cv2.imwrite(os.path.join(ruta_detectadas, filename), image)
