import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# Bot tokenni shu yerga yozing (Tokenni to'g'ri va bo'sh joysiz yozing!)
BOT_TOKEN = "7669259973:AAGYMKI8EF39FGA33R-His_gENKcoMWVH54"

# Adminlar ro'yxati (Telegram ID raqamlarini vergul bilan ajrating)
ADMINS = [7752032178, ]

# Adminlar bilan bog'lanish ma'lumotlari
ADMIN_CONTACTS = (
    "📞 Telefon: +998 94 089 81 19\n"
    "💬 Telegram: @sardorbeksobirjonov"
)

# Foydalanuvchilar IDlarini saqlash uchun set
users = set()

# /start komandasi
async def start_handler(message: Message):
    await message.answer(
        "👋 Salom!\n\n"
        "🛍 Kerakli mahsulot yoki xizmat nomini yozing.\n"
        "📨 Biz uni administratorlarga yetkazamiz va ular siz bilan tez orada bog‘lanadi.\n\n"
        "✏️ Masalan: Logo, Dizayn, Telegram bot va h.k."
    )

# Foydalanuvchidan kelgan xabarni adminlarga yuborish
async def user_message_handler(message: Message, bot: Bot):
    users.add(message.from_user.id)

    user_info = (
        f"💬 <b>Yangi so‘rov:</b>\n\n"
        f"👤 Foydalanuvchi: "
        f"{'@' + message.from_user.username if message.from_user.username else f'id: <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.id}</a>'}\n"
        f"📩 Xabar: <i>{message.text}</i>"
    )

    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, user_info, parse_mode=ParseMode.HTML)
        except Exception as e:
            logging.warning(f"Adminlarga xabar yuborishda xatolik: {e}")

    await message.answer(
        f"✅ So‘rovingiz qabul qilindi!\n\n"
        f"<b>Adminlar bilan bog‘lanish:</b>\n{ADMIN_CONTACTS}",
        parse_mode=ParseMode.HTML
    )

# /panel komandasi - adminlarga foydalanuvchilar ro'yxati
async def panel_handler(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("🚫 Bu buyruq faqat adminlar uchun!")
        return

    if not users:
        await message.answer("👥 Hozircha foydalanuvchi yo‘q.")
        return

    user_list = "\n".join([f"• <a href='tg://user?id={uid}'>{uid}</a>" for uid in users])
    await message.answer(
        f"👥 Botdan foydalanganlar soni: {len(users)}\n\n"
        f"Foydalanuvchilar ro‘yxati:\n{user_list}",
        parse_mode=ParseMode.HTML
    )

# /reklama komandasi - adminlardan reklama matnini olib, barcha foydalanuvchilarga yuborish
async def reklama_handler(message: Message, bot: Bot):
    if message.from_user.id not in ADMINS:
        await message.answer("🚫 Bu buyruq faqat adminlar uchun!")
        return

    reklama_matni = message.text.partition(" ")[2].strip()
    if not reklama_matni:
        await message.answer("❗️ Reklama matnini /reklama so‘zgacha yozing.\nMasalan:\n/reklama Yangi xizmatlarimiz bor!")
        return

    sent_count = 0
    failed_count = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, f"📢 Reklama xabari:\n\n{reklama_matni}")
            sent_count += 1
        except Exception:
            failed_count += 1

    await message.answer(f"📤 Reklama xabari {sent_count} foydalanuvchiga yuborildi.\n❌ Muvaffaqiyatsizlar: {failed_count}")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command(commands=["start"]))
    dp.message.register(panel_handler, Command(commands=["panel"]))
    dp.message.register(reklama_handler, Command(commands=["reklama"]))
    # So'nggi qoida: barcha boshqa xabarlar user_message_handlerga tushadi
    dp.message.register(user_message_handler)

    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
