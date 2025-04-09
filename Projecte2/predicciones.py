import cv2
from ultralytics import YOLO
import torch
import os
import numpy as np
from modelo import OCRModel

# Rutas y modelo YOLO
ruta_base = os.path.dirname(__file__)
ruta_final = os.path.join(ruta_base, "runs/detect/train7/weights/best.pt")
model_yolo = YOLO(ruta_final)

ruta_cmax = os.path.join(ruta_base, "test/images")
ruta_detectadas = os.path.join(ruta_base, "test/images_detectadas")

if not os.path.exists(ruta_detectadas):
    os.makedirs(ruta_detectadas)

# Cargar el modelo OCR previamente entrenado
ocr_model = OCRModel(num_classes=37)
ocr_model.load_state_dict(torch.load("modelo_ocr.pth"))
ocr_model.eval()

# Crear el dataset de caracteres
from dataset import CaracteresDataset
ruta_dataset = os.path.join(ruta_base, "caracteres")
dataset = CaracteresDataset(ruta_dataset)

def rotate_image(image, angle):
    """Rota la imagen según el ángulo proporcionado"""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def get_rotation_angle(image):
    """Calcula el ángulo de rotación para corregir la inclinación de la matrícula"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        angles.append(angle)
    
    # Promediar los ángulos para obtener la rotación general
    if angles:
        return np.mean(angles)
    return 0

for filename in os.listdir(ruta_cmax):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        ruta_imagen = os.path.join(ruta_cmax, filename)

        results = model_yolo(ruta_imagen)

        image = cv2.imread(ruta_imagen)

        # Detectar la inclinación y rotar la imagen si es necesario
        angle = get_rotation_angle(image)
        rotated_image = rotate_image(image, angle)

        # Variables para almacenar el texto detectado
        detected_text = []

        for result in results:
            for idx, box in enumerate(result.boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(rotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Recortar la región de la matrícula
                cropped_img = rotated_image[y1:y2, x1:x2]

                # Convertir la imagen recortada a escala de grises
                gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

                # Aplicar un umbral para separar los caracteres
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                # Encontrar contornos en la imagen binarizada
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Filtrar y ordenar los contornos por su posición vertical (de arriba a abajo)
                contours = [contour for contour in contours if cv2.contourArea(contour) > 100]
                contours = sorted(contours, key=lambda contour: cv2.boundingRect(contour)[1])  # Ordenar por Y

                # Crear una carpeta para los caracteres si no existe
                ruta_caracteres = os.path.join(ruta_detectadas, f"{os.path.splitext(filename)[0]}_caracteres")
                if not os.path.exists(ruta_caracteres):
                    os.makedirs(ruta_caracteres)

                # Recorrer los contornos y extraer los caracteres
                for char_idx, contour in enumerate(contours[:8]):  # Limitar a 8 caracteres (ajustar si es necesario)
                    x, y, w, h = cv2.boundingRect(contour)
                    char_img = thresh[y:y+h, x:x+w]  # Extraer cada carácter como una imagen

                    # Guardar cada carácter individual
                    ruta_caracter_img = os.path.join(ruta_caracteres, f"char_{char_idx}.png")
                    cv2.imwrite(ruta_caracter_img, char_img)

                    # Redimensionar y convertir en tensor para la predicción
                    char_img_resized = cv2.resize(char_img, (32, 32))
                    char_tensor = torch.tensor(char_img_resized, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.0

                    # Predicción del carácter con el modelo OCR
                    with torch.no_grad():
                        output = ocr_model(char_tensor)
                        pred = torch.argmax(output, dim=1)

                    # Agregar el carácter detectado a la lista
                    detected_text.append(dataset.caracteres[pred.item()])

        # Mostrar y guardar el texto completo detectado
        all_text = ''.join(detected_text)
        print(f'Todo el texto detectado en {filename}: {all_text}')

        # Guardar la imagen con los rectángulos de detección
        cv2.imwrite(os.path.join(ruta_detectadas, filename), rotated_image)
