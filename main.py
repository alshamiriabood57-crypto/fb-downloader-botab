import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# استدعاء التوكن من إعدادات Render (Environment Variables)
API_TOKEN = os.getenv("BOT_TOKEN") 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- قائمة الأزرار الرئيسية (مثل الصورة) ---
def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # الزر الأول مخصص للبحث داخل البوت
    search_btn = InlineKeyboardButton("🔍 البحث في البوت", switch_inline_query_current_chat="")
    
    # بقية الأزرار لتنظيم التصنيفات
    btn_marvel = InlineKeyboardButton("مارفل", callback_data="marvel")
    btn_series = InlineKeyboardButton("المسلسلات", callback_data="series")
    btn_movies = InlineKeyboardButton("الافلام", callback_data="movies")
    btn_arabic = InlineKeyboardButton("افلام عربية", callback_data="arabic")
    btn_quotes = InlineKeyboardButton("قناة اقتباسات", url="https://t.me/your_channel") # ضع رابط قناتك هنا
    btn_featured = InlineKeyboardButton("🎬 أفلام مختارة", callback_data="featured")

    # ترتيب الأزرار في صفوف
    keyboard.add(search_btn)
    keyboard.row(btn_marvel, btn_series)
    keyboard.row(btn_movies, btn_arabic)
    keyboard.add(btn_quotes)
    keyboard.add(btn_featured)
    
    return keyboard

# --- الرد على أمر /start ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "🎬 **أهلاً بك في بوت الأفلام والمسلسلات!**\n\n"
        "يمكنك البحث عن أي فيلم مباشرة بالضغط على الزر أدناه أو اختيار التصنيف المناسب لك."
    )
    await message.reply(welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# --- محرك البحث (البحث الفوري) ---
@dp.inline_handler()
async def search_movies(inline_query: types.InlineQuery):
    query = inline_query.query.lower()
    
    # قاعدة بيانات تجريبية (يمكنك إضافة أفلامك هنا)
    movies_db = [
        {"id": "1", "title": "Inception", "link": "https://t.me/share/1"},
        {"id": "2", "title": "Interstellar", "link": "https://t.me/share/2"},
        {"id": "3", "title": "The Dark Knight", "link": "https://t.me/share/3"},
        {"id": "4", "title": "Inception 2", "link": "https://t.me/share/4"},
    ]

    results = []
    for movie in movies_db:
        # إذا كانت الكلمة التي كتبها المستخدم موجودة في اسم الفيلم
        if query in movie['title'].lower():
            results.append(
                types.InlineQueryResultArticle(
                    id=movie['id'],
                    title=movie['title'],
                    input_message_content=types.InputTextMessageContent(
                        f"🎬 **الفيلم:** {movie['title']}\n🔗 **الرابط:** {movie['link']}",
                        parse_mode="Markdown"
                    ),
                    description="اضغط هنا لإرسال رابط الفيلم"
                )
            )
    
    # عرض النتائج (حتى 50 نتيجة)
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
