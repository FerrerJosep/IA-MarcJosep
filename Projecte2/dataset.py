import os
import cv2
import torch
from torch.utils.data import Dataset
from torchvision import transforms

class CaracteresDataset(Dataset):
    def __init__(self, carpeta, transform=None):
        self.imagenes = []
        self.labels = []
        self.transform = transform
        self.caracteres = sorted(list(set([f.split("_")[0] for f in os.listdir(carpeta)])))
        self.caracter_a_idx = {c: i for i, c in enumerate(self.caracteres)}
        
        for file in os.listdir(carpeta):
            if file.endswith(".jpg") or file.endswith(".png"):
                etiqueta = file.split("_")[0]
                img_path = os.path.join(carpeta, file)
                self.imagenes.append(img_path)
                self.labels.append(self.caracter_a_idx[etiqueta])
        
    def __len__(self):
        return len(self.imagenes)
    
    def __getitem__(self, idx):
        img = cv2.imread(self.imagenes[idx], cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (32, 32))
        if self.transform:
            img = self.transform(img)
        else:
            img = torch.tensor(img, dtype=torch.float32).unsqueeze(0) / 255.0
        label = self.labels[idx]
        return img, label
