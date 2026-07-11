import urllib.request
import base64
import re

# لیست آدرس‌های گیت‌هاب که فرستادید
URLS = [
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_base64.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/free-nodes/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/base64.txt",
    "https://raw.githubusercontent.com/hans-thomas/v2ray-subscription/main/servers.txt",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray"
]

def is_base64(sb):
    """بررسی اینکه آیا متن دریافتی کدگذاری Base64 است یا خیر"""
    try:
        if isinstance(sb, str):
            sb_bytes = sb.encode('ascii')
        else:
            sb_bytes = sb
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False

def decode_base64(data):
    """رمزگشایی دیتای Base64 به متن معمولی"""
    try:
        # اضافه کردن paddingهای گمشده برای جلوگیری از خطای طول رشته
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except Exception:
        return data

def scrape():
    all_configs = set() # استفاده از set برای حذف خودکار کانفیگ‌های تکراری
    
    print("شروع فرآیند جمع‌آوری کانفیگ‌ها...")
    
    for url in URLS:
        try:
            print(f"در حال دریافت از: {url}")
            # ایجاد درخواست با User-Agent برای جلوگیری از مسدود شدن توسط گیت‌هاب
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore').strip()
                
                # اگر کل فایل Base64 بود آن را باز کند
                if is_base64(content):
                    content = decode_base64(content)
                
                # تک‌تک خطوط فایل را بررسی کند
                lines = content.splitlines()
                for line in lines:
                    line = line.strip()
                    # بررسی پروتکل‌های معروف مثل vless, vmess, ss, trojan
                    if any(line.startswith(proto) for proto in ["vless://", "vmess://", "ss://", "trojan://", "shadowsocks://"]):
                        all_configs.add(line)
                        
        except Exception as e:
            print(f"خطا در دریافت این لینک: {e}")

    # ذخیره کانفیگ‌های استخراج شده در یک فایل متنی
    output_file = "sub.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for config in sorted(all_configs):
                f.write(config + "\n")
        print(f"\nعملیات با موفقیت پایان یافت! {len(all_configs)} کانفیگ یکتا در فایل '{output_file}' ذخیره شد.")
    except Exception as e:
        print(f"خطا در ذخیره‌سازی فایل خروجی: {e}")

if __name__ == "__main__":
    scrape()
