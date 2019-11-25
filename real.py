#Блок импорта
import telebot
import wikipedia
import random
import time, re
import time
import pyowm
import requests
# from mqtt import *
import datetime
#import reader
import os
from dotenv import load_dotenv
from queue import Queue
import codecs
import urllib.request
from bs4 import BeautifulSoup as bs
from parsing import *
#Блок токена
token = load_dotenv()
token = os.getenv('TOKEN')
#Блок такси
f = codecs.open( 'taxinumbers.txt', "r", "utf_8_sig" )
taxicities = f.read()
taxicities = taxicities.split('\r\n')[:-1]
taxidict = dict()
for i in taxicities:
    key = i[:i.index(';')]
    taxidict[key] = i[i.index(';') + 2:]
#Блок стикеров
commandlist = {'/advice' : 'advice_message(message)', '/wikipedia' : 'wikipedia_message(message)', '/wiki' : 'wikipedia_message(message)', '/start': 'start_message(message)', '/help' : 'help_message(message)', '/tickets' : 'tickets_message(message)', '/route' : 'tickets_message(message)', '/weather' : 'weather_message(message)', '/music' : 'music_message(message)', '/developers' : 'developers_message(message)', '/taxi' : 'taxi_message(message)', '/video' : 'video_message(message)'}
commandlist_ru = {'советы' : 'advice_message(message)', 'википедия' : 'wikipedia_message(message)', 'вики' : 'wikipedia_message(message)', 'старт': 'start_message(message)', 'помощь' : 'help_message(message)','билеты' : 'tickets_message(message)', 'маршрут' : 'tickets_message(message)', 'погода' : 'weather_message(message)', 'музыка' : 'music_message(message)', 'разработчики' : 'developers_message(message)', 'такси' : 'taxi_message(message)', 'видео' : 'video_message(message)'}
lovestickerpack = ['CAADAgAD2QADVp29CtGSZtLSYweoFgQ', 'CAADAgAD0gADVp29Cg4FcjZ1gzWKFgQ', 'CAADAgAD0wADVp29CvUyj5fVEvk9FgQ', 'CAADAgAD2AADVp29CokJ3b9L8RQnFgQ', 'CAADAgAD3gADVp29CqXvdzhVgxXEFgQ', 'CAADAgADFQADwDZPE81WpjthnmTnFgQ', 'CAADAgADBQADwDZPE_lqX5qCa011FgQ', 'CAADAgADDQADwDZPE6T54fTUeI1TFgQ', 'CAADAgADHQADwDZPE17YptxBPd5IFgQ', 'CAADAgAD4QcAAnlc4gndRsN-Tyzk1xYE', 'CAADAgAD3wcAAnlc4gmeYgfVO_CEsxYE', 'CAADAgAD4AcAAnlc4gmXqeueTbWXlRYE', ]
questionstickerpack = ['CAADAgAD4wADVp29Cg_4Isytpgs3FgQ', 'CAADAgADEgADwDZPEzO8ngEulQc3FgQ', 'CAADAgADEAADwDZPE-qBiinxHwLoFgQ', 'CAADAgADIAADwDZPE_QPK7o-X_TPFgQ', 'CAADAgAD2wcAAnlc4gkSqCLudDgLbhYE', 'CAADAgADzwcAAnlc4gnrZCnufdBTahYE', 'CAADAgAD2QcAAnlc4gn3Ww8qzk3S3BYE', 'CAADAgAD0gcAAnlc4gmLqZ82yF4OlxYE']
angrystickerpack = ['CAADAgAD3AADVp29Cpy9Gm5Tg192FgQ', 'CAADAgAD2wADVp29Clxn-p9taVttFgQ', 'CAADAgADywADVp29CllGpcs9gzQoFgQ']
loadstickerpack = ['CAADAgADGAADwDZPE9b6J7-cahj4FgQ', 'CAADAgAD1QADVp29CveXwRdcmk7nFgQ', 'CAADAgADwAADVp29Ct1dnTI9q-YvFgQ', 'CAADAgAD4QADVp29ClvBlItA-NOgFgQ', 'CAADAgAD5QADVp29CggLFmSVBdGKFgQ']
#Блок имен
developerslist = ['рустам', 'ярослав', 'владимир', 'даниэль', 'игорь']
nongratlist = ['арина', 'ариша', 'алия']
#Блок кнопок
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('такси', 'билеты', 'погода')
keyboard1.row('музыка', 'видео', 'вики')
keyboard1.row('советы', 'помощь')
keyboard1.row('старт', 'разработчики')
#Блок погоды
owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = 'ru, en')
bot = telebot.TeleBot(token)
#Блок переменных
fromplace_dict={}
toplace_dict={}
dateregistration_dict={}
video_search = ''
video_search_list = []
videos_for_dict={}
res = ''
status = ''
q = Queue()
#Блок для советов
@bot.message_handler(commands=['advice'])
def advice_message(message):
    bot.send_message(message.chat.id, 'Возможно вам понадобятся следущие вещи:')
    bot.send_message(message.chat.id, 'Документы:\nпаспорт: внутренний или загран; документы для ребенка: 1) паспорт, 2) свидетельство о рождении, 3) согласие на выезд из России, если ребенок едет за границу без родителей; наличные деньги; билеты на самолет, поезд, автобус; брони отелей; водительские права; копия паспорта; страховой полис путешественника')
    bot.send_message(message.chat.id, 'Техника и гаджеты в дорогу: \ncмартфон и зарядка; внешний жесткий диск; дорожный утюг; маленький электрический чайник; наушники; ноутбук и зарядка; переходник для розеток; плеер; тройник, удлинитель или сетевой фильтр; фен; фотоаппарат, зарядка, карты памяти, сумка для камеры; штатив, монопод, палка для селфи; электронная книга')
    bot.send_message(message.chat.id, 'Бытовые мелочи и комфорт в поездке: \nсумочка или городской рюкзак для прогулок; блокнот и ручка; вилка, ложка, тарелка, чашка; зонт; карманное зеркало; карта; книга, путеводитель, журнал; маска для сна, беруши, надувная подушка; обычные пакеты; полотенце; разговорник; солнечные очки; туалетная бумага; швейный набор; швейцарский армейский нож')
    bot.send_message(message.chat.id, 'Гигиена и косметика в поездку: \nбритва; дезодорант; зубная паста и щетка; расческа; ватные палочки, ватные диски; Влажные салфетки, бумажные платочки; гигиеническая помада, бальзам для губ; гигиенические прокладки, тампоны; дезинфицирующий гель для рук; зубная нить, зубочистки; крем от солнца; кремы для лица и тела; ножницы и пилочка для ногтей; очки или контактные линзы с контейнером и раствором; парфюм; пена для и после бритья; помада, тушь для ресниц и другая декоративная косметика, средство для снятия макияжа; презервативы; репеллент от комаров; средство для укладки волос; фумигатор; шампунь, кондиционер для волос, мыло, гель для душа, мочалка')
#
#Блок для Википедии
@bot.message_handler(commands=['wiki', 'wikipedia'])
def wikipedia_message(message):
    bot.send_message(message.chat.id, 'Введите место, информацию о котором хотели бы узнать')
    bot.register_next_step_handler(message, wikipedia_information)

def wikipedia_information(message):
    if message.text.lower() in commandlist:
            exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
            exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
            exec(commandlist['/' + message.text.lower()])
    else:
        try:
            global lovestickerpack
            wikipedia.set_lang('ru')
            wikipediamessage = wikipedia.summary(message.text.lower(), sentences=4)
            bot.send_message(message.chat.id, wikipediamessage)
        except:
            bot.send_message(message.chat.id, 'Такой статьи пока не существует, но вы в любой момент можете её создать')
            bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
    
#Блок команды для такси
@bot.message_handler(commands=['taxi'])
def taxi_message(message):
    bot.send_message(message.chat.id, 'Введите город, в котором вы хотели бы заказать такси')
    bot.register_next_step_handler(message, taxi_telephone_numbers_message)
    
def taxi_telephone_numbers_message(message):
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        global taxidict
        try:
            ttnumbers = taxidict[message.text.lower()]
            ttnumbers = ttnumbers.split('. ')
            ttnumbers = '\n'.join(ttnumbers)
            bot.send_message(message.chat.id, ttnumbers)
        except:
            global questionstickerpack
            bot.reply_to(message, 'Боюсь, что даже мистер Вульф не сможет туда приехать')
            bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
#Блок для разработчиков
@bot.message_handler(commands=['developers'])
def developers_message(message):
    bot.send_message(message.chat.id, 'Если у вас есть идеи по дальнейшему развитию нашего проекта:\nИгорь: https://vk.com/bayanovigor\nЯрослав: https://vk.com/yarik_tat\nВладимир: https://vk.com/ia_ifferus\nРустам: https://vk.com/rustknight7\nДаниэль: https://vk.com/sintirev')
