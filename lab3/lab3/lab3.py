import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np

def get_file_paths():
    user_input = input("Введіть шлях до файлу (або кілька через кому): ")
    return [p.strip() for p in user_input.split(',') if p.strip()]

# ==========================================
# ЛАБ 2, ЗАВДАННЯ 1: Конвертація форматів
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
# ЛАБ 2, ЗАВДАННЯ 2: Зміна розміру
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
# ЛАБ 2, ЗАВДАННЯ 3: Заміна кольору
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
# ЛАБ 2, ЗАВДАННЯ 4: Корекція балансу
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

# ==========================================
# ЛАБ 2, ЗАВДАННЯ 5: Прозорість зображення
# ==========================================
def task5_transparency():
    print("\n--- Завдання 5: Прозорість зображення ---")
    path = input("Введіть шлях до зображення: ").strip()
    alpha = int(input("Введіть рівень прозорості (0-255, де 0 - повністю прозоре): "))
    out_path = input("Введіть повний шлях для збереження (формат .png): ").strip()

    img = Image.open(path).convert("RGBA")
    img.putalpha(alpha)
    img.save(out_path)
    print("Готово! Збережено у: " + out_path)

# ==========================================
# ЛАБ 2, ЗАВДАННЯ 6: Кадрування зображення
# ==========================================
def task6_crop():
    print("\n--- Завдання 6: Кадрування зображення ---")
    path = input("Введіть шлях до зображення: ").strip()
    img = Image.open(path)
    w, h = img.size

    print("Поточний розмір: " + str(w) + "x" + str(h))
    print("Оберіть дію:")
    print("1 - Розбити зображення на частини")
    print("2 - Залишити вибрану область (кадрування)")
    print("3 - Вилучити вибрану область (зробити прозорою)")
    choice = input("Ваш вибір (1-3): ").strip()

    if choice == '1':
        n = int(input("Кількість частин по горизонталі: "))
        m = int(input("Кількість частин по вертикалі: "))
        out_dir = input("Введіть папку для збереження: ").strip()
        os.makedirs(out_dir, exist_ok=True)
        part_w, part_h = w // n, h // m

        for i in range(n):
            for j in range(m):
                box = (i * part_w, j * part_h, (i + 1) * part_w, (j + 1) * part_h)
                part = img.crop(box)
                part.save(os.path.join(out_dir, "part_" + str(i) + "_" + str(j) + ".png"))
        print("Зображення успішно розбито та збережено!")

    elif choice == '2':
        coords = input("Введіть координати (x1, y1, x2, y2) через кому: ")
        x1, y1, x2, y2 = map(int, coords.split(','))
        cropped = img.crop((x1, y1, x2, y2))
        out_path = input("Введіть шлях для збереження: ").strip()
        cropped.save(out_path)
        print("Область збережено у: " + out_path)

    elif choice == '3':
        coords = input("Введіть координати (x1, y1, x2, y2) через кому: ")
        x1, y1, x2, y2 = map(int, coords.split(','))
        img_rgba = img.convert("RGBA")
        
        img_rgba.paste((0, 0, 0, 0), (x1, y1, x2, y2))
        
        out_path = input("Введіть шлях для збереження (.png): ").strip()
        img_rgba.save(out_path)
        print("Область вилучено та збережено у: " + out_path)
    else:
        print("Невірний вибір!")

# ==========================================
# ЛАБ 2, ЗАВДАННЯ 7: Збільшення контрастності
# ==========================================
def task7_contrast():
    print("\n--- Завдання 7: Збільшення контрастності ---")
    path = input("Введіть шлях до зображення: ").strip()
    K = float(input("Введіть коефіцієнт контрастності K (1.0 - без змін, >1.0 - збільшення): "))
    out_path = input("Введіть шлях для збереження: ").strip()

    img = Image.open(path).convert('RGB')
    # Переводимо у float для точних математичних обчислень
    img_float = np.array(img, dtype=np.float32) 
    new_image = np.zeros_like(img_float)

    # Проходимося по трьох каналах (0 - R, 1 - G, 2 - B)
    for c in range(3):
        # Обчислення середнього значення для визначеного каналу
        AveY = np.mean(img_float[:, :, c])
        # Застосовуємо математичну формулу
        new_image[:, :, c] = K * (img_float[:, :, c] - AveY) + AveY
        
    new_image_clipped = np.clip(new_image, 0, 255).astype(np.uint8)
    
    Image.fromarray(new_image_clipped).save(out_path)
    print("Збережено зі зміненою контрастністю у: " + out_path)

