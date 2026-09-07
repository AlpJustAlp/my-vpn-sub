import os
import requests

BASE_URL = "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/"
OUTPUT_FILE = "subscription.txt"
MAX_FILE_SIZE_MB = 90

def fetch_and_merge():
    all_lines = set()
    print("Просто копируем данные из 25 файлов в один...")
    
    for i in range(1, 26):
        file_name = f"{i}.txt"
        url = f"{BASE_URL}{file_name}"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                plain_text = response.text.strip()
                if not plain_text:
                    continue
                
                for line in plain_text.splitlines():
                    cleaned_line = line.strip()
                    if cleaned_line:
                        all_lines.add(cleaned_line)
                print(f"Успешно скопирован файл: {file_name}")
            else:
                print(f"Не удалось открыть {file_name}. Статус: {response.status_code}")
                    
        except Exception as e:
            print(f"Ошибка при копировании {file_name}: {e}")

    total_lines = len(all_lines)
    print(f"\nВсего уникальных строк после очистки от дубликатов: {total_lines}")

    if total_lines == 0:
        print("Критическая ошибка: Строк нет.")
        raise ValueError("Скрипт скопировал 0 строк.")

    # Переводим в список для возможности безопасной обрезки
    lines_list = list(all_lines)
    
    # Умная подгонка под лимит размера файла
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    current_text = "\n".join(lines_list)
    
    # Если текст весит больше лимита, потихоньку откусываем строки с конца
    if len(current_text.encode('utf-8')) > max_bytes:
        print(f"Внимание: Общий объем превышает {MAX_FILE_SIZE_MB} МБ. Начинаем обрезку строк...")
        while len(current_text.encode('utf-8')) > max_bytes and lines_list:
            # Удаляем последние 500 строк за раз для ускорения процесса
            lines_list = lines_list[:-500]
            current_text = "\n".join(lines_list)
        print(f"Файл успешно ограничен! Осталось строк: {len(lines_list)}")

    # Записываем итоговый оптимизированный текст
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(current_text)
        
    final_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"Готово! Итоговый файл {OUTPUT_FILE} весит: {final_size_mb:.2f} МБ")

    # --- БЛОК АВТОМАТИЧЕСКОЙ ОЧИСТКИ МУСОРА ---
    print("\nУдаляем старые мусорные файлы...")
    for i in range(1, 45):
        trash_file = f"{i}.txt"
        if os.path.exists(trash_file):
            os.remove(trash_file)
            print(f"Удален мусорный файл: {trash_file}")

if __name__ == "__main__":
    fetch_and_merge()
