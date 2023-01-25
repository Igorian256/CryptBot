import telebot
from config import keys, TOKEN
from extentions import APIExeption, CriptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Комманды боту писать в следующем формате (через пробел):\n<имя валюты, цену которой хотите узнать> \
<в какую валюту перевести> <количество первой валюты>\n<увидеть список всех доступных валют:/values\n Например: биткоин доллар 1'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIExeption("Количество параметров должно быть равно 3(трём) значениям. Введите 3 параметра.")

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        total_base = float(total_base) * float(amount)
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()