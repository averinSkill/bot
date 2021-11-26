import telebot
from config import TOKEN, keys
from extensions import APIException, Converter



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате: \
               \n<имя валюты> <в какую перевести> <количество>\
               \nУвидеть список доступных валют: /values'
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
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера. Не удалось обработать команду\n{e}')
    else:
        text = f'Сумма конвертации {amount} {quote} в {base} - {str(total_base)} {keys[base]}'
        bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['new_chat_members', ])
def greeting(message: telebot.types.Message):
    print("New member", message.chat.id)
    bot.send_message(message.chat.id, text='Хэлло, хэллоу!')


# # bot.polling(none_stop=True)
if __name__ == '__main__':
    bot.polling(none_stop=True)