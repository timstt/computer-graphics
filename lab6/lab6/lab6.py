import numpy as np
from PIL import Image

np.random.seed(1)      # щоб шум щоразу був однаковий і результати збігалися
N = 128                # висота зображення
M = 128                # ширина зображення


# ======================================================================
# 1. СТВОРЕННЯ 9 ТЕСТОВИХ ЗОБРАЖЕНЬ
# ======================================================================

# Зображення 0: чисте. Беремо фото, робимо сірим і розміром 128x128.
path = input("Введіть шлях до зображення: ").strip().strip('"')
photo = Image.open(path).convert("L").resize((M, N))
clean = np.array(photo, dtype=float)

# Координати пікселів: x - номер стовпця, y - номер рядка
y, x = np.mgrid[0:N, 0:M]


def gauss_noise(sigma):
    """Гаусів шум із нульовим середнім і стандартним відхиленням sigma."""
    return np.random.normal(0, 1, (N, M)) * sigma


def salt_pepper(image, p):
    """Імпульсний шум: частка p пікселів стає чорною (0) або білою (255)."""
    result = image.copy()
    r = np.random.random((N, M))          # випадкове число для кожного пікселя
    result[r < p / 2] = 0                 # "перець"
    result[(r >= p / 2) & (r < p)] = 255  # "сіль"
    return result


images = []
images.append(clean)                                        # 0: без шуму

images.append(clean + gauss_noise(10))                      # 1: адитивний, σ = 10
images.append(clean + gauss_noise(25))                      # 2: адитивний, σ = 25

images.append(salt_pepper(clean, 0.05))                     # 3: імпульсний, p = 0.05
images.append(salt_pepper(clean, 0.20))                     # 4: імпульсний, p = 0.20

# Дисперсія залежить від яскравості: σ² = α * I, тому σ = sqrt(α * I)
images.append(clean + gauss_noise(np.sqrt(0.5 * clean)))    # 5: α = 0.5
images.append(clean + gauss_noise(np.sqrt(3.0 * clean)))    # 6: α = 3

# Дисперсія залежить від координат
var_linear = 6 * x + 3 * y + 10                             # σ² = αx + βy + γ
var_square = 0.25 * (x - 64) ** 2 + 0.25 * (y - 64) ** 2 + 10   # σ² = αx² + βy² + γ
images.append(clean + gauss_noise(np.sqrt(var_linear)))     # 7
images.append(clean + gauss_noise(np.sqrt(var_square)))     # 8

# Зберігаємо у файли image0.bmp ... image8.bmp і читаємо їх назад.
# Так ми працюємо саме з тим, що лежить у файлах (значення 0..255, цілі).
pictures = []
for k in range(9):
    file_name = "image" + str(k) + ".bmp"
    saved = np.clip(np.round(images[k]), 0, 255).astype(np.uint8)
    Image.fromarray(saved).save(file_name)
    pictures.append(np.array(Image.open(file_name), dtype=float))


# ======================================================================
# 2. ФІЛЬТРИ
# Кожен фільтр - це правило: з вікна пікселів (маленький квадрат
# навколо пікселя) отримати одне нове значення для центрального пікселя.
# ======================================================================

# --- лінійні фільтри (нове значення = сума пікселів вікна з вагами) ---

def average(window):
    """Усереднення: звичайне середнє всіх пікселів вікна."""
    return window.mean()


# Ваги гаусового фільтра 3x3: центр важить найбільше
gauss_weights = np.array([[1, 2, 1],
                          [2, 4, 2],
                          [1, 2, 1]]) / 16


def gauss(window):
    """Гаусів фільтр: зважена сума, ближчі до центру пікселі важать більше."""
    return (window * gauss_weights).sum()


# --- нелінійні фільтри (нове значення = не сума, а щось інше) ---

def median(window):
    """Медіана: середнє значення за порядком, якщо пікселі впорядкувати."""
    return np.median(window)


def minimum(window):
    """Мінімум вікна."""
    return window.min()


def maximum(window):
    """Максимум вікна."""
    return window.max()


def midpoint(window):
    """Середина між мінімумом і максимумом."""
    return (window.min() + window.max()) / 2


def trimmed_mean(window):
    """Усічене середнє: відкидаємо 2 найменші й 2 найбільші, решту усереднюємо."""
    values = np.sort(window.flatten())   # усі 9 значень по порядку
    return values[2:7].mean()


def geometric_mean(window):
    """Геометричне середнє (+1, щоб не брати логарифм від нуля)."""
    return np.exp(np.log(window + 1).mean()) - 1


def apply_filter(image, size, rule):
    """
    Застосовує фільтр до всього зображення.
    size - розмір вікна (3 означає 3x3, 5 означає 5x5)
    rule - функція, яка з вікна рахує нове значення.
    Границі зображення не обробляємо: там лишається старе значення.
    """
    half = size // 2
    result = image.copy()
    for i in range(half, N - half):
        for j in range(half, M - half):
            window = image[i - half:i + half + 1, j - half:j + half + 1]
            result[i, j] = rule(window)
    return result


# Список фільтрів: (назва, розмір вікна, правило)
filters = [
    # лінійні
    ("Усереднюючий 3x3", 3, average),
    ("Усереднюючий 5x5", 5, average),
    ("Гаусса 3x3", 3, gauss),
    # нелінійні
    ("Медіанний 3x3", 3, median),
    ("Медіанний 5x5", 5, median),
    ("Мінімум 3x3", 3, minimum),
    ("Максимум 3x3", 3, maximum),
    ("Середня точка 3x3", 3, midpoint),
    ("Усічене середнє 3x3", 3, trimmed_mean),
    ("Геометричне 3x3", 3, geometric_mean),
]


def distortion(filtered, original):
    """Спотворення eps^2 = середнє від (filtered - original)^2 по всіх пікселях."""
    return np.sum((filtered - original) ** 2) / (N * M)


# ======================================================================
# 3. ЗАВДАННЯ 2: спотворення чистого зображення кожним фільтром
# ======================================================================

print("\nЗавдання 2: спотворення чистого зображення кожним фільтром")
print("Фільтр".ljust(22) + "eps^2".rjust(10))

for name, size, rule in filters:
    filtered = apply_filter(pictures[0], size, rule)
    value = distortion(filtered, pictures[0])
    print(name.ljust(22) + "{:.2f}".format(value).rjust(10))


# ======================================================================
# 4. ЗАВДАННЯ 3: якість фільтрації зашумлених зображень 1..8
# ======================================================================

noise_names = ["Адит σ=10", "Адит σ=25", "Імп p=0.05", "Імп p=0.20",
               "σ²=0.5·I", "σ²=3·I", "σ²=лін(x,y)", "σ²=кв(x,y)"]

print("\nЗавдання 3: якість фільтрації зашумлених зображень")
print("Фільтр".ljust(22), end="")
for noise in noise_names:
    print(noise.rjust(13), end="")
print()

for name, size, rule in filters:
    print(name.ljust(22), end="")
    for k in range(1, 9):
        filtered = apply_filter(pictures[k], size, rule)
        value = distortion(filtered, pictures[k])
        print("{:.2f}".format(value).rjust(13), end="")
    print()
