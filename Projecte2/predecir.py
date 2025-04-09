from modelo import OCRModel
from dataset import CaracteresDataset
import torch
import cv2
import os

model = OCRModel(num_classes=37)
model.load_state_dict(torch.load("modelo_ocr.pth"))
model.eval()

ruta_base = os.path.dirname(__file__)
ruta_dataset = os.path.join(ruta_base, "caracteres")
dataset = CaracteresDataset(ruta_dataset)

# Imagen de prueba
ruta_imagen = "/home/marc/Documentos/GitHub/IA-MarcJosep/Projecte2/test/images_detectadas/0123_GCW_caracteres/char_3.png" #os.path.join(ruta_base, "caracteres/hola.jpg")
img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (32, 32))
img = torch.tensor(img, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.0

with torch.no_grad():
    salida = model(img)
    pred = torch.argmax(salida, dim=1)
    print(f"Carácter detectado: {dataset.caracteres[pred.item()]}")
