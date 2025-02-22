import asyncio
import logging

from django.core.management.base import BaseCommand

from apps.checks.bot.main_bot import bot

logger = logging.getLogger(__name__)


async def start():
    await asyncio.gather(
        bot.infinity_polling(logger_level=logging.DEBUG)
    )


class Command(BaseCommand):
    help = "Запуск бота"

    def handle(self, *args, **options):
        asyncio.run(start())
