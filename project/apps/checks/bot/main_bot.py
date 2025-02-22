import telebot
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings

from apps.checks.bot.filters.admin import AdminFilter
from apps.checks.bot.handlers.commands.user import (
    send_welcome,
    handle_json_file,
)

bot = AsyncTeleBot(
    settings.TELEGRAM_TOKEN,
    parse_mode='HTML'
)

telebot.logger.setLevel(settings.LOG_LEVEL)

# Обработчики сообщений
bot.register_message_handler(
    send_welcome, commands=['start'], pass_bot=True)

bot.register_message_handler(
    handle_json_file, content_types=['document'], pass_bot=True
)


# Фильтр для администраторов
bot.add_custom_filter(AdminFilter())
