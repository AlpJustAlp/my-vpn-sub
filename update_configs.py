import base64
import requests

# Точный и проверенный адрес до raw-файлов (обрати внимание на слэш на конце!)
BASE_URL = "https://raw.githubusercontent.com/AvenCores/goida-vpn-configs/refs/heads/main/githubmirror/"
OUTPUT_FILE = "subscription.txt"

def fetch_and_merge():
    all_links = set()
    print("Начинаем сбор конфигураций в облаке...")
    
    for i in range(1, 26):
        file_name = f"{i}.txt"
        # Правильно и безопасно склеиваем ссылку
        url = f"{BASE_URL}{file_name}"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            print(f"Файл {file_name} -> Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                plain_text = response.text.strip()
                if not plain_text:
                    print(f"Предупреждение: файл {file_name} пустой внутри.")
                    continue
                
                lines_count = 0
                # Файлы уже текстовые, просто читаем их построчно
                for line in plain_text.splitlines():
                    link = line.strip()
                    # Сохраняем только строчки, которые начинаются с протоколов VPN
                    if link and any(link.startswith(p) for p in ["vless://", "vmess://", "ss://", "ssr://", "trojan://", "hysteria", "tuic"]):
                        all_links.add(link)
                        lines_count += 1
                print(f"Успешно извлечено ссылок из {file_name}: {lines_count}")
            else:
                print(f"Не удалось скачать {file_name}. Статус: {response.status_code}")
                    
        except Exception as e:
            print(f"Ошибка при обработке {file_name} (Ссылка: {url}): {e}")

    print(f"\nВсего уникальных ссылок собрано: {len(all_links)}")

    if not all_links:
        print("Критическая ошибка: Массив ссылок пуст! Записывать нечего.")
        raise ValueError("Скрипт не смог собрать данные")

    # Объединяем все чистые ссылки через перенос строки
    merged_plain_text = "\n".join(all_links)
    
    # Кодируем ИТОГОВЫЙ результат в Base64 для v2rayN
    final_base64 = base64.b64encode(merged_plain_text.encode("utf-8")).decode("utf-8")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_base64)
        
    print("Файл subscription.txt успешно перезаписан плотными данными!")

if __name__ == "__main__":
    fetch_and_merge()
