import urllib.request
import base64
import re

# لیست آدرس‌هایی که کانفیگ‌های رایگان را به اشتراک می‌گذارند
SOURCES = [
    "https://raw.githubusercontent.com/freev2rayuser/freev2ray/main/v2ray",
    "https://raw.githubusercontent.com/IranianBypass/V2ray-Configs/main/Splitted-Configs/vless.txt"
]

def fetch_and_clean():
    all_configs = []
    
    for url in SOURCES:
        try:
            # دانلود دیتای لینک
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
                # اگر متن با Base64 کدگذاری شده بود، آن را باز می‌کنیم
                if "vless://" not in content and "vmess://" not in content:
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                # جدا کردن خط به خط کانفیگ‌ها
                for line in content.splitlines():
                    line = line.strip()
                    # فقط کانفیگ‌های معتبر نسل جدید (VLESS/Trojan/SS) را جدا میکنیم
                    if line.startswith(("vless://", "trojan://", "ss://")):
                        # یک فیلتر ساده برای حذف کانفیگ‌های نامعتبر یا بسیار قدیمی
                        if "@" in line:
                            all_configs.append(line)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
    # حذف کانفیگ‌های تکراری
    unique_configs = list(set(all_configs))
    
    # ذخیره نهایی در فایل متنی
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_configs))
    print(f"Successfully saved {len(unique_configs)} configs.")

if __name__ == "__main__":
    fetch_and_clean()
