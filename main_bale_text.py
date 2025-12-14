import time
import requests
import json
import sys

# ---------------------------------------------------------
# 👇 تنظیمات بله 👇
BALE_TOKEN = "1966584246:GoviJIXCtftUFwIz1JGB4ijXUwuZBpvDouk"
CHAT_ID = "2087326516"

# 👇 لیست لینک‌ها 👇
DEFAULT_TARGETS = [
    {"name": "کت تک مردانه", "url": "https://www.banimode.com/1319/%DA%A9%D8%AA-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "پیراهن مردانه (همه)", "url": "https://www.banimode.com/11/%D9%BE%DB%8C%D8%B1%D8%A7%D9%87%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "پیراهن مردانه (برندها)", "url": "https://www.banimode.com/11/%D9%BE%DB%8C%D8%B1%D8%A7%D9%87%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?brand=694%2C2113%2C3274%2C522%2C4%2C469%2C1552%2C479%2C1414%2C3328%2C631%2C1238%2C1293%2C1018%2C1256%2C2455%2C693%2C665%2C2038%2C360%2C1%2C2%2C683%2C614%2C415%2C1040%2C849%2C1276%2C3427%2C1335%2C377%2C2080%2C3151%2C445%2C965%2C801%2C82%2C2524%2C1072%2C2713%2C905%2C748%2C488%2C921%2C823%2C733%2C848%2C1148%2C3730&sort%7Cprice=asc"},
    {"name": "ژاکت و پلیور", "url": "https://www.banimode.com/9/%DA%98%D8%A7%DA%A9%D8%AA-%D9%88-%D9%BE%D9%84%DB%8C%D9%88%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوار کتان", "url": "https://www.banimode.com/371/%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%DA%A9%D8%AA%D8%A7%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوار مردانه", "url": "https://www.banimode.com/8/%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "شلوارک مردانه", "url": "https://www.banimode.com/12/%D8%B4%D9%84%D9%88%D8%A7%D8%B1%DA%A9-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کت چرم", "url": "https://www.banimode.com/1780/%DA%A9%D8%AA-%DA%86%D8%B1%D9%85-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "لباس راحتی", "url": "https://www.banimode.com/871/%D9%84%D8%A8%D8%A7%D8%B3-%D8%B1%D8%A7%D8%AD%D8%AA%DB%8C-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کفش ورزشی", "url": "https://www.banimode.com/529/category-men-sport-shoes?sort%7Cprice=asc"},
    {"name": "کفش رسمی", "url": "https://www.banimode.com/817/%DA%A9%D9%81%D8%B4-%D8%B1%D8%B3%D9%85%DB%8C-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کت و شلوار", "url": "https://www.banimode.com/1105/%DA%A9%D8%AA-%D9%88-%D8%B4%D9%84%D9%88%D8%A7%D8%B1-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "لباس ورزشی", "url": "https://www.banimode.com/932/category-men-sportswear?sort%7Cprice=asc"},
    {"name": "پالتو مردانه", "url": "https://www.banimode.com/886/%D9%BE%D8%A7%D9%84%D8%AA%D9%88-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "مایو شنا", "url": "https://www.banimode.com/4651/%D9%85%D8%A7%DB%8C%D9%88-%D8%B4%D9%86%D8%A7-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "برند هالیدی", "url": "https://www.banimode.com/Brand/693/%D9%87%D8%A7%D9%84%DB%8C%D8%AF%DB%8C?category=832%2C871%2C1338%2C11%2C1630%2C8%2C703%2C3205%2C1545%2C1544%2C3&sort%7Cprice=asc"},
    {"name": "کاپشن مردانه", "url": "https://www.banimode.com/883/%DA%A9%D8%A7%D9%BE%D8%B4%D9%86-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"},
    {"name": "کفش روزمره", "url": "https://www.banimode.com/815/%DA%A9%D9%81%D8%B4-%D8%B1%D9%88%D8%B2%D9%85%D8%B1%D9%87-%D9%85%D8%B1%D8%AF%D8%A7%D9%86%D9%87?sort%7Cprice=asc"}
]
# ---------------------------------------------------------

def send_message(text, show_keyboard=False):
    """ارسال پیام متنی به بله با دکمه"""
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    
    # اضافه کردن دکمه اگر لازم باشد
    if show_keyboard:
        keyboard = {
            "keyboard": [[{"text": "📋 دریافت لینک‌ها"}]],
            "resize_keyboard": True
        }
        payload["reply_markup"] = json.dumps(keyboard)
        
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        pass

def get_last_command():
    """خواندن آخرین پیام"""
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/getUpdates"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if not data.get('result'): return None

        last_update = data['result'][-1]
        message = last_update.get('message', {})
        text = message.get('text', '')
        chat_id = str(message.get('chat', {}).get('id'))
        msg_date = message.get('date', 0)
        
        if chat_id != str(CHAT_ID): return None
        # اگر پیام قدیمی‌تر از 15 دقیقه باشد
        if int(time.time()) - msg_date > 1200: return None
            
        return text
    except:
        return None

def main():
    print("--- شروع بررسی ---")
    command = get_last_command()
    
    if not command:
        print("💤 دستوری نیست.")
        return

    print(f"📩 دستور: {command}")

    # 1. اگر دستور "دریافت لینک‌ها" بود
    if "دریافت لینک" in command or command.lower() in ['all', 'list']:
        
        # ساختن یک متن طولانی و مرتب از تمام لینک‌ها
        final_message = "🛍 **لیست دسترسی سریع بانی‌مد:**\n\n"
        
        for item in DEFAULT_TARGETS:
            final_message += f"🔹 {item['name']}\n🔗 {item['url']}\n\n"
            
        final_message += "✅ پایان لیست."
        
        # ارسال پیام یکجا
        send_message(final_message, show_keyboard=True)
        print("✅ لیست ارسال شد.")

    # 2. فعال‌سازی اولیه
    elif command == "/start":
        send_message("👋 سلام! دکمه زیر را بزنید تا لینک‌ها را بفرستم.", show_keyboard=True)

if __name__ == "__main__":
    main()
