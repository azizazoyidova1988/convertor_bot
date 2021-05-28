from convertor import Convertor
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, \
    CallbackContext, MessageHandler, Filters, CallbackQueryHandler

exchange = Convertor()
convertor_dict = {
    '1': 'USD',
    '2': 'RUB',
    '3': 'EUR',
    '1_1': 'UZS_USD',
    '2_2': 'UZS_RUB',
    '3_3': 'UZS_EUR'
}


def start(update: Update, context: CallbackContext):
    language_button = [
        [KeyboardButton("O'zbek tili"), KeyboardButton('Rus tili')]
    ]
    update.message.reply_text('Assalomu aleykum!!! \n Tilni tanlang:',
                              reply_markup=ReplyKeyboardMarkup(language_button, resize_keyboard=True))
    # context.bot.send_photo(chat_id='-1001369173362', photo=open('rasm.jpg.', 'rb'))
    return 1


def main_menu(update: Update, context: CallbackContext):
    convertor_button = [
        [
            InlineKeyboardButton('USD 🔄 UZS', callback_data='1'),
            InlineKeyboardButton('RUB 🔄 UZS', callback_data='2'),
            InlineKeyboardButton('EUR 🔄 UZS', callback_data='3')
        ],
        [
            InlineKeyboardButton('UZS 🔄 USD', callback_data='1_1'),
            InlineKeyboardButton('UZS 🔄 RUB', callback_data='2_2'),
            InlineKeyboardButton('UZS 🔄 EUR', callback_data='3_3')
        ]
    ]
    user = update.message.from_user
    # update.message.reply_text('Asosiy menu', reply_markup=ReplyKeyboardRemove())
    update.message.reply_photo(photo=open('rasm.jpg.', 'rb'),
                               caption='Siz valyutalar kursi haqida malumot olasiz.\n Keraklisini tanlang.',
                               reply_markup=InlineKeyboardMarkup(convertor_button))
    return 2


def inline_button(update: Update, context: CallbackContext):
    button_back = [
        [InlineKeyboardButton('↩ Go Back', callback_data='0')],
        [InlineKeyboardButton("Convertatsiyaga o'tish", callback_data='4')]

    ]
    query = update.callback_query
    data = query.data

    for i, j in convertor_dict.items():
        if int(i) == int(data) and int(len(i)) == 1:
            button_back = [
                [InlineKeyboardButton('↩ Go Back', callback_data='0')],
                [InlineKeyboardButton("Convertatsiyaga o'tish", callback_data='4')]
            ]
            query.message.delete()
            info = exchange.getData(j)
            query.message.reply_text(f"1 {info['Ccy']}= {info['Rate']} so'm  ",
                                     reply_markup=InlineKeyboardMarkup(button_back))

            with open('infos.txt', 'w') as f:
                f.write(f"{info['Ccy']}-{info['Rate']}")

        elif int(i) == int(data):
            j = j.split('_')
            button_back = [
                [InlineKeyboardButton('↩ Go Back', callback_data='0')],
                [InlineKeyboardButton("Convertatsiyaga o'tish", callback_data='4')]
            ]
            query.message.delete()
            info = exchange.getData(j[1])
            query.message.reply_text(f"1 so'm = {1 / float(info['Rate'])} ",
                                     reply_markup=InlineKeyboardMarkup(button_back))

            with open('infos.txt', 'w') as f:
                f.write(f"{info['Ccy']}-{1 / float(info['Rate'])}")

    if data == '0':
        query.message.delete()
        return main_menu(query, context)

    elif data == '4':
        query.message.delete()
        query.message.reply_text("Sonni kiriting: ")

        return 3


def convertor(update: Update, context: CallbackContext):
    button_main = [
        [KeyboardButton('Main menu')]
    ]
    number = update.message.text
    if number.isdigit():
        number = float(number)
        with open('infos.txt', 'r') as f:
            info = f.read()
        info = info.split('-')
        s = float(info[1]) * float(number)
        update.message.reply_text(f"{number} === {s} ",
                                  reply_markup=ReplyKeyboardMarkup(button_main, resize_keyboard=True))
    elif number == 'Main menu':
        update.message.delete()
        return main_menu(update, context)


def main():
    token = "1542491519:AAFEazocWUU-3X0xMt4cALD4gtzsGYuMhSY"
    updater = Updater(token)
    all_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      MessageHandler(Filters.regex('^(Main menu)$'), main_menu)
                      ],

        states={
            1: [MessageHandler(Filters.regex("^(O'zbek tili)$"), main_menu)],
            2: [CallbackQueryHandler(inline_button)],
            3: [MessageHandler(Filters.text, convertor)]

        },
        fallbacks=[]
    )
    updater.dispatcher.add_handler(all_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
