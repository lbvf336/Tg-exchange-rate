import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
from datetime import datetime

# Токен для доступа к боту, который вы получите у @BotFather в Telegram
TOKEN = 'TOKEN'

# Ссылка на API Центрального Банка России для получения курса валют
API_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'

# Функция для получения актуального курса валют
def get_currency_rates():
    response = requests.get(API_URL)
    data = json.loads(response.content)
    return data['Valute']

# Функция для получения курса выбранной валюты
def get_currency_rate(currency):
    rates = get_currency_rates()
    if currency == 'usd':
        return rates['USD']['Value']
    elif currency == 'eur':
        return rates['EUR']['Value']
    elif currency == 'cny':
        return rates['CNY']['Value']
    elif currency == 'byn':
        return rates['BYN']['Value']
    else:
        return None

# Функция-обработчик команды /start
def start(update, context):
    now = datetime.now()
    current_time = now.strftime("%d.%m.%Y %H:%M:%S")
    message = f'Привет! Я бот для перевода рублей по актуальному курсу в доллары, евро, китайский юань и белорусский рубль.\nКурс обновлен {current_time}.\nВыберите валюту:'
    keyboard = [
        [telegram.KeyboardButton('USD', callback_data='USD'), telegram.KeyboardButton('EUR', callback_data='EUR')],
        [telegram.KeyboardButton('CNY', callback_data='CNY'), telegram.KeyboardButton('BYN', callback_data='BYN')],
        [telegram.KeyboardButton('О боте', callback_data='about')],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.user_data['current_time'] = current_time
    update.message.reply_text(message, reply_markup=reply_markup)
    
# Функция-обработчик сообщений
def start(update, context):
    now = datetime.now()
    current_time = now.strftime("%d.%m.%Y %H:%M:%S")
    message = f'Привет! Я бот для перевода рублей по актуальному курсу в доллары, евро, китайский юань и белорусский рубль.\nКурс обновлен {current_time}.\nВыберите валюту:'
    keyboard = [
        [telegram.KeyboardButton('USD'), telegram.KeyboardButton('EUR')],
        [telegram.KeyboardButton('CNY'), telegram.KeyboardButton('BYN')],
        [telegram.KeyboardButton('О боте')],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)
     
def echo(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    if text == 'USD' or text == 'EUR' or text == 'CNY' or text == 'BYN':
        rate = get_currency_rate(text.lower())
        if rate:
            message = f'Курс {text}: {rate:.2f} руб.\nВведите количество рублей, которые нужно перевести:'
            context.user_data['currency'] = text.lower()
            update.message.reply_text(message)
        else:
            update.message.reply_text('К сожалению, я не могу получить курс этой валюты. Попробуйте позже.')
    elif text.isdigit() and 'currency' in context.user_data:
        amount = int(text)
        rate = get_currency_rate(context.user_data['currency'])
        result = amount / rate
        message = f'{amount} руб. = {result:.2f} {context.user_data["currency"].upper()}'
        update.message.reply_text(message)
    elif text == 'О боте':
        update.message.reply_text('Этот бот предназначен для перевода рублей по актуальному курсу в доллары, евро, китайский юань и белорусский рубль.')
    else:
        update.message.reply_text('Я не понимаю, что вы хотите. Пожалуйста, выберите валюту из списка.')

# Создаем объект бота
bot = telegram.Bot(token=TOKEN)

# Создаем обновление
updater = Updater(token=TOKEN, use_context=True)

# Создаем обработчики команд и сообщений
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

# Добавляем обработчики в диспетчер
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(echo_handler)

# Запускаем бота
updater.start_polling()
updater.idle()

