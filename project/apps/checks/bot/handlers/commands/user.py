from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from apps.checks.bot.checks import Check
from apps.checks.misc import const


async def send_welcome(message: Message, bot: AsyncTeleBot):
    await bot.send_message(chat_id=message.chat.id,
                           text=const.TEXT_WELCOME)


async def handle_json_file(message: Message, bot: AsyncTeleBot):
    try:
        await bot.send_message(message.chat.id, "🗳 JSON получен, обработываю данные...")
        file_info = await bot.get_file(message.document.file_id)
        file = await bot.download_file(file_info.file_path)
        check = Check()
        rows, id_ = check.parse_json(file.decode('utf-8'))
    except Exception as ex:
        await bot.reply_to(message, f"❌ Ошибка при парсинге: {ex}")
    else:
        if not check.find_id(id_):
            try:
                check.write_to_sheet(rows)
            except Exception as ex:
                await bot.reply_to(message, f"❌ Ошибка при записи в файл: {ex}")
            else:
                await bot.reply_to(message, "✅ Данные успешно записаны в Google Sheets!")
        else:
            await bot.reply_to(message, "⛔ Чек уже внесен!")
