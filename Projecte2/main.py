import cv2
from ultralytics import YOLO
from paddleocr import PaddleOCR
import os
import re
import matplotlib.pyplot as plt
import argparse

ruta_base = os.path.dirname(__file__)
ruta_modelo_yolo = os.path.join(ruta_base, "runs/detect/train7/weights/best.pt")
ruta_resultados = os.path.join(ruta_base, "test/images_detectadas")
os.makedirs(ruta_resultados, exist_ok=True)

model_yolo = YOLO(ruta_modelo_yolo)
ocr = PaddleOCR(use_angle_cls=True, lang='en', det=False)

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

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"No se pudo cargar la imagen: {image_path}")
        return None
    
    orig_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model_yolo(image_path)
    best_plate = None
    highest_conf = 0

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            
            if conf > highest_conf:
                plate_img = image[y1:y2, x1:x2]
                processed_plate = preprocess_plate(plate_img)
                result_ocr = ocr.ocr(processed_plate, cls=True)

                raw_text = ''
                for line in result_ocr:
                    for word_info in line:
                        raw_text += word_info[1][0]

                formatted_text = format_plate_text(raw_text)
                
                if len(formatted_text) >= 6:  # Minimum plate length
                    best_plate = formatted_text
                    highest_conf = conf

    return best_plate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="Path to the image file to process")
    args = parser.parse_args()

    if args.image:
        plate = process_image(args.image)
        if plate:
            print(plate)  
        else:
            print("") 




    # parser = argparse.ArgumentParser()
    # parser.add_argument("--image", help="Path to the image file to process")
    # args = parser.parse_args()

    # if args.image:
    #     plate = process_image(args.image)
    #     if plate:
    #         print(plate)  # This will be captured by the subprocess call
    #     else:
    #         print("")  # Empty string if no plate found
    # else:
    #     # Original batch processing mode
    #     ruta_imagenes_test = os.path.join(ruta_base, "test/images")
    #     for filename in os.listdir(ruta_imagenes_test):
    #         if filename.lower().endswith((".jpg", ".jpeg", ".png")):
    #             ruta_imagen = os.path.join(ruta_imagenes_test, filename)
    #             plate = process_image(ruta_imagen)
    #             if plate:
    #                 print(f"Matrícula detectada en {filename}: {plate}")