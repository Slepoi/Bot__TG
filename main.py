import telebot
import requests
import uuid
import os
import soundfile as sf
import speech_recognition as sr
from telebot import types

bot = telebot.TeleBot("6392011247:AAEScim2l0D0j7vYCyFcIQH8s_fmLDpCNA4")

language='ru_RU'
#CHAT_ID='-100xxxxxxxxxxxxxxxxxxxxx')
r = sr.Recognizer()

def recognise(filename):
  with sr.AudioFile(filename) as source:
      audio_text = r.listen(source)
      try:
          text = r.recognize_google(audio_text,language=language)
          print('Преобразование аудиозаписей в текст ...')
          print(text)
          return text
      except:
          print('Сорри.. Попробуйте попозже...')
          return "Сорри.. Попробуйте попозже..."

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    if os.path.exists(file_name_full_converted):  # Check if the file exists
        text = recognise(file_name_full_converted)
        bot.reply_to(message, text)
        os.remove(file_name_full)  # переместили удаление файла сюда
        os.remove(file_name_full_converted)
    else:
        bot.reply_to(message, "Error: File not found")




@bot.message_handler(commands=["api"])
def get_janet_weaver_email(message):
    url = "https://reqres.in/api/users/2"
    response = requests.get(url)
    data = response.json()
    email = data['data']['email']
    bot.send_message(message.chat.id, email)

@bot.message_handler(commands=['calculator'])
def handle_text(message): 
    numvan = bot.send_message(message.chat.id, 'ведите 1 число') 
    bot.register_next_step_handler(numvan ,num1_fun)

def num1_fun(message):
   global num1
   num1 = message.text
   numtwo = bot.send_message(message.chat.id, 'ведите 2 число')
   bot.register_next_step_handler(numtwo ,num2_fun)

def num2_fun(message):
    global num2
    num2 = message.text      
    operu = bot.send_message(message.chat.id, 'ведите действие')
    bot.register_next_step_handler(operu ,operi)

def operi(message):
    global oper
    oper = message.text
    if oper == "+":
        resylit = int(num1)+int(num2)
        bot.send_message(message.chat.id,resylit)
    elif oper == "-":
        resylit = int(num1)-int(num2)
        bot.send_message(message.chat.id,resylit)
    elif oper == "*":
        resylit = int(num1)*int(num2)
        bot.send_message(message.chat.id,resylit)
    elif oper == "/": 
      if num1 and num2 == 0:
        resylit = int(num1)/int(num2)
        bot.send_message(message.chat.id,resylit)
      else:
        bot.send_message(message.chat.id,"Нельзя делить на 0")
    else:
        bot.send_message(message.chat.id,"ошибка ведите /start")
# Вывод всех кнопок
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Полезные ссылки")
    btn2 = types.KeyboardButton("Погода")
    btn3 = types.KeyboardButton("Пообщаться")
    btn4 = types.KeyboardButton("Ссылка на Гугл")
    btn7 = types.KeyboardButton("Закрыть!")
    btn8 = types.KeyboardButton("Api")
    markup.add(btn1, btn2, btn3, btn4, btn8, btn7)  # Добавление сущности кнопок
    bot.send_message(
        message.chat.id,
        "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, созданный чтобы помогать тебе. Пожалуйста, для начала, выберите категорию вашего вопроса (для управления ботом использвуте кнопки)".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
        reply_markup=markup,
    )
@bot.message_handler(content_types=["text"])
def func(message):
    if message.chat.type == "private":
        if message.text == "Полезные ссылки":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("КемГУ")
            btn2 = types.KeyboardButton("КузГТУ")
            btn3 = types.KeyboardButton("КемТИПП")
            btn4 = types.KeyboardButton("РЭУ")
            btn5 = types.KeyboardButton("Назад")
            btn7 = types.KeyboardButton("Закрыть!")
            markup.add(btn1, btn2, btn3, btn4, btn7, btn5)
            bot.send_message(
                message.chat.id, text="Вы выбрали полезные ссылки", reply_markup=markup
            )

        elif message.text == "КемГУ":
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("КемГУ", url="https://kemsu.ru")
            markup.add(button1)
            bot.send_message(
                message.chat.id,
                text="Ссылка на КемГУ".format(),
                reply_markup=markup,
            )
        elif message.text == "КузГТУ":
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("КузГТУ", url="https://kuzstu.ru")
            markup.add(button1)
            bot.send_message(
                message.chat.id,
                text="Ссылка на КемГУ".format(),
                reply_markup=markup,
            )
        elif message.text == "КемТИПП":
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                "КемТИПП",
                url="https://ru.wikipedia.org/wiki/Кемеровский_технологический_институт_пищевой_промышленности_КемГУ",
            )
            markup.add(button1)
            bot.send_message(
                message.chat.id,
                text="Ссылка на КемГУ".format(),
                reply_markup=markup,
            )
        elif message.text == "Ссылка на Гугл":
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                "Ссылка на Гугл",
                url="https://www.google.com",
            )
            markup.add(button1)
            bot.send_message(
                message.chat.id,
                text="Ссылка на Гугл".format(),
                reply_markup=markup,
            )
        elif message.text == "РЭУ":
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("РЭУ", url="https://рэу.рф")
            markup.add(button1)
            bot.send_message(
                message.chat.id,
                text="Ссылка на РЭУ".format(),
                reply_markup=markup,
            )
        elif message.text == "Закрыть!":
          bot.send_message(message.chat.id, "Используйте команду /start!", reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Назад":
            start(message)
          
        elif message.text == "Api":
            get_janet_weaver_email(message)
          
        elif message.text == "Погода":
          
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton("Погода")
            markup.add(btn2)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                "Гисметео", url="https://www.gismeteo.ru"
            )
            markup.add(button1)
            bot.send_message(
                message.chat.id,
                text="Ссылка на Гисметео".format(),
                reply_markup=markup,
            )

        if message.text == "Пообщаться":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Как меня зовут?")
            btn6 = types.KeyboardButton("Калькулятор")
            btn5 = types.KeyboardButton("Назад")
            markup.add(btn1, btn6, btn5)
            bot.send_message(
                message.chat.id, text="Вы выбрали пообщаться", reply_markup=markup
            )
        elif message.text == "Как меня зовут?":
            bot.send_message(
                message.chat.id,
                "Тебя зовут, {0.first_name}!".format(message.from_user, ),
                parse_mode="html",
            )
        elif message.text == "Калькулятор":
          handle_text(message)
bot.polling(none_stop=True)

