import telebot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import filmsM
bot=telebot.TeleBot()

@bot.message_handler(commands=["start"])
def Start(msg):
    KB=InlineKeyboardMarkup()
    KB.add(InlineKeyboardButton("Help",callback_data="Help"))
    bot.send_message(msg.chat.id,"Привіт,Я Бот для пошуку філмів",reply_markup=KB)

@bot.message_handler(commands=["help"])
def Help(msg):
    KB=InlineKeyboardMarkup()
    KB.add(InlineKeyboardButton("films",callback_data="films"))
    bot.send_message(msg.chat.id,"Привіт,Я Бот для пошуку філмів",reply_markup=KB)



@bot.message_handler(commands=["film"])
def film(msg):
    KB=InlineKeyboardMarkup()
    films=[InlineKeyboardButton(film,callback_data=f"film:{film}")for film in filmsM.Biblioteka]
    KB.add(*films)
    bot.send_message(msg.chat.id,"Привіт,Я Бот для пошуку філмів",reply_markup=KB)



@bot.callback_query_handler(func=lambda call:True)

def Button(call):
    if call.data=="Help":
         KB=InlineKeyboardMarkup()
         KB.add(InlineKeyboardButton("films",callback_data="films"))
         bot.answer_callback_query(call.id)
         bot.send_message(call.message.chat.id,"Привіт,Я Бот для пошуку філмів",reply_markup=KB)
    elif call.data=="films":
         KB=InlineKeyboardMarkup()
         films=[InlineKeyboardButton(film,callback_data=f"film:{film}")for film in filmsM.Biblioteka]
         KB.add(*films)
         bot.answer_callback_query(call.id)
         bot.send_message(call.message.chat.id,"Привіт,Я Бот для пошуку філмів",reply_markup=KB)
    else:
        name=call.data.replace("film:","")
        if name in filmsM.Biblioteka:
            info=filmsM.Biblioteka[name]
            foto=info.get("Фото","")
            response = f"{name} ({info['Рік']})\nРежисер: {info['Режисер']}\nЖанр: {info['Жанр']}"
            if foto:
                bot.send_photo(call.message.chat.id,foto,caption=response)
            else:
                bot.send_message(call.message.chat.id,response)



@bot.message_handler(commands=['addfilm'])
def add(msg):
    bot.reply_to(msg,"Введіть назву фільму")
    bot.register_next_step_handler(msg,adddirector)

def adddirector(message):
    user_data={}
    user_data["name"]=message.text
    bot.reply_to(message, f"Введіть режисера фільму")
    bot.register_next_step_handler(message, add_year, user_data)
def add_year(message,user_data):
    user_data["director"]=message.text
    bot.reply_to(message, f"Введіть рік випуску фільму")
    bot.register_next_step_handler(message, add_genre, user_data)
def add_genre(message,user_data):
    user_data["year"]=message.text
    bot.reply_to(message, f"Введіть жанр фільму")
    bot.register_next_step_handler(message, add_photo, user_data)
def add_photo(message,user_data):
    user_data["genre"]=message.text
    bot.reply_to(message, f"Введіть посилання на фото фільму")
    bot.register_next_step_handler(message, add_save, user_data)
def add_save(message,user_data):
    filmsM.Biblioteka[user_data['name']]={
        'Режисер':user_data['director'],
        'Рік':user_data['year'],
        'Жанр':user_data['genre'],
        "Фото":message.text
    }
    bot.reply_to(message,"Філм додано до бібліотеки")





























bot.polling()