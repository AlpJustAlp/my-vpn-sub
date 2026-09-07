import base64
import requests

BASE_URL = "https://githubusercontent.com"
OUTPUT_FILE = "subscription.txt"

def fetch_and_merge():
    all_links = set()
    print("Начинаем сбор конфигураций в облаке...")
    
    for i in range(1, 26):
        file_name = f"{i}.txt"
        url = f"{BASE_URL}{file_name}"
        
        try:
            # Делаем запрос с таймаутом и обманкой под браузер
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            print(f"Файл {file_name} -> Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                encoded_content = response.text.strip()
                if not encoded_content:
                    print(f"Предупреждение: файл {file_name} пустой внутри.")
                    continue
                    
                cleaned_encoded = "".join(encoded_content.split())
                cleaned_encoded += "=" * ((4 - len(cleaned_encoded) % 4) % 4)
                
                decoded_bytes = base64.b64decode(cleaned_encoded)
                decoded_text = decoded_bytes.decode("utf-8", errors="ignore")
                
                lines_count = 0
                for line in decoded_text.splitlines():
                    link = line.strip()
                    if link and any(link.startswith(p) for p in ["vless://", "vmess://", "ss://", "ssr://", "trojan://", "hysteria", "tuic"]):
                        all_links.add(link)
                        lines_count += 1
                print(f"Успешно извлечено ссылок из {file_name}: {lines_count}")
                    
        except Exception as e:
            print(f"Ошибка при обработке {file_name}: {e}")

    print(f"\nВсего уникальных ссылок собрано: {len(all_links)}")

    if not all_links:
        print("Критическая ошибка: Массив ссылок пуст! Записывать нечего.")
        # Намеренно вызываем ошибку, чтобы пустой файл не коммитился
        raise ValueError("Скрипт не смог собрать данные")

    merged_plain_text = "\n".join(all_links)
    final_base64 = base64.b64encode(merged_plain_text.encode("utf-8")).decode("utf-8")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_base64)
        
    print("Файл subscription.txt успешно перезаписан плотными данными!")

if __name__ == "__main__":
    fetch_and_merge()
