import base64
import urllib.request

BASE_URL = "https://githubusercontent.com"
OUTPUT_FILE = "subscription.txt"

def fetch_and_merge():
    all_links = set()
    print("Начинаем сбор конфигураций в облаке...")
    
    for i in range(1, 26):
        file_name = f"{i}.txt"
        url = f"{BASE_URL}{file_name}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                encoded_content = response.read().decode('utf-8').strip()
                
            if not encoded_content:
                continue
                
            cleaned_encoded = "".join(encoded_content.split())
            cleaned_encoded += "=" * ((4 - len(cleaned_encoded) % 4) % 4)
            
            decoded_bytes = base64.b64decode(cleaned_encoded)
            decoded_text = decoded_bytes.decode("utf-8", errors="ignore")
            
            for line in decoded_text.splitlines():
                link = line.strip()
                if link and any(link.startswith(p) for p in ["vless://", "vmess://", "ss://", "ssr://", "trojan://", "hysteria", "tuic"]):
                    all_links.add(link)
                    
        except Exception as e:
            print(f"Пропуск {file_name}: {e}")

    if not all_links:
        print("Нечего сохранять.")
        return

    print(f"Собрано уникальных ссылок: {len(all_links)}")

    merged_plain_text = "\n".join(all_links)
    final_base64 = base64.b64encode(merged_plain_text.encode("utf-8")).decode("utf-8")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_base64)
        
    print("Файл успешно перезаписан!")

if __name__ == "__main__":
    fetch_and_merge()
