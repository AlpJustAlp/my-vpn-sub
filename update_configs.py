import os
import requests

BASE_URL = "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/"
LINES_PER_FILE = 15000

def fetch_and_merge():
    all_lines = set()
    print("Просто копируем данные из 25 файлов...")
    
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
                
                # Просто собираем все строки как есть, убирая дубликаты
                for line in plain_text.splitlines():
                    cleaned_line = line.strip()
                    if cleaned_line:
                        all_lines.add(cleaned_line)
                print(f"Скопирован файл: {file_name}")
            else:
                print(f"Не удалось открыть {file_name}. Статус: {response.status_code}")
                    
        except Exception as e:
            print(f"Ошибка при копировании {file_name}: {e}")

    total_lines = len(all_lines)
    print(f"\nВсего уникальных строк скопировано: {total_lines}")

    if total_lines == 0:
        print("Критическая ошибка: Данных нет.")
        raise ValueError("Скрипт скопировал 0 строк.")

    # Переводим в список, чтобы нарезать по 15 000 строк
    lines_list = list(all_lines)
    
    # Режем на файлы и сохраняем
    file_counter = 1
    for start_idx in range(0, total_lines, LINES_PER_FILE):
        end_idx = start_idx + LINES_PER_FILE
        chunk = lines_list[start_idx:end_idx]
        
        output_file = f"{file_counter}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))
            
        print(f"Записан файл {output_file} (строк: {len(chunk)})")
        file_counter += 1

if __name__ == "__main__":
    fetch_and_merge()
