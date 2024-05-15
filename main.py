from aiogram import Bot, Dispatcher, F
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
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

# Кнопки в боте
button_1 = KeyboardButton(text='Помощь')

# Создание кнопок
keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1]],
    resize_keyboard=True,
    one_time_keyboard=True
    )

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Бот Артёма!\n' +
                         'Этот бот поможет скачать песню с Яндекс Музыки',
                         reply_markup=keyboard
                         )
    


# Этот хэндлер будет срабатывать на команду "Помощь"
@dp.message(F.text == 'Помощь')
async def process_help_command(message: Message):
    await message.answer(
        'Отправьте название песни, которую вы хотите скачать и бот отправим вам аудио файл'
    )


# Этот хэндлер будет срабатывать на любые текстовые сообщения
# кроме команд "/start" и "Помощь"
# Будет отправлять песню по тексту сообщения

async def find_track(message: Message):
    # Поиск трека с использованием API яндекс музыки
    search_result = client.search(message.text,playlist_in_best=False)
    try:
        best = search_result.best.result.get_download_info(get_direct_links=True)
        # Информация о треке и ссылка на скачивание песни
        audio_name = search_result.best.result.title
        audio_author = search_result.best.result.artists[0].name
        linkForDownload = best[0].get_direct_link()
        print(audio_author + " " + audio_name)
        # Загрузка трека на сервера телеграм и отправка в боте
        audio = URLInputFile(linkForDownload,filename=audio_name + " - " + audio_author)
        await message.reply_audio(audio)
    except AttributeError:
        await message.reply("Результатов не было найдено, пожалуйста попробуйте чтото другое")





# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='Помощь'))
dp.message.register(find_track)

if __name__ == '__main__':
    dp.run_polling(bot)