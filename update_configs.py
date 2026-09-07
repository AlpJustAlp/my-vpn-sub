import requests

BASE_URL = "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/"
OUTPUT_FILE = "subscription.txt"

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
                
                # Собираем абсолютно все строки, дубликаты уберутся автоматически
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

    # Объединяем весь этот чистый текст в один файл
    merged_plain_text = "\n".join(all_lines)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(merged_plain_text)
        
    print(f"Готово! Все уникальные прокси слиты в один файл: {OUTPUT_FILE}")
    
    print("\nУдаляем старые мусорные файлы...")
    for i in range(1, 45):  # Проверяем файлы с 1.txt по 44.txt
        trash_file = f"{i}.txt"
        if os.path.exists(trash_file):
            os.remove(trash_file)
            print(f"Удален мусорный файл: {trash_file}")

if __name__ == "__main__":
    fetch_and_merge()
