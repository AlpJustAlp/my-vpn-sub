import base64
import requests

# Точный и проверенный адрес до raw-файлов (обрати внимание на слэш на конце!)
BASE_URL = "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/"
OUTPUT_FILE = "subscription.txt"

# Максимальное количество серверов в одной подписке, чтобы не вешать v2rayN и уложиться в лимиты GitHub
MAX_LINKS = 50000

def fetch_and_merge():
    all_links = set()
    print("Начинаем сбор конфигураций в облаке...")
    
    for i in range(1, 26):
        file_name = f"{i}.txt"
        url = f"{BASE_URL}{file_name}"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            print(f"Файл {file_name} -> Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                plain_text = response.text.strip()
                if not plain_text:
                    continue
                
                lines_count = 0
                for line in plain_text.splitlines():
                    link = line.strip()
                    if link and any(link.startswith(p) for p in ["vless://", "vmess://", "ss://", "ssr://", "trojan://", "hysteria", "tuic"]):
                        all_links.add(link)
                        lines_count += 1
                print(f"Успешно прочитано строк из {file_name}: {lines_count}")
            else:
                print(f"Ошибка скачивания {file_name}. Код: {response.status_code}")
                    
        except Exception as e:
            print(f"Не удалось обработать файл {file_name}: {e}")

    print(f"\nВсего уникальных прокси найдено: {len(all_links)}")

    if not all_links:
        print("Критическая ошибка: Конфигов нет.")
        raise ValueError("Скрипт собрал 0 подписок.")

    # Обрезаем массив до разумного количества, если серверов слишком много
    links_list = list(all_links)
    if len(links_list) > MAX_LINKS:
        print(f"Внимание: Ссылок слишком много! Ограничиваем подписку до первых {MAX_LINKS} серверов.")
        links_list = links_list[:MAX_LINKS]

    # Объединяем итоговый список
    merged_plain_text = "\n".join(links_list)
    final_base64 = base64.b64encode(merged_plain_text.encode("utf-8")).decode("utf-8")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_base64)
        
    print(f"Файл успешно сохранен! В подписку упало ровно {len(links_list)} серверов.")

if __name__ == "__main__":
    fetch_and_merge()
