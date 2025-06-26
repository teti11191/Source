from flask import Flask, request
import telebot
import os

app = Flask(__name__)

# الحصول على التوكن من المتغيرات البيئية
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Railway توفر متغير بيئي VERCEL_URL تلقائياً
# ولكن بالنسبة لـ Railway، الأفضل استخدام اسم نطاق المشروع أو متغير مخصص إن أردت.
# غالباً لا تحتاج لـ WEBHOOK_URL_BASE في الكود نفسه إذا كنت ستعين الويب هوك يدوياً.
# يكفي فقط تحديد المسار الفريد للويب هوك.
WEBHOOK_URL_PATH = "/webhook/" + BOT_TOKEN # مسار الـ webhook الفريد

bot = telebot.TeleBot(BOT_TOKEN)

# هذا هو المسار الذي سيستقبل الـ webhook من تليجرام
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook_handler():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        return 'bad request', 400

# ... (هنا تأتي معالجات الرسائل والأوامر الأخرى الخاصة بالبوت الخاص بك) ...
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوتك على Railway.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "تلقيت رسالتك: " + message.text)

# **مهم جداً:** هذا الجزء يجعل تطبيق Flask يستمع للمنفذ الذي توفره Railway
if __name__ == "__main__":
    # تعيين الـ webhook (ربما تحتاج لتشغيل هذا السطر مرة واحدة بعد النشر الأول)
    # يمكنك الحصول على URL مشروعك من لوحة تحكم Railway بعد النشر.
    # ثم تستخدمه لتعيين الـ webhook.
    # bot.set_webhook(url="https://YOUR_RAILWAY_PROJECT_URL" + WEBHOOK_URL_PATH)

    port = int(os.environ.get('PORT', 5000)) # 5000 هو منفذ افتراضي لو لم يتم تعيين PORT
    app.run(host='0.0.0.0', port=port)
    
