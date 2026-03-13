import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# إعداد التوكن (يفضل وضعه في Environment Variables على Render)
API_TOKEN = os.getenv("BOT_TOKEN") 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- لوحة الأزرار الرئيسية (التي تظهر أسفل الرسالة) ---
def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🎬 الأفلام", callback_data="movies")
    btn2 = InlineKeyboardButton("📺 المسلسلات", callback_data="series")
    btn3 = InlineKeyboardButton("🔍 بحث سريع", switch_inline_query_current_chat="")
    btn4 = InlineKeyboardButton("⭐ أفلام مختارة", callback_data="featured")
    keyboard.add(btn1, btn2, btn3, btn4)
    return keyboard

# --- عند إرسال /start ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "👋 أهلاً بك في بوت الأفلام المتطور!\n\n"
        "استخدم الأزرار أدناه للتنقل، أو اكتب اسم الفيلم في البحث."
    )
    await message.reply(welcome_text, reply_markup=main_menu_keyboard())

# --- ميزة البحث المباشر (Inline Query) ---
@dp.inline_handler()
async def search_movies(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    
    # قائمة تجريبية للأفلام (يفضل ربطها بقاعدة بيانات لاحقاً)
    movies_db = [
        {"id": "1", "title": "Inception", "link": "https://t.me/your_channel/1"},
        {"id": "2", "title": "Interstellar", "link": "https://t.me/your_channel/2"},
        {"id": "3", "title": "The Dark Knight", "link": "https://t.me/your_channel/3"},
    ]

    results = []
    for movie in movies_db:
        if query in movie['title'].lower():
            results.append(
                types.InlineQueryResultArticle(
                    id=movie['id'],
                    title=movie['title'],
                    input_message_content=types.InputTextMessageContent(
                        f"🎬 **الفيلم:** {movie['title']}\n🔗 **الرابط:** {movie['link']}",
                        parse_mode="Markdown"
                    ),
                    description="اضغط للإرسال"
                )
            )
    
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
