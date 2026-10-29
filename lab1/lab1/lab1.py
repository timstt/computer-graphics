import os
from PIL import Image #для завантаження, зміни розміру та збереження зображень.
import numpy as np

def get_file_paths():
    user_input = input("Введіть шлях до файлу (або кілька через кому): ")
    return [p.strip()
           for p in user_input.split(',') 
            if p.strip()]

# ==========================================
# ЗАВДАННЯ 1: Конвертація форматів
# ==========================================
def task1_convert():
    print("\n--- Завдання 1: Конвертація форматів ---")
    paths = get_file_paths()
    target_fmt = input("Введіть новий формат (jpg, png, bmp): ").strip().lower()
    out_dir = input("Введіть папку для збереження: ").strip()

    for path in paths:
            
        orig_size = os.path.getsize(path)
        img = Image.open(path)
        
        if target_fmt in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        file_name = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join(out_dir, file_name + "." + target_fmt)
        
        img.save(out_path)
        new_size = os.path.getsize(out_path)
        
        # --- Блок порівняння розмірів ---
        diff = new_size - orig_size
        
        if diff > 0:
            diff_str = "збільшився на " + str(diff) + " байт"
        elif diff < 0:
            diff_str = "зменшився на " + str(abs(diff)) + " байт" 
        else:
            diff_str = "не змінився"
            
        print("Збережено: " + out_path)
        print("Розмір: було " + str(orig_size) + " -> стало " + str(new_size) + " байт (" + diff_str + ").")

# ==========================================
# ЗАВДАННЯ 2: Зміна розміру
# ==========================================
def task2_resize():
    print("\n--- Завдання 2: Зміна розміру ---")
    paths = get_file_paths()
    side = input("Змінювати за (w) шириною чи (h) висотою?: ").strip().lower()
    value = int(input("Введіть нове значення у пікселях: "))
    out_dir = input("Введіть папку для збереження: ").strip()

    for path in paths:
            
            img = Image.open(path)
            w, h = img.size
            if side == 'w':
                new_w = value
                new_h = int(h * (value / w))
            else:
                new_h = value
                new_w = int(w * (value / h))
            
            resized = img.resize((new_w, new_h))
            out_path = os.path.join(out_dir, "resized_" + os.path.basename(path))
            
            if resized.mode in ('RGBA', 'P') and out_path.endswith('.jpg'):
                resized = resized.convert('RGB')
                
            resized.save(out_path)
            print("Збережено: " + out_path + " (Новий розмір: " + str(new_w) + "x" + str(new_h) + ")")

# ==========================================
# ЗАВДАННЯ 3: Заміна кольору
# ==========================================
def task3_color():
    print("\n--- Завдання 3: Заміна кольору ---")
    path = input("Введіть шлях до зображення: ").strip()
    
    old_color_input = input("Введіть старий колір (R,G,B через кому): ")
    old_color = tuple(map(int, old_color_input.split(',')))
    
    new_color_input = input("Введіть новий колір (R,G,B через кому): ")
    new_color = tuple(map(int, new_color_input.split(',')))
    
    out_path = input("Введіть повний шлях для збереження: ").strip()

    img = Image.open(path).convert("RGB")
    pixel_data = img.load()
    width, height = img.size
    
    for x in range(width):
        for y in range(height):
            if pixel_data[x, y] == old_color:
                pixel_data[x, y] = new_color
                
    img.save(out_path)
    print("Готово! Збережено у: " + out_path)

# ==========================================
# ЗАВДАННЯ 4: Корекція балансу
# ==========================================
def task4_balance():
    print("\n--- Завдання 4: Корекція колірного балансу ---")
    path = input("Введіть шлях до зображення: ").strip()

    print("Режими: 1 - Червоний, 2 - Зелений, 3 - Синій, 4 - Усі канали")
    mode = input("Ваш вибір (1-4): ").strip()
    
    if mode == '1':
        r_s = int(input("Зсув R: "))
        shifts = (r_s, 0, 0)
    elif mode == '2':
        g_s = int(input("Зсув G: "))
        shifts = (0, g_s, 0)
    elif mode == '3':
        b_s = int(input("Зсув B: "))
        shifts = (0, 0, b_s)
    elif mode == '4':
        r_s = int(input("Зсув R: "))
        g_s = int(input("Зсув G: "))
        b_s = int(input("Зсув B: "))
        shifts = (r_s, g_s, b_s)
    else:
        print("Невірний режим!")
        return
        
    out_path = input("Введіть повний шлях для збереження: ").strip()

    img_rgb = Image.open(path).convert('RGB')
    arr = np.array(img_rgb, dtype=np.int16)
    data = np.clip(arr + shifts, 0, 255)
    
    Image.fromarray(data.astype(np.uint8)).save(out_path)
    print("Готово! Збережено у: " + out_path)


if __name__ == "__main__":
    tasks = {
        '1': task1_convert, 
        '2': task2_resize, 
        '3': task3_color, 
        '4': task4_balance
    }
    
    while True:
        print("\n=== ЛАБОРАТОРНА РОБОТА №1 ===")
        print("1. Конвертація форматів")
        print("2. Зміна розміру")
        print("3. Заміна кольору")
        print("4. Корекція балансу")
        print("0. Вихід")
        
        choice = input("Оберіть номер: ").strip()
        
        if choice == '0':
            print("Вихід з програми...")
            break
        elif choice in tasks:
            tasks[choice]()
        else:
            print("Невірний вибір, спробуйте ще раз.")