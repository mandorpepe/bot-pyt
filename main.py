from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import URLInputFile
from yandex_music import Client

import random
import config

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = config.BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

client = Client('y0_AgAAAAAhthTgAAG8XgAAAAD--2rKAAAATeO76FVHHaRpEhTi_HgrkNBYQw').init()

# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут расписание!\n' +
                         'Напиши мне что-нибудь и я отправю 1 песню фонка')


# Этот хэндлер будет срабатывать на команду "/help "
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе фонк'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
# Будет отправлять мой 1 трек из лайкнутых
async def send_track(message: Message):
    listOfMusic = client.users_likes_tracks()[random.randrange(0,13)].fetch_track().getDownloadInfo(get_direct_links=True)
    linkForDownload = listOfMusic[0].get_direct_link()
    print('принято')
    audio = URLInputFile(linkForDownload,filename="test")
    await message.reply_audio(audio)

# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_track)

if __name__ == '__main__':
    dp.run_polling(bot)