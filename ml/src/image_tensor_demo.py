from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms


IMAGE_PATH = Path(
    "/Users/macbook/Desktop/FruitVision/uploads/1becede6892d4cfa908c2a6947042bc9.png"
)


image = Image.open(IMAGE_PATH)

print("Original image:")
print("Format:", image.format)
print("Mode:", image.mode)
print("Size:", image.size)


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


tensor = transform(image)
tensor = tensor.unsqueeze(0)  # Add batch dimension

print()
print("Tensor:")
print("Shape:", tensor.shape)
print("Dimensions:", tensor.ndim)
print("Data type:", tensor.dtype)
print("Minimum:", tensor.min())
print("Maximum:", tensor.max())