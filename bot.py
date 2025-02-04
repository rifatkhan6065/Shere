import telebot
import requests
from config import *

# ✅ Telegram Bot সেটআপ
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ✅ Facebook-এ পোস্ট ফাংশন
def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
    params = {
        "message": message,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    return response.json()

# ✅ Facebook Messenger-এ মেসেজ পাঠানোর ফাংশন
def send_facebook_message(message):
    url = f"https://graph.facebook.com/v12.0/me/messages"
    params = {
        "recipient": {"id": FACEBOOK_USER_ID},
        "message": {"text": message},
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    response = requests.post(url, json=params)
    return response.json()

# ✅ Telegram Bot মেসেজ হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "👋 Welcome! Send me a message to share on Facebook.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    # ✅ Facebook পোস্ট
    fb_response = post_to_facebook(text)
    fb_status = fb_response.get("id", "Failed")

    # ✅ Facebook Friend Inbox মেসেজ
    fb_msg_response = send_facebook_message(text)
    fb_msg_status = fb_msg_response.get("recipient_id", "Failed")

    # ✅ Telegram-এ স্ট্যাটাস জানানো
    bot.reply_to(message, f"✅ Facebook Post: {fb_status}\n✅ Facebook Inbox: {fb_msg_status}")

# ✅ Telegram Bot চালু
bot.polling()
