import telebot
from telebot import types
import json, os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
FILE = "videos.json"

if not os.path.exists(FILE):
    open(FILE, "w").write("{}")

def load():
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):
    data = load()
    if not data:
        bot.send_message(message.chat.id, "حمو المشاكس 😎\nلسه مفيش فيديوهات، ابعتلي فيديو وانا احفظه")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in data.keys():
        markup.add(types.KeyboardButton(name))
    bot.send_message(message.chat.id, "حمو المشاكس 😎\nأهلا بيك! عاوز أنهي فيديو؟", reply_markup=markup)

@bot.message_handler(content_types=['video'])
def save_video(message):
    data = load()
    num = len(data) + 1
    name = f"video{num}"
    data[name] = message.video.file_id
    save(data)
    bot.reply_to(message, f"تمام! حفظت الفيديو باسم {name} ✅")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("video"))
def send_video(message):
    data = load()
    file_id = data.get(message.text)
    if file_id:
        bot.send_video(message.chat.id, file_id, caption=f"الفيديو {message.text} اهو")
    else:
        bot.reply_to(message, "الفيديو مش موجود")

print("البوت شغال...")
bot.polling()
