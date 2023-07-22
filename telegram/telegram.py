import telebot
import Tokens
import req
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = Tokens.telegramToken
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Получить посты из vk', callback_data='read_public_name'))
    keyboard.add(InlineKeyboardButton('отмена', callback_data='cancel'))
    bot.send_message(message.chat.id, 'Этот бот предназначен для быстрого доступа к записям сообщества вконтакте', reply_markup=keyboard)


@bot.message_handler()
def cancel(message):
    if message.text == 'отмена':
        bot.send_message(message.chat.id, 'Введите команду /start чтобы начать заново')


@bot.callback_query_handler(func = lambda call: True)
def working_logic(call):
    lst = []
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('отмена'))
    if call.data == 'read_public_name':

        msg = bot.send_message(call.message.chat.id, 'Введите ссылку на группу',
                         reply_markup=keyboard)

        bot.register_next_step_handler(msg, ask_count, lst)
    else:
        bot.send_message(call.message.chat.id, 'Введите команду /start чтобы начать заново')



def ask_count(message, lst):
    if message.text != 'отмена':
        lst.append(message.text.split('/')[-1])
        try:
            bot.send_message(message.chat.id, f'Колличество записей в группе - {req.wall_get(lst[0], 0, 0)["response"]["count"]}')

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton('отмена'))
            msg = bot.send_message(message.chat.id,
                                   'Введите колличество записей, которое хотите получить, максимум 100',
                                   reply_markup=keyboard)

            bot.register_next_step_handler(msg, ask_offset, lst)
        except:
            bot.send_message(message.chat.id, f'Кажется такой группы не существует либо 1 из сервисов - vk или telegram испытывает проблеммы \n Введите команду /start чтобы начать заново')

    else:
        bot.send_message(message.chat.id, 'Введите команду /start чтобы начать заново')


def ask_offset(message, lst):
    if message.text != 'отмена':
        lst.append(message.text)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('отмена'))

        msg = bot.send_message(message.chat.id, 'Введите отступ от первой записи',
                             reply_markup=keyboard)




        bot.register_next_step_handler(msg, result, lst)
    else:
        bot.send_message(message.chat.id, 'Введите команду /start чтобы начать заново')


def result(message, lst):
    if message.text != 'отмена':
        lst.append(message.text)
        content = req.wall_get(*lst)["response"]["items"]
        for item in content:
            try:
                media_list = []
                if 'attachments' in item and item['attachments'] != []:
                    for media in item['attachments']:
                        if media['type'] == 'photo':
                            media_list.append(media['photo']['sizes'][-1]['url'])

                    if len(media_list) > 1:
                        media_input = list(map(lambda x: telebot.types.InputMediaPhoto(x), media_list))
                        if 'text' in item and item['text'] != None:
                            media_input[0].caption = item['text']
                            bot.send_media_group(message.chat.id, media_input)
                        else:
                            bot.send_media_group(message.chat.id, media_input)

                    elif len(media_list) == 0:
                        if 'text' in item and item['text'] != None:
                            bot.send_message(message.chat.id, f'Данный пост скорее всего содержал видеозапись, доступ к которой нам не удалось получить. \n Текст поста: \n {item["text"]}')
                        else:
                            bot.send_message(message.chat.id,
                                             f'Пост содержит только видеозапись, в данный момент наш бот не может получать видеозаписи')

                    elif len(media_list) == 1:
                        if 'text' in item and item['text'] != None:
                            bot.send_photo(message.chat.id, media_list[0], caption=item['text'])
                        else:
                            bot.send_photo(message.chat.id, media_list[0])

                elif 'text' in item:
                    bot.send_message(message.chat.id, item['text'])

            except Exception as ex:
                print(ex)

    else:
        bot.send_message(message.chat.id, 'Введите команду /start чтобы начать заново')



bot.infinity_polling()