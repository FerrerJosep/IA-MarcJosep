import torch
from torch.utils.data import DataLoader, random_split
import torch.optim as optim
from dataset import CaracteresDataset
from modelo import OCRModel  # Guarda el modelo anterior como modelo.py
import os
import torch.nn as nn

ruta_base = os.path.dirname(__file__)
ruta_dataset = os.path.join(ruta_base, "caracteres")
dataset = CaracteresDataset(ruta_dataset)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_set, val_set = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_set, batch_size=32, shuffle=True)
val_loader = DataLoader(val_set, batch_size=32)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = OCRModel(num_classes=len(dataset.caracteres)).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(20):
    model.train()
    running_loss = 0.0
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print(f"Epoch {epoch+1} - Loss: {running_loss:.4f}")

    # Validación
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Accuracy: {100 * correct / total:.2f}%")

torch.save(model.state_dict(), "modelo_ocr.pth")