# ==========================================
# ЛАБ 3, ЗАВДАННЯ 1: Об'єднання зображень
# ==========================================
def task8_combine():
    print("\n--- Лаб 3, Завдання 1: Об'єднання зображень ---")
    image1_path = input("Введіть шлях до першого зображення: ")
    image2_path = input("Введіть шлях до другого зображення: ")
    output_path = input("Введіть шлях для збереження (напр., result.jpg): ")
    dir_choice = input("Напрямок (1 - горизонтально, 2 - вертикально): ")

    img1 = Image.open(image1_path).convert("RGB")
    img2 = Image.open(image2_path).convert("RGB")

    if dir_choice == '1':
        new_height = img1.height
        aspect_ratio = img2.width / img2.height
        new_width2 = int(aspect_ratio * new_height)
        img2_resized = img2.resize((new_width2, new_height))

        new_width = img1.width + img2_resized.width
        new_img = Image.new('RGB', (new_width, new_height))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2_resized, (img1.width, 0))

    elif dir_choice == '2':
        new_width = img1.width
        aspect_ratio = img2.height / img2.width
        new_height2 = int(aspect_ratio * new_width)
        img2_resized = img2.resize((new_width, new_height2))

        new_height = img1.height + img2_resized.height
        new_img = Image.new('RGB', (new_width, new_height))
        new_img.paste(img1, (0, 0))
        new_img.paste(img2_resized, (0, img1.height))
    else:
        print("Помилка: Неправильний напрямок.")
        return

    new_img.save(output_path)
    print("\nУспіх! Зображення збережено у {}".format(output_path))

# ==========================================
# ЛАБ 3, ЗАВДАННЯ 2: Створення водяного знаку
# ==========================================
def task9_watermark():
    print("\n--- Лаб 3, Завдання 2: Водяний знак ---")
    image_path = input("Введіть шлях до вхідного зображення: ")
    output_path = input("Введіть шлях для збереження (напр., watermarked.jpg): ")
    text = input("Введіть текст водяного знаку: ")

    x = int(input("Введіть координату X (по горизонталі): "))
    y = int(input("Введіть координату Y (по вертикалі): "))
    opacity = int(input("Рівень прозорості (0-255, де 255 - непрозорий): "))
    font_size = int(input("Розмір шрифту: "))
    color_input = input("Введіть колір тексту (R,G,B через кому): ")
    color = tuple(map(int, color_input.split(','))) 

    base_image = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0)) #пусте прозоре полотно 
    draw = ImageDraw.Draw(txt_layer) 

    font = ImageFont.truetype("arial.ttf", font_size)
    text_color = color + (opacity,)
    draw.text((x, y), text,text_color, font)

    watermarked = Image.alpha_composite(base_image, txt_layer)
    watermarked = watermarked.convert("RGB")
    watermarked.save(output_path)
    print("\nУспіх! Водяний знак додано. Збережено у {}".format(output_path))

# ==========================================
# ЛАБ 3, ЗАВДАННЯ 3: Створення слайд-шоу
# ==========================================
def task10_slideshow():
    print("\n--- Лаб 3, Завдання 3: Слайд-шоу ---")
    paths_input = input("Введіть шляхи до зображень через кому (напр., img1.jpg, img2.jpg): ")
    paths = [p.strip() for p in paths_input.split(",")]
    delay_ms = 2000

    print("\nЗапуск слайд-шоу... Закрийте вікно, щоб повернутися до меню.")
    root = tk.Tk() 
    root.title("Слайд-шоу")

    label = tk.Label(root) # створює елемент для показу картинки у вікні
    label.pack()

    def update_image(index):
        if index < len(paths): 
            img = Image.open(paths[index]) 
            img.thumbnail((800, 600)) 
            tk_img = ImageTk.PhotoImage(img)  
            label.config(image=tk_img) 
            label.image = tk_img 

            root.after(delay_ms, update_image, index + 1) 
        else:
            root.quit()
            root.destroy() 

    update_image(0) 
    root.mainloop() 
# ==========================================
# МЕНЮ
# ==========================================
if __name__ == "__main__":
    tasks = {
        '1': task1_convert, 
        '2': task2_resize, 
        '3': task3_color, 
        '4': task4_balance,
        '5': task5_transparency,
        '6': task6_crop,
        '7': task7_contrast,
        '8': task8_combine,
        '9': task9_watermark,
        '10': task10_slideshow
    }
    
    while True:
        print("\n=== ОБРОБКА ЗОБРАЖЕНЬ ===")
        print("1. Конвертація форматів")
        print("2. Зміна розміру")
        print("3. Заміна кольору")
        print("4. Корекція балансу")
        print("5. Додавання прозорості")
        print("6. Кадрування та розбиття")
        print("7. Збільшення контрастності")
        print("8. Об'єднання зображень")
        print("9. Водяний знак")
        print("10. Слайд-шоу")
        print("0. Вихід")
        
        choice = input("Оберіть номер: ").strip()
        
        if choice == '0':
            print("Вихід з програми...")
            break
        elif choice in tasks:
            tasks[choice]()
        else:
            print("Невірний вибір, спробуйте ще раз.")