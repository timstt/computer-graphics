import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # графіки не відкриваються у вікні, а лише зберігаються у файл
import matplotlib.pyplot as plt
from PIL import Image

# ==========================================
# Допоміжні функції
# ==========================================
def get_out_path(example, default_ext):
    # Запитуємо шлях (ім'я файлу) для збереження
    out_path = input("Введіть шлях для збереження (напр., " + example + "): ").strip()
    return out_path

def brightness_matrix(img):
    # Розкладаємо зображення на канали R, G, B
    arr = np.array(img.convert("RGB"), dtype=np.float32)
    R = arr[:, :, 0]
    G = arr[:, :, 1]
    B = arr[:, :, 2]
    # Формула яскравості: Y = 0.299*R + 0.587*G + 0.114*B
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    return np.clip(np.round(Y), 0, 255).astype(np.uint8)

# ==========================================
# ЛАБ 4, ЗАВДАННЯ 1: Виведення кольорового зображення
# ==========================================
def task1_show():
    print("\n--- Завдання 1: Виведення кольорового зображення ---")
    path = input("Введіть шлях до зображення: ").strip()

    img = Image.open(path).convert("RGB")
    w, h = img.size
    print("Розмір зображення: " + str(w) + "x" + str(h))

    # Відкриваємо зображення у стандартному переглядачі системи
    img.show()

# ==========================================
# ЛАБ 4, ЗАВДАННЯ 2: Матриця значень яскравості
# ==========================================
def task2_matrix():
    print("\n--- Завдання 2: Матриця значень яскравості ---")
    path = input("Введіть шлях до зображення: ").strip()
    out_path = get_out_path("matrix.txt", ".txt")

    img = Image.open(path).convert("RGB")
    Y = brightness_matrix(img)
    h, w = Y.shape
    print("Розмір матриці: " + str(h) + " рядків x " + str(w) + " стовпців")

    # Приклад розрахунку яскравості для першого пікселя (для звіту)
    r, g, b = img.getpixel((0, 0))
    y = 0.299 * r + 0.587 * g + 0.114 * b
    print("\nПриклад розрахунку для пікселя (0, 0): R=" + str(r) + ", G=" + str(g) + ", B=" + str(b))
    print("Y = 0.299*" + str(r) + " + 0.587*" + str(g) + " + 0.114*" + str(b)
          + " = " + str(round(y, 3)) + " ≈ " + str(round(y)))

    # Виводимо на екран фрагмент матриці (вся матриця занадто велика для консолі)
    n = min(10, h, w)
    print("\nФрагмент матриці яскравості " + str(n) + "x" + str(n) + " (лівий верхній кут):")
    print(Y[:n, :n])

    # Повну матрицю зберігаємо у текстовий файл
    np.savetxt(out_path, Y, fmt="%3d")
    print("Повну матрицю збережено у: " + out_path)

# ==========================================
# ЛАБ 4, ЗАВДАННЯ 3: Гістограма яскравості кольорового зображення
# ==========================================
def task3_histogram():
    print("\n--- Завдання 3: Гістограма яскравості ---")
    path = input("Введіть шлях до зображення: ").strip()
    out_path = get_out_path("histogram.png", ".png")

    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    Y = brightness_matrix(img)

    # Рахуємо, скільки пікселів має кожне значення яскравості 0..255
    hist_Y = np.bincount(Y.ravel(), minlength=256)
    hist_R = np.bincount(arr[:, :, 0].ravel(), minlength=256)
    hist_G = np.bincount(arr[:, :, 1].ravel(), minlength=256)
    hist_B = np.bincount(arr[:, :, 2].ravel(), minlength=256)

    print("Середня яскравість зображення: " + str(round(np.mean(Y), 2)))

    x = np.arange(256)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    ax1.bar(x, hist_Y, width=1.0, color="gray")
    ax1.set_title("Гістограма яскравості Y")

    ax2.plot(x, hist_R, color="red", label="R")
    ax2.plot(x, hist_G, color="green", label="G")
    ax2.plot(x, hist_B, color="blue", label="B")
    ax2.set_title("Гістограми каналів R, G, B")
    ax2.legend()

    for ax in (ax1, ax2):
        ax.set_xlim(0, 255)
        ax.set_xlabel("Значення яскравості")
        ax.set_ylabel("Кількість пікселів")
    plt.tight_layout()

    fig.savefig(out_path)
    plt.close(fig)
    print("Гістограму збережено у: " + out_path)

# ==========================================
# ЛАБ 4, ЗАВДАННЯ 4: Зміна кольоровості
# ==========================================
def task4_color_change():
    print("\n--- Завдання 4: Зміна кольоровості ---")
    path = input("Введіть шлях до зображення: ").strip()

    print("Оберіть дію:")
    print("1 - Бінаризація (чорно-біле)")
    print("2 - Відтінки сірого")
    print("3 - Негатив")
    print("4 - Гістограма зображення в градаціях сірого")
    choice = input("Ваш вибір (1-4): ").strip()

    img = Image.open(path).convert("RGB")
    Y = brightness_matrix(img)

    if choice == '1':
        P = int(input("Введіть поріг P (0-255, напр. 128): "))
        out_path = get_out_path("binary.png", ".png")
        # Якщо Y <= P — чорний (0), інакше — білий (255)
        bw = np.where(Y <= P, 0, 255).astype(np.uint8)
        Image.fromarray(bw).save(out_path)

    elif choice == '2':
        out_path = get_out_path("gray.png", ".png")
        # R = G = B = Y
        Image.fromarray(Y).convert("RGB").save(out_path)

    elif choice == '3':
        out_path = get_out_path("negative.png", ".png")
        # Кожен канал: 255 - значення
        arr = np.array(img)
        neg = 255 - arr
        Image.fromarray(neg.astype(np.uint8)).save(out_path)

    elif choice == '4':
        out_path = get_out_path("gray_histogram.png", ".png")
        hist = np.bincount(Y.ravel(), minlength=256)
        fig = plt.figure(figsize=(10, 5))
        plt.bar(np.arange(256), hist, width=1.0, color="dimgray")
        plt.xlim(0, 255)
        plt.title("Гістограма зображення в градаціях сірого")
        plt.xlabel("Значення яскравості")
        plt.ylabel("Кількість пікселів")
        plt.tight_layout()
        fig.savefig(out_path)
        plt.close(fig)

    else:
        print("Невірний вибір!")
        return

    print("Готово! Збережено у: " + out_path)

# ==========================================
# МЕНЮ
# ==========================================
if __name__ == "__main__":
    tasks = {
        '1': task1_show,
        '2': task2_matrix,
        '3': task3_histogram,
        '4': task4_color_change
    }

    while True:
        print("\n=== ЛАБОРАТОРНА РОБОТА №4 ===")
        print("1. Виведення кольорового зображення")
        print("2. Матриця значень яскравості")
        print("3. Гістограма яскравості")
        print("4. Зміна кольоровості (бінаризація, сірий, негатив, гістограма)")
        print("0. Вихід")

        choice = input("Оберіть номер: ").strip()

        if choice == '0':
            print("Вихід з програми...")
            break
        elif choice in tasks:
            tasks[choice]()
        else:
            print("Невірний вибір, спробуйте ще раз.")