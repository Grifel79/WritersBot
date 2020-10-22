# %%
import os, random
from telegram.ext import Updater, PicklePersistence
import logging
from telegram.ext import CommandHandler
import docx
import textwrap
import requests
import re

def getText(filename):
    doc = docx.Document("stories/" + filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

PORT = int(os.environ.get('PORT', 5000))
TOKEN = '1359274306:AAHWYfzgsD3Q6v8HD7wdedqc535M65asjPQ'


# %%
# выгружаем статьи
url = 'https://api.discours.io/api/v2/content-links'
response = requests.get(
    url,
    params={'limit': 100},
)
str_all = response.content.decode("utf-8")
result = re.findall(r'".+"', str_all)
result_new = []
for i in range(len(result)):
    str_ = result[i][1:-1]
    if str_[0:5] == 'https':
        result_new.append(str_)

# %%
hello = """ Привет! Я чат бот, который познакомит тебя с офигительными статьями Дискурса. Нажми start, чтобы получить 
случайную статью
"""
def start(update, context):
    #lines = open('list.txt').read().splitlines()
    lines = result_new
    story_link = random.choice(lines)
    context.bot.send_message(chat_id=update.effective_chat.id, text=story_link)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Хочешь другую статью? Жми: /start')

def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=hello)

my_persistence = PicklePersistence(filename='persistence_file')
updater = Updater(token=TOKEN, persistence=my_persistence, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)