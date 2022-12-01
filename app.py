import telebot
from config import TOKEN, currencies
from extensions import Exchange, ExchangeException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def handler_start(message: telebot.types.Message):
    text = 'Здравствуйте!\n' \
           'Я бот-конвертер валют и я могу:\n' \
           'Вывести список всех доступных валют при применении команды /values ;\n' \
           'Осуществить конвертацию валюты при вводе в строке ввода команды в следующем формате:\n' \
           '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>;\n' \
           'Напомнить мои возможности при применении команды /help'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['help'])
def handler_help(message: telebot.types.Message):
    text = 'Что бы начать работу с ботом введите в строке ввода команду в следующем формате:\n' \
           '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
           'Что бы вывести список всех доступных валют примените команду /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def handler_values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for currency in currencies.keys():
        text = '\n'.join((text, currency,))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ExchangeException('Введено неверное количество параметров. Пожалуйста, введите команду или 3 параметра')

        base, quote, amount = values
        total_base = Exchange.get_price(base, quote, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так.\n{e}')
    else:
        answer = (total_base * int(amount))
        text = f'Переводим {base} в {quote}\n{amount} {base} = {answer} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop = True)
