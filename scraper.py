import urllib.request
import base64

# دو منبع فوق‌العاده فعال و پایدار در سال ۲۰۲۶
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Borders-Freedom/freedom/main/All_Configs_Sub.txt"
]

def fetch_and_clean():
    all_configs = []
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
                # بررسی اینکه آیا کل متن Base64 است یا خیر
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
    
    # اگر هیچ کانفیگی پیدا نشد، یک کانفیگ تست می‌نویسیم تا فایل هیچ‌وقت خالی نماند
    if not unique_configs:
        unique_configs = ["vless://dummy_config_if_sources_were_empty@127.0.0.1:443?encryption=none&security=reality#NoConfigsFound"]
    
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_configs))
    print(f"Successfully saved {len(unique_configs)} configs.")

if __name__ == "__main__":
    fetch_and_clean()