#Блок для поиска билетов
@bot.message_handler(commands=['tickets', 'route'])
def tickets_message(message):
    bot.send_message(message.chat.id, 'Введите город отправления')
    bot.register_next_step_handler(message, fromplace_registration)
    
def fromplace_registration(message):
    global commandlist
    global fromplace_dict
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        fromplace_dict.update({str(message.chat.id):message.text.lower()})
        bot.send_message(message.chat.id, 'Введите город назначения')
        bot.register_next_step_handler(message, toplace_registration)
        
def toplace_registration(message):
    global commandlist
    global toplace_dict
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        toplace_dict.update({str(message.chat.id):message.text.lower()})
        bot.send_message(message.chat.id, 'Введите дату отправления')#rzd
        bot.register_next_step_handler(message, date_registration)
        
def date_registration(message):
    global commandlist
    global fromplace_dict
    global toplace_dict
    global dateregistration_dict
    global loadsticerpack
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        global lovestickerpack
        global q
        q.put([fromplace_dict[str(message.chat.id)],toplace_dict[str(message.chat.id)],dateregistration_dict[str(message.chat.id)],str(message.chat.id)])
        dateregistration_dict.update({str(message.chat.id):message.text.lower()})
        print(fromplace_dict[str(message.chat.id)])
        print(toplace_dict[str(message.chat.id)])
        print(dateregistration_dict[str(message.chat.id)])
        args=q.get()
        #Sendler(fromInput=fromplace_dict[str(message.chat.id)],fromOutput=toplace_dict[str(message.chat.id)],date=dateregistration_dict[str(message.chat.id)]).send()
        bot.send_message(message.chat.id, 'Ищу билеты по выбранному направлению')
        bot.send_sticker(message.chat.id, random.choice(loadstickerpack))
        fromplace = fromplace_dict[str(message.chat.id)]
        toplace = toplace_dict[str(message.chat.id)]
        response= Parsers(fromInput=args[0],fromOutput=args[1],date=args[2],user=args[3]).threader()
        res=response.split(":")
        if str(message.chat.id) in res[0]:
            bot.send_message(message.chat.id, 'Билеты по маршруту {0} - {1} на {2} '.format(fromplace[0].upper() + fromplace.lower()[1:], toplace[0].upper() + toplace.lower()[1:], dateregistration_dict[str(message.chat.id)]) + "\n" +  str( response[response.index(":"):]))      
            bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
            del fromplace_dict[str(message.chat.id)]
            del toplace_dict[str(message.chat.id)]
            del dateregistration_dict[str(message.chat.id)]
        else:
            bot.send_message(res[0], 'Билеты по маршруту {0} - {1} на {2} '.format(fromplace[0].upper() + fromplace.lower()[1:], toplace[0].upper() + toplace.lower()[1:], dateregistration_dict[str(message.chat.id)]) + "\n" +  str( response[response.index(":"):]))      
            bot.send_sticker(res[0], random.choice(lovestickerpack))
            del fromplace_dict[str(res[0])]
            del toplace_dict[str(res[0])]
            del dateregistration_dict[str(res[0])]
        
#Блок для команды старт
@bot.message_handler(commands=['start'])

def start_message(message):
    global weatherinformation
    global lovestickerpack
    bot.send_message(message.chat.id, 'Привет!\nМеня зовут Travellta !\nВот список моих функций :\n1./start\n2./help\n3./weather\n4./tickets, /route\n5./taxi\n6./music\n7./video\n8./wikipedia\n9./developers', reply_markup=keyboard1)
    bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
#Блок для погоды
@bot.message_handler(commands=['weather'])
def weather_message(message):
    bot.send_message(message.chat.id, 'Напишите город, погодные условия которого вы хотели бы узнать')
    bot.register_next_step_handler(message, weather_information)
    
