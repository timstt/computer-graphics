import os
import numpy as np
from PIL import Image


src = input("Шлях до картинки: ").strip().strip('"')
dst = input("Шлях для збереження: ").strip().strip('"')

image = Image.open(src).convert("RGB")
img = np.array(image, dtype=float)
gray = 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2] 

# Курсова маска "південний схід"
SE = np.array([[1, 1,  1],
               [1, -2,  -1],
               [ 1,  -1,  -1]])

# Курсова маска "південь"
S = np.array([[1, 1, 1],
              [ 1, -2,  1],
              [ -1,  -1,  -1]])

def apply_mask(gray, mask):
    h, w = gray.shape
    out = np.zeros_like(gray)
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            window = gray[y - 1:y + 2, x - 1:x + 2]
            out[y, x] = np.sum(window * mask)   
    return np.clip(np.abs(out), 0, 255).astype(np.uint8)

result_se = apply_mask(gray, SE)
result_s = apply_mask(gray, S)

# збереження результатів
name, ext = os.path.splitext(dst)
if ext == "":
    ext = ".png"

# значення яскравості повторюється в трьох каналах R, G, B
Image.fromarray(result_se).convert("RGB").save(name + "_south_east" + ext)
Image.fromarray(result_s).convert("RGB").save(name + "_south" + ext)

print("\nЗбережено:")
print(name + "_south_east" + ext)
print(name + "_south" + ext)