import urllib.request
import base64
import re

# منابع جدید و همیشه فعال گیت‌هاب برای جمع‌آوری کانفیگ
SOURCES = [
    "https://raw.githubusercontent.com/Deidara61/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/v2ray/sub"
]

def fetch_and_clean():
    all_configs = []
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
                # اگر کل متن با Base64 کدگذاری شده بود
                if "vless://" not in content and "vmess://" not in content:
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith(("vless://", "trojan://", "ss://")):
                        if "@" in line:
                            all_configs.append(line)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
    unique_configs = list(set(all_configs))
    
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_configs))
    print(f"Successfully saved {len(unique_configs)} configs.")

if __name__ == "__main__":
    fetch_and_clean()
