import gdown
from pathlib import Path
import timeit

def bad_character_heuristic(substring):
    bad_char = {}
    m = len(substring)
    for i in range(m - 1):
        bad_char[substring[i]] = m - 1 - i
    return bad_char

def good_suffix_heuristic(substring):
    m = len(substring)
    suffixes = [0] * m
    k = m - 1
    for i in range(m - 2, -1, -1):
        if i > k and suffixes[i + m - 1 - k] < i - k:
            suffixes[i] = suffixes[i + m - 1 - k]
        else:
            j = max(0, k - i)
            while i - j >= 0 and substring[i - j] == substring[k - j]:
                j += 1
            suffixes[i] = j
            k = i
    return suffixes

def boyer_moore(substring, text):
    m = len(substring)
    n = len(text)

    bad_char = bad_character_heuristic(substring)
    good_suffix = good_suffix_heuristic(substring)

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and substring[j] == text[i + j]:
            j -= 1

        if j < 0:
            # Знайдено підрядок
            return i

        x = bad_char.get(text[i + j], m)
        y = j - good_suffix[j]

        i += max(x, y)

    return -1

def compute_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0

    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k

    return pi

def kmp_search(pattern, text):
    n = len(text)
    m = len(pattern)
    pi = compute_prefix_function(pattern)
    q = 0

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]

        if pattern[q] == text[i]:
            q += 1

        if q == m:
            return i - m + 1

    return -1

def rabin_karp_search(pattern, text):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    h = pow(d, m - 1, q)
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t and pattern == text[i:i + m]:
            return i

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q

    return -1

def download_and_get_text(google_drive_id, destination_folder):
    # Створюємо шлях для збереження завантаженого текстового файлу
    download_path = destination_folder / f"{google_drive_id}.txt"
    
    # Завантаження текстового файлу з Google Drive
    gdown.download(f"https://drive.google.com/uc?id={google_drive_id}", download_path, quiet=False)
    
    # Читаємо текст з файлу
    with open(download_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    return text

# Google Drive ID для текстового файлу 1
file1_google_drive_id = "1InFE6KGZwkEOSTaC5vMZvGsGGJKV1DMA"

# Google Drive ID для текстового файлу 2
file2_google_drive_id = "1ofVa-00z-VoMs9493FQAgHZEwsXE8kMt"

# Шлях, куди будуть завантажені тексти (диск D)
destination_folder = Path("D:")

# Завантаження текстових файлів
text_file1 = download_and_get_text(file1_google_drive_id, destination_folder)
text_file2 = download_and_get_text(file2_google_drive_id, destination_folder)

# Отримання тексту з файлів
text_file1 = download_and_get_text(file1_google_drive_id, destination_folder)
text_file2 = download_and_get_text(file2_google_drive_id, destination_folder)

# Тексти для пошуку
existing_substring = "бібліотека, що доступна"
fake_substring = "Частину коштів від проданих квитків"

# Функція для вимірювання часу виконання алгоритму для конкретного тексту та підрядка
def measure_algorithm(algorithm_function, substring, text):
    setup_code = f"""
from __main__ import {algorithm_function}

# Виклик алгоритму пошуку підрядка
{algorithm_function}("{substring}", "{text}")
"""

    time_taken = timeit.timeit(stmt=algorithm_function, setup=setup_code, number=100)

    return time_taken / 100

# Вимірюємо час для кожного алгоритму та підрядка для обох текстів
bm_existing_time_file1 = measure_algorithm("boyer_moore", existing_substring, text_file1)
bm_fake_time_file1 = measure_algorithm("boyer_moore", fake_substring, text_file1)

kmp_existing_time_file1 = measure_algorithm("kmp_search", existing_substring, text_file1)
kmp_fake_time_file1 = measure_algorithm("kmp_search", fake_substring, text_file1)

rk_existing_time_file1 = measure_algorithm("rabin_karp_search", existing_substring, text_file1)
rk_fake_time_file1 = measure_algorithm("rabin_karp_search", fake_substring, text_file1)

bm_existing_time_file2 = measure_algorithm("boyer_moore", existing_substring, text_file2)
bm_fake_time_file2 = measure_algorithm("boyer_moore", fake_substring, text_file2)

kmp_existing_time_file2 = measure_algorithm("kmp_search", existing_substring, text_file2)
kmp_fake_time_file2 = measure_algorithm("kmp_search", fake_substring, text_file2)

rk_existing_time_file2 = measure_algorithm("rabin_karp_search", existing_substring, text_file2)
rk_fake_time_file2 = measure_algorithm("rabin_karp_search", fake_substring, text_file2)

# Виводимо результати у вигляді порівняльної таблиці
print("{:<15} {:<25} {:<25} {:<25} {:<25}".format("Алгоритм", "Файл 1 (існуючий)", "Файл 1 (вигаданий)", "Файл 2 (існуючий)", "Файл 2 (вигаданий)"))
print("-" * 120)
print("{:<15} {:<25.6f} {:<25.6f} {:<25.6f} {:<25.6f}".format("Boyer-Moore", bm_existing_time_file1, bm_fake_time_file1, bm_existing_time_file2, bm_fake_time_file2))
print("{:<15} {:<25.6f} {:<25.6f} {:<25.6f} {:<25.6f}".format("KMP", kmp_existing_time_file1, kmp_fake_time_file1, kmp_existing_time_file2, kmp_fake_time_file2))
print("{:<15} {:<25.6f} {:<25.6f} {:<25.6f} {:<25.6f}".format("Rabin-Karp", rk_existing_time_file1, rk_fake_time_file1, rk_existing_time_file2, rk_fake_time_file2))
