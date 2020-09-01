#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, random
from telegram.ext import Updater, PicklePersistence
import logging
from telegram.ext import CommandHandler
import docx
import textwrap

def getText(filename):
    doc = docx.Document("stories/" + filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

PORT = int(os.environ.get('PORT', 5000))
TOKEN = '1359274306:AAHWYfzgsD3Q6v8HD7wdedqc535M65asjPQ'

# """
# Привет! Вот текст молодого писателя:
#
# я впервые побывал в Калининграде – всегда было интересно узнать, что это за кусочек России в Европе между Литвой и Польшей. Женщина таксист, которая везла нас в первый вечер в Ельцин бар, рассказывала, что это был портовый город в советское время, и жизнь была спокойной и размеренной. Поколение ее родителей приехало в регион из разных мест советского союза. С тех пор многое изменилось, а жизнь стала вертеться вокруг денег, говорит она. На следующий день мы пообедали в кошерной столовой во дворе недавно построенной синагоги – старую нацисты разрушили в Хрустальную ночь 1938го года. Местный раввин рассказывал нам об интересных местах в городе, а рядом попрошайничал еду черный котик по кличке Сарочка. Странное ощущение от немецкого прошлого меня преследовало. В самом Калининграде - Кенигсберге, почти полностью разрушенном в Великую Отечественную, это не так заметно – разве что кафедральный готический собор с могилой Иммануила Канта. А в небольших городах региона, например Балтийск – крепость Пиллау 17го века, немецкая кирха и кирпичные домики уже не оставляют сомнений, что 75 лет назад здесь была Германия. Из Балтийска на пароме мы переправились на балтийскую косу, которую поляки называют Вислинской. Тут какой-то свой тихий и спокойный мир с песчаными пляжами и чистым звездным небом. Купаться в тех местах нельзя из-за опасных течений, зато мы смогли посерфить с ребятами из Konig surf club в Зеленоградске. До океана не дотягивает, но взять десяток хороших волн удалось. Отбившись от калининградских ментов, которым не понравились мои веселые московские глаза, я не поехал с ними сдавать кровь и мочу на наличие каннабиноидов. И так не пропустил закат в Донском, где мы потанцевали с ребятами из Route.Community у трассы – было красиво и весело. Если окажусь еще раз в Калиниграде, схожу в старый квартал Амалиенау, который рекомендовал нам чат бот в телеграм – наш digital проводник в поездке. И попробую познакомиться с калининградской молодежью, чтобы узнать, как они видят будущее своего региона и чем живут.
# """

hello = """ Привет! Я чат бот, который познакомит тебя с рассказами молодых писателей. Нажми start, чтобы получить 
случайный рассказ
"""

def start(update, context):
    # filename = random.choice(os.listdir('stories/'))
    # text = getText(filename)
    # parts = textwrap.wrap(text, width=4000, break_long_words=False)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=os.path.splitext(filename)[0])
    # for part in parts:
    #     context.bot.send_message(chat_id=update.effective_chat.id, text=part)
    lines = open('list.txt').read().splitlines()
    story_link = random.choice(lines)
    context.bot.send_message(chat_id=update.effective_chat.id, text=story_link)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Хочешь другой рассказ? Жми: /start')

def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=hello)

my_persistence = PicklePersistence(filename='persistence_file')
updater = Updater(token=TOKEN, persistence=my_persistence, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('https://arcane-brushlands-32559.herokuapp.com/' + TOKEN)
updater.idle()