from django.core.management.base import BaseCommand

import telebot, requests
from telebot import types
import re
from core.models import Visitor
from map.settings import TEST_BOT_TOKEN

bot = telebot.TeleBot(TEST_BOT_TOKEN)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.startswith('/start '):
        arr = message.text.split(" ")
        if len(arr) > 1:
            inviter = arr[1]
            inviter = Visitor.objects.get(tg_id=int(inviter))
            visitor, created = Visitor.objects.get_or_create(tg_id=message.from_user.id, tg_username=message.from_user.username, who_invited=inviter)
            if created:
                visitor.save()
            
            if inviter == str(message.from_user.id):
                bot.send_message(message.from_user.id, "Отправь эту ссылку друзьям!")
                return

            bot.send_message(inviter, 'Кто-то зарегистрировался по твоей ссылке!')
            bot.send_message(message.from_user.id, "Привет! Чтобы получить доступ к приложению пригласи 2х друзей. Вот твоя ссылка: t.me/map_app_bot?start="+str(message.from_user.id))
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Чтобы получить доступ к приложению пригласи 2х друзей. Вот твоя ссылка: t.me/map_app_bot?start="+str(message.from_user.id))
        visitor, created = Visitor.objects.get_or_create(tg_id=message.from_user.id, tg_username=message.from_user.username)
        if created:
            visitor.save()
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю.")

bot.polling(none_stop=True, interval=0)