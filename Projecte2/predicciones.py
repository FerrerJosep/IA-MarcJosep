import cv2
from ultralytics import YOLO
import easyocr
import os

ruta_base = os.path.dirname(__file__)
ruta_final = os.path.join(ruta_base, "runs/detect/train7/weights/best.pt")
model = YOLO(ruta_final)

ruta_cmax = os.path.join(ruta_base, "test/images")
ruta_detectadas = os.path.join(ruta_base, "test/images_detectadas")

if not os.path.exists(ruta_detectadas):
    os.makedirs(ruta_detectadas)

reader = easyocr.Reader(['en', 'es'])

for filename in os.listdir(ruta_cmax):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_cmax, filename)

        results = model(ruta_imagen)

        image = cv2.imread(ruta_imagen)

        letters = []
        numbers = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cropped_img = image[y1:y2, x1:x2]

                gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                ocr_results = reader.readtext(thresh)
                for result in ocr_results:
                    ocr_text = result[1]
                    if ocr_text.isdigit():
                        numbers.append(ocr_text)
                    elif ocr_text.isalpha():
                        letters.append(ocr_text)

        all_text = ''.join(numbers) + ''.join(letters)
        print(f'Todo el texto detectado en {filename} (letras primero, luego números):\n{all_text}')

        cv2.imwrite(os.path.join(ruta_detectadas, filename), image)