def weather_information(message):
    place = ''
    global status
    global angrystickerpack
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        try:
            place = message.text.lower()
            observation = owm.weather_at_place(place)
            weather = observation.get_weather()
            status = weather.get_detailed_status()
            temp = weather.get_temperature('celsius')['temp']
            wind = weather.get_wind()['speed']
            print(weather)
            weathercity = message.text[0].upper() + message.text.lower()[1:]
            bot.send_message(message.chat.id, "Погода города/Weather: " + weathercity + "\nТемпература/Temperature: " + str(temp) + "°C" + "\nНа улице/On the street: " + str.title(status) + "\nСкорость Ветра/Wind speed: " + str(wind) + "м/c")
            if temp >= 15:
                bot.send_message(message.chat.id, "Погода-mood: Cамое-то ")
            elif 15 > temp  and temp > 0:
                bot.send_message(message.chat.id, "Погода-mood: Накинь что нибудь на себя ")
            elif temp < 0 and -25 < temp:
                bot.send_message(message.chat.id, "Погода-mood: Одевайся мать, пора воевать ")
            elif temp <= -25:
                bot.send_message(message.chat.id, "Погода-mood: Ты умрёшь, если уйдёшь")
        except:
            bot.reply_to(message, 'Врешь, такого города нет на картах')
            bot.send_sticker(message.chat.id, random.choice(angrystickerpack))
#Блок для помощи
@bot.message_handler(commands=['help'])
def help_message(message):
    global lovestickerpack
    bot.send_message(message.chat.id, '1./start("старт") - возвращает наш диалог к исходному состоянию\n2./weather("погода") - узнать погоду в любом городе мира\n3./tickets, /route("билеты", "маршрут") - узнать доступные на данный момент билеты\n4./taxi("такси") - узнать номера такси в выбранном городе\n5./music("музыка") - прослушать случайные треки, выбранные нашей командой\n6./video - найти видео по запросу\n7./wikipedia, /wiki("Википедия", "вики") - позволяет узнает краткую информационную сводку из Википедии\n8./developers("разработчики") - узнать контактные данные нашей команды')
    bot.send_sticker(message.chat.id,random.choice(lovestickerpack))
#Блок для музыки
@bot.message_handler(commands=['music'])
def music_message(message):
    bot.send_message(message.chat.id, 'Введите количество треков для прослушивания')
    bot.register_next_step_handler(message, playlist)
def playlist(message):
    if message.text.lower() in commandlist:
            exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        audiolist = []
        for i in range(int(message.text)):
            while True:
                n = random.randint(1,45)
                if n not in audiolist:
                    break
            audiolist.append(n)
            audio = open(str(n) + ".mp3", mode='rb')
            print("opened " + str(n) + ".mp3")
            bot.send_audio(message.from_user.id, audio, timeout=1000)
#Блок для видео
@bot.message_handler(commands=['video'])
def video_message(message):
    global video
    global video_search
    global video_search_list
    bot.send_message(message.chat.id, 'Введите ключевое слово для поиска видео')
    bot.register_next_step_handler(message, video_search)

def video_search(message):
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        try:
            video_search = message.text
            video_search_list = video_search.split()
            video_search = 'https://www.youtube.com/results?search_query='
            for i in range(len(video_search_list)):
                video_search += video_search_list[i]
                video_search += '+'
            video_search = video_search[:-1]
            html = requests.get(video_search).text
            soup = bs(html,'html.parser')
            count=0
            links = soup.find_all(attrs={'class':'yt-uix-tile-link'})
            links= [l['href'] for l in links]
            if ('channel' or 'user') not in links[0]:
                res = 'https://www.youtube.com/' + links[0]
            else:
                res = 'https://www.youtube.com/' + links[1]
            bot.send_message(message.chat.id, res)
        except:
            global questionstickerpack
            bot.send_message(message.chat.id, 'Видео, связанное с этой темой, пока не сняли')
            bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
#Блок для обработки текста
@bot.message_handler(content_types=['text'])
def text_analyze(message):
    global lovestickerpack
    global angrystickerpack
    global questionstickerpack
    if '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif message.text.lower() in developerslist:
        developername = message.text[0].upper() + message.text.lower()[1:]
        bot.reply_to(message, 'в моей системе рейтинга {0} стоит на первом месте'.format(developername))
        bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
    elif message.text.lower() in nongratlist:
        nongratname = message.text[0].upper() + message.text.lower()[1:]
        bot.reply_to(message, '{0}...{0}...звучит как что-то неприятное'.format(nongratname))
        bot.send_sticker(message.chat.id, random.choice(angrystickerpack))
    else:
        bot.reply_to(message, 'RUSSIAN, MOTHERFUCKER, DO YOU SPEAK IT ?')
        bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
bot.polling()
