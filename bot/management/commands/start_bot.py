from django.core.management.base import BaseCommand

import telebot, requests
from telebot import types
import re
from core.models import User, Interest
from django.core.files.base import ContentFile
from map.settings import BOT_TOKEN

def start_bot():
    bot = telebot.TeleBot(BOT_TOKEN)
 
    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == "yes":
            bot.send_message(call.message.chat.id, 'Как тебя зовут?')
            bot.register_next_step_handler(call.message, get_name)

    def get_name(message):
        name = message.text
        user, created = User.objects.get_or_create(tg_id=message.chat.id, tg_username=message.chat.username)
        user.name = name
        user.save()
        bot.send_message(message.chat.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, get_age)

    def get_age(message):
        age = message.text
        user = User.objects.get(tg_id=message.chat.id)
        user.age = int(age)
        user.save()
        bot.send_message(message.chat.id, 'С какого ты факультета?')
        bot.register_next_step_handler(message, get_department)
    
    def get_department(message):
        department = message.text
        user = User.objects.get(tg_id=message.chat.id)
        user.department = department
        user.save()
        bot.send_message(message.chat.id, 'Расскажи о себе. Максимум 130 символов')
        bot.register_next_step_handler(message, get_bio)

    def get_bio(message):
        bio = message.text
        if len(bio) > 130:
            bot.send_message(message.chat.id, 'Слишком много символов')
            bot.register_next_step_handler(message, get_bio)
            return
        user = User.objects.get(tg_id=message.chat.id)
        user.bio = bio
        user.save()
        bot.send_message(message.chat.id, 'Отправь песню, которая тебе нравится')
        bot.register_next_step_handler(message, get_song)

    def get_song(message):
        name, artist = message.text.split('-')
        user = User.objects.get(tg_id=message.chat.id)
        song = Song.objects.create(name=name, artist=artist)
        user.song = song
        user.save()
        bot.send_message(message.chat.id, 'Отправь фотографию')
        bot.register_next_step_handler(message, get_photo)

    def get_photo(message):
        chat_id = message.chat.id

        file_id = message.photo[-1].file_id
        file_url = bot.get_file_url(file_id)

        response = requests.get(file_url)
        user = User.objects.get(tg_id=message.chat.id)
        user.photo.save(f'{user.tg_id}.jpg', ContentFile(response.content))
        user.save()
        bot.send_message(message.chat.id, 'Регистрация успешна')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Давай)', callback_data='yes')
        keyboard.add(key_yes)
        bot.send_message(message.chat.id, 'Привет! Это Map. Я задам тебе несколько вопросов, чтобы добавить тебя на карту, начнем?', reply_markup=keyboard)

    @bot.message_handler(commands=['edit'])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Давай)', callback_data='yes')
        keyboard.add(key_yes)
        bot.send_message(message.chat.id, 'Сейчас можно заполнить анкету заново', reply_markup=keyboard)

    @bot.message_handler(commands=['feedback'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Пиши сюда: @abakunov')

    @bot.message_handler(commands=['about'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Меня зовут Арсений, я здесь, чтобы сэкономить твое время и помочь найти работу мечты.\nТоже устал просматривать бесконечные списки вакансий? Просто укажи параметры вакансии и получай подборки сгенерированные искуственным интелектом.')

    bot.polling(none_stop=True, interval=0)

class Command(BaseCommand):
    help = 'Bot'

    def handle(self, *args, **options):
        start_bot()
        