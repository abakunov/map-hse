from django.core.management.base import BaseCommand

import telebot, requests
from telebot import types
import re
from core.models import User, Interest, Song, Location
from django.core.files.base import ContentFile
from map.settings import BOT_TOKEN
from .templates import *

def start_bot():
    bot = telebot.TeleBot(BOT_TOKEN)
 
    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == "yes":
            bot.send_message(call.message.chat.id, 'Как тебя зовут?')
            bot.register_next_step_handler(call.message, get_name)
        # if call.data == "skip-song":
        #     keyboard = types.InlineKeyboardMarkup()
        #     key_skip = types.InlineKeyboardButton(text='Пропустить', callback_data='skip-photo')
        #     keyboard.add(key_skip)
        #     bot.send_message(call.message.chat.id, ask_photo, reply_markup=keyboard)
        #     bot.send_photo(call.message.chat.id, photo=open('bot/management/commands/ask_photo.jpg', 'rb'))
        #     bot.register_next_step_handler(call.message, get_photo)
        # if call.data == "skip-photo":
        #     bot.register_next_step_handler(call.message, finish_reg)

    def get_name(message):
        name = message.text
        try:
            user, created = User.objects.get_or_create(tg_id=message.chat.id, tg_username=message.chat.username)
            user.name = name
            user.save()
        except:
            bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуй еще раз')
            bot.register_next_step_handler(message, get_name)
            return
        bot.send_message(message.chat.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, get_age)

    def get_age(message):
        age = message.text
        try:
            user = User.objects.get(tg_id=message.chat.id)
            user.age = int(age)
            user.save()
        except:
            bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуй еще раз')
            bot.register_next_step_handler(message, get_age)
            return
        bot.send_message(message.chat.id, 'Напиши свой факультет или направление')
        bot.register_next_step_handler(message, get_department)
    
    def get_department(message):
        department = message.text
        try:
            user = User.objects.get(tg_id=message.chat.id)
            user.department = department
            user.save()
        except:
            bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуй еще раз')
            bot.register_next_step_handler(message, get_department)
            return
        bot.send_message(message.chat.id, ask_for_bio)
        bot.register_next_step_handler(message, get_bio)

    def get_bio(message):
        bio = message.text
        if len(bio) > 130:
            bot.send_message(message.chat.id, 'Слишком много символов')
            bot.register_next_step_handler(message, get_bio)
            return
        try:
            user = User.objects.get(tg_id=message.chat.id)
            user.bio = bio
            user.save()
        except:
            bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуй еще раз')
            bot.register_next_step_handler(message, get_bio)
            return
        # keyboard = types.InlineKeyboardMarkup()
        # key_skip = types.InlineKeyboardButton(text='Пропустить', callback_data='skip-song')
        # keyboard.add(key_skip)
        bot.send_message(message.chat.id, ask_song)
        bot.register_next_step_handler(message, get_song)

    def get_song(message):
        try:
            artist, name = message.text.split('-')
            atrist = artist.strip().lower()
            name = name.strip().lower()
            user = User.objects.get(tg_id=message.chat.id)
            song = Song(name=name, artist=artist).save()
            user.song = Song.objects.filter(name=name, artist=artist)[0]
            user.save()
        except:
            bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуй еще раз')
            bot.register_next_step_handler(message, get_song)
            return
        # keyboard = types.InlineKeyboardMarkup()
        # key_skip = types.InlineKeyboardButton(text='Пропустить', callback_data='skip-photo')
        # keyboard.add(key_skip)
        bot.send_message(message.chat.id, ask_photo)
        bot.send_photo(message.chat.id, photo=open('bot/management/commands/ask_photo.jpg', 'rb'))
        bot.register_next_step_handler(message, get_photo)

    def get_photo(message):
        chat_id = message.chat.id
        try:
            file_id = message.photo[-1].file_id
            file_url = bot.get_file_url(file_id)
            response = requests.get(file_url)
            user = User.objects.get(tg_id=message.chat.id)
            user.photo.save(f'{user.tg_id}.jpg', ContentFile(response.content))
            user.save()
        except:
            bot.send_message(message.chat.id, 'Неправильный формат ввода, попробуй еще раз')
            bot.register_next_step_handler(message, get_photo)
            return
        bot.send_message(message.chat.id, reg_finish)

    def finish_reg(message):
        bot.send_message(message.chat.id, reg_finish)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, intro)
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Окей', callback_data='yes')
        keyboard.add(key_yes)
        bot.send_message(message.chat.id, start_reg, reply_markup=keyboard)

    @bot.message_handler(commands=['edit'])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Давай', callback_data='yes')
        keyboard.add(key_yes)
        bot.send_message(message.chat.id, 'Сейчас можно заполнить анкету заново', reply_markup=keyboard)

    @bot.message_handler(commands=['feedback'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Пиши сюда: @abakunov')

    @bot.message_handler(commands=['about'])
    def start_message(message):
        bot.send_message(message.chat.id, intro)

    bot.polling(none_stop=True, interval=0)

class Command(BaseCommand):
    help = 'Bot'

    def handle(self, *args, **options):
        start_bot()
        