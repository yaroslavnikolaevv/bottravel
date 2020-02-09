#!/usr/bin/python
# -*- coding: UTF-8 -*-
import apiai
from create import *
import json
import telebot
import wikipedia
import random
import time
import re
import pyowm
import requests
# from mqtt import *
import datetime
#import reader
import os
from dotenv import load_dotenv
import codecs
import urllib.request
from bs4 import BeautifulSoup as bs
from parsing import *
#Блок токена
token = load_dotenv()
token = os.getenv('TOKEN')
#Защита от DDoS
ddos_defend = {}
minimalq = 0
ban_list=[]
count = 0
search_info=0
#Блок такси
place = ''
f = codecs.open( 'taxinumbers.txt', "r", "utf_8_sig" )
taxicities = f.read()
taxicities = taxicities.split('\r\n')[:-1]
taxidict = dict()
for i in taxicities:
    key = i[:i.index(';')]
    taxidict[key] = i[i.index(';') + 2:]
#Блок стикеров
commandlist = {'/advice' : 'advice_message(message)', '/wikipedia' : 'wikipedia_message(message)', '/placeinfo' : 'wikipedia_message(message)', '/start': 'start_message(message)', '/help' : 'help_message(message)', '/tickets' : 'tickets_message(message)', '/route' : 'tickets_message(message)', '/weather' : 'weather_message(message)', '/music' : 'music_message(message)', '/developers' : 'developers_message(message)', '/taxi' : 'taxi_message(message)', '/video' : 'video_message(message)'}
commandlist_ru = {'советы' : 'advice_message(message)', 'википедия' : 'wikipedia_message(message)', 'информация про город' : 'wikipedia_message(message)', 'старт': 'start_message(message)', 'помощь' : 'help_message(message)','найти билеты' : 'tickets_message(message)', 'маршрут' : 'tickets_message(message)', 'погода' : 'weather_message(message)', 'музыка' : 'music_message(message)', 'контакты разработчиков' : 'developers_message(message)', 'номера такси' : 'taxi_message(message)', 'найти видео' : 'video_message(message)', 'обратная связь' : 'feedback_message(message)'}
lovestickerpack = ['CAADAgAD2QADVp29CtGSZtLSYweoFgQ', 'CAADAgAD0gADVp29Cg4FcjZ1gzWKFgQ', 'CAADAgAD0wADVp29CvUyj5fVEvk9FgQ', 'CAADAgAD2AADVp29CokJ3b9L8RQnFgQ', 'CAADAgAD3gADVp29CqXvdzhVgxXEFgQ', 'CAADAgADFQADwDZPE81WpjthnmTnFgQ', 'CAADAgADBQADwDZPE_lqX5qCa011FgQ', 'CAADAgADDQADwDZPE6T54fTUeI1TFgQ', 'CAADAgADHQADwDZPE17YptxBPd5IFgQ', 'CAADAgAD4QcAAnlc4gndRsN-Tyzk1xYE', 'CAADAgAD3wcAAnlc4gmeYgfVO_CEsxYE', 'CAADAgAD4AcAAnlc4gmXqeueTbWXlRYE', ]
questionstickerpack = ['CAADAgAD4wADVp29Cg_4Isytpgs3FgQ', 'CAADAgADEgADwDZPEzO8ngEulQc3FgQ', 'CAADAgADEAADwDZPE-qBiinxHwLoFgQ', 'CAADAgADIAADwDZPE_QPK7o-X_TPFgQ', 'CAADAgAD2wcAAnlc4gkSqCLudDgLbhYE', 'CAADAgADzwcAAnlc4gnrZCnufdBTahYE', 'CAADAgAD2QcAAnlc4gn3Ww8qzk3S3BYE', 'CAADAgAD0gcAAnlc4gmLqZ82yF4OlxYE']
angrystickerpack = ['CAADAgAD3AADVp29Cpy9Gm5Tg192FgQ', 'CAADAgAD2wADVp29Clxn-p9taVttFgQ', 'CAADAgADywADVp29CllGpcs9gzQoFgQ']
loadstickerpack = ['CAADAgADGAADwDZPE9b6J7-cahj4FgQ', 'CAADAgAD1QADVp29CveXwRdcmk7nFgQ', 'CAADAgADwAADVp29Ct1dnTI9q-YvFgQ', 'CAADAgAD4QADVp29ClvBlItA-NOgFgQ', 'CAADAgAD5QADVp29CggLFmSVBdGKFgQ']
#недопустимые символы в названии файла

#Блок имен
developerslist = ['рустам', 'ярослав', 'владимир', 'даниэль', 'игорь']
nongratlist = ['арина', 'ариша', 'алия']
#Блок кнопок
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('номера такси', 'найти билеты', 'погода')
keyboard1.row('музыка', 'найти видео', 'информация про город')
keyboard1.row('советы', 'помощь')
keyboard1.row('старт', 'контакты разработчиков')
keyboard1.row('обратная связь')
keyboardExit= telebot.types.ReplyKeyboardMarkup(True, True)
keyboardExit.row('Назад к функционалу')
req_us = {}
#Блок погоды
owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language='ru')
bot = telebot.TeleBot(token)
#Блок переменных
fromplace_dict = {}
toplace_dict = {}
dateregistration_dict = {}
video_search = ''
video_search_list = []
videos_for_dict = {}
res = ''
status = ''
users=""
q = []
bylo=""
already = 0
def run_pars(args):
	fromInput = args[0]
	fromOutput = args[1]
	date = args[2]
	user = args[3]
	withuser = Parsers(fromInput,fromOutput,date,user).threader().split(":")
	withoutuser = withuser[1:]
	itog = ':'.join(withoutuser)
	return(itog)
class read_feedback:
        
        def read(self):
                global bylo
                r=open('feedback.txt',mode='r')
                
                for line in r:

                        bylo+=line

                r.close()

                bylo=bylo+'\n'
                return bylo
class read_users:
        
        def read(self):
                global users
                r=open('users.txt',mode='r')
                
                for line in r:

                        users+=line

                r.close()

                users=users+'\n'
                return users

#Блок для советов
@bot.message_handler(commands=['advice'])
def advice_message(message):
	bot.send_message(message.chat.id, 'Возможно вам понадобятся следущие вещи:')
	bot.send_message(message.chat.id, ' *Документы* :\nпаспорт: внутренний или загран; документы для ребенка: 1) паспорт, 2) свидетельство о рождении, 3) согласие на выезд из России, если ребенок едет за границу без родителей; наличные деньги; билеты на самолет, поезд, автобус; брони отелей; водительские права; копия паспорта; страховой полис путешественника' , parse_mode="Markdown")
	bot.send_message(message.chat.id, ' *Техника и гаджеты в дорогу* : \ncмартфон и зарядка; внешний жесткий диск; дорожный утюг; маленький электрический чайник; наушники; ноутбук и зарядка; переходник для розеток; плеер; тройник, удлинитель или сетевой фильтр; фен; фотоаппарат, зарядка, карты памяти, сумка для камеры; штатив, монопод, палка для селфи; электронная книга' , parse_mode="Markdown")
	bot.send_message(message.chat.id, ' *Бытовые мелочи и комфорт в поездке:* \nсумочка или городской рюкзак для прогулок; блокнот и ручка; вилка, ложка, тарелка, чашка; зонт; карманное зеркало; карта; книга, путеводитель, журнал; маска для сна, беруши, надувная подушка; обычные пакеты; полотенце; разговорник; солнечные очки; туалетная бумага; швейный набор; швейцарский армейский нож' , parse_mode="Markdown")
	bot.send_message(message.chat.id, ' *Гигиена и косметика в поездку* : \nбритва; дезодорант; зубная паста и щетка; расческа; ватные палочки, ватные диски; Влажные салфетки, бумажные платочки; гигиеническая помада, бальзам для губ; гигиенические прокладки, тампоны; дезинфицирующий гель для рук; зубная нить, зубочистки; крем от солнца; кремы для лица и тела; ножницы и пилочка для ногтей; очки или контактные линзы с контейнером и раствором; парфюм; пена для и после бритья; помада, тушь для ресниц и другая декоративная косметика, средство для снятия макияжа; репеллент от комаров; средство для укладки волос; фумигатор; шампунь, кондиционер для волос, мыло, гель для душа, мочалка' , parse_mode="Markdown")
	bot.send_message(message.chat.id, ' *Одежда и обувь в путешествие* : \nблузка / рубашка; брюки / джинсы / штаны; кофта / худи / свитер / теплая рубашка; нижнее белье; носки / колготки; удобная обувь на каждый день; футболки с короткими и длинными рукавами; аксессуары; домашняя одежда / пижама; купальник / плавки; куртка; нарядная обувь «на выход»; плащ-дождевик или непромокаемая куртка; шлепки / сланцы; шляпа / бейсболка / панама от солнца; Шорты; юбка / платье' , parse_mode="Markdown")
	bot.send_message(message.chat.id, ' *Лекарства* для одного взрослого в спокойный отпуск на 2–3 недели: /nНурофен (Обезболивающее, жаропонижающее) 20 таблеток (200 мг); Но-шпа (При мышечных спазмах) 6 таблеток (40 мг); Полисорб МП (Сорбент: при пищевом отравлении) 10 пакетиков (3 г); Мезим форте (Пищеварительное ферментное средство: при переедании, тяжести в животе, вздутии) 10 таблеток; Церукал (При рвоте, в т. ч. мешающей приему лекарств) 5 таблеток (10 мг); Имодиум (При диарее) 6 таблеток (2 мг); Хлоргексидин, пластырь и бинт (Антисептик для обработки ран) пластиковый флакон 50 мл; Септолете (Антисептик от боли в горле) 10 таблеток для рассасывания' , parse_mode="Markdown")
#
#Блок для Википедии
@bot.message_handler(commands=['placeinfo', 'wikipedia'])
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
			print(ttnumbers)
			if len(ttnumbers) >= 5:
				for i in range(5):
					bot.send_message(message.chat.id, ttnumbers[i])
			else:
				for i in range(len(ttnumbers)):
					bot.send_message(message.chat.id, ttnumbers[i])
		except:
			global questionstickerpack
			bot.reply_to(message, 'Извините, в моей базе данных пока нет такого города')
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
        bot.send_message(message.chat.id, 'Введите дату отправления в формате DD.MM.YYYY')#rzd
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
        global minimalq
        global lovestickerpack
        global q
        global already
        global ban_list
        dateregistration_dict.update({str(message.chat.id):message.text.lower()})
   
       
        if len(q)<1:
            q.append([fromplace_dict[str(message.chat.id)],toplace_dict[str(message.chat.id)],dateregistration_dict[str(message.chat.id)],str(message.chat.id)])    
            bot.send_message(q[len(q)-1][3],"Вы добавлены в очередь по поиску билетов,ожидайте. Ввод команд может быть недоступен до завершения поиска")
        else:
            bot.send_message(message.chat.id,'Попробуйте попозже, на данный момент очередь функции забита, напишите через несколько секунд,введите "старт"')
            bot.register_next_step_handler(message,start_message)
            
        #добавили поток в очередь
        #ран - очередь от нуля
        #запускаем ран
        #пока запущено не равно нулю-пауза
        while already!=0:
            time.sleep(0.1)
            
            #если запущено равно нулю запускаем
        else:
            global loadstickerpack
            global lovestickerpack
            run=q[0]
            ban_list.append(run[3])
            bot.send_message(run[3], 'Ищу билеты по выбранным критериям...')
            bot.send_sticker(run[3], random.choice(loadstickerpack))
            already=1
                
            bot.send_message(run[3], run_pars(run))
            bot.send_sticker(run[3], random.choice(lovestickerpack))
            #ран парс-ссылки
            already=0
            del q[0]
            del ban_list[ban_list.index(run[3])]
            
#Блок для команды старт
@bot.message_handler(commands=['start'])

def start_message(message):
    global weatherinformation
    global lovestickerpack
    Create_user(str(message.chat.id)).create()
    bot.send_message(message.chat.id, 'Привет!\nМеня зовут *Travellta* !\nВот список моих функций :\n 1) *старт* \n 2) *погода* \n 3) *номера такси* в том или ином городе\n 4) *музыка* не даст вам заскучать в поездке \n 5) *найти видео* - мы найдём *ЛЮБОЕ* видео ,имеющееся в интернете за вас, в скором времени появится возможность скачивания видео \n 6) *информация про город* -мы расскажем вам о любом городе и ,если хотите, о чём-либо ещё \n 7) *разработчики* - контакты разработчиков \n 8) *найти билеты* - мы просмотрим за вас сайты ржд и S7 (тестовая функция) \n 9) *советы* - функция поможет не забыть взять в дорогу что-либо, \n 10) *А так же Я (Travellta) ОБЛАДАЮ ИСКУССТВЕННЫМ ИНТЕЛЛЕКТОМ* , для того,чтобы пообщаться со мной напишите любое слово, например, "привет" \n 11) *ТАКЖЕ Я УМЕЮ ЗАЩИЩАТЬСЯ ОТ DoS атак, так что давайте уважать друг друга ;)*', parse_mode="Markdown", reply_markup=keyboard1)
    bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
#Блок для погоды
@bot.message_handler(commands=['weather'])
def weather_message(message):
    bot.send_message(message.chat.id, 'Напишите город, погодные условия которого вы хотели бы узнать')
    bot.register_next_step_handler(message, weather_information)
    
def weather_information(message):
    global place
    global status
    global owm
    global questionstickerpack
    if message.text.lower() in commandlist:
        exec(commandlist[message.text.lower()])
    elif message.text.lower() in commandlist_ru:
        exec(commandlist_ru[message.text.lower()])
    elif '/' + message.text.lower() in commandlist:
        exec(commandlist['/' + message.text.lower()])
    else:
        try:
            place = message.text.lower()
            print(place)
            observation = owm.weather_at_place(place)
            weather = observation.get_weather()
            status = weather.get_detailed_status()
            temp = weather.get_temperature('celsius')['temp']
            wind = weather.get_wind()['speed']
            weathercity = message.text[0].upper() + message.text.lower()[1:]
            bot.send_message(message.chat.id, 'Погода в городе {0} :\nТемпература : {1}°C\nПогодные условия : {2}\nСкорость ветра : {3} м/с'.format(weathercity, temp, status, wind))
        except:
            try:
                nd = {"й" : "j", "ц" : "c", "у" : "u", "к" : "k", "е" : "e", "н" : "n", "г" : "g", "ш" : "sh", "щ" : "shh", "з" : "z",
                      "х" : "h", "ф" : "f", "ы" : "y", "в" : "v", "а" : "a", "п" : "p", "р" : "r", "о" : "o", "л" : "l", "д" : "d", "ж" : "zh",
                      "э" : "je", "я" : "ya", "ч" : "ch", "с" : "s", "м" : "m", "и" : "i", "т" : "t", "б" : "b", "ю" : "ju", "ё" : "jo"}
                fplace = [place[i] for i in range(len(place))]
                fplace = [nd[i] for i in fplace]
                place = ''.join(fplace)
                observation = owm.weather_at_place(place)
                weather = observation.get_weather()
                status = weather.get_detailed_status()
                temp = weather.get_temperature('celsius')['temp']
                wind = weather.get_wind()['speed']
                weathercity = message.text[0].upper() + message.text.lower()[1:]
                bot.send_message(message.chat.id, 'Погода в городе {0} :\nТемпература : {1}°C\nПогодные условия : {2}\nСкорость ветра : {3} м/с'.format(weathercity, temp, status, wind))
            except:
                bot.reply_to(message, 'Извините, в моей базе данных пока нет такого города')
                bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
#Блок для помощи
@bot.message_handler(commands=['help'])
def help_message(message):
    global lovestickerpack
    bot.send_message(message.chat.id, '1. *старт* - возвращает наш диалог к исходному состоянию \n 2. *погода* - узнать погоду в любом городе мира \n 3. *найти билеты* , *маршрут* - узнать доступные на данный момент билеты \n 4. *номера такси* - узнать номера такси в выбранном городе \n 5. *музыка* - прослушать случайные треки, выбранные нашей командой \n 6. *найти видео* - найти видео по запросу \n 7. *Википедия* , *информация про город* - позволяет узнает краткую информационную сводку из Википедии \n 8. *контакты разработчиков* - узнать контактные данные нашей команды \n *советы* - поможем вам собраться в путешествие и ничего не забыть ' , parse_mode="Markdown")
    bot.send_sticker(message.chat.id,random.choice(lovestickerpack))
#Блок для музыки
@bot.message_handler(commands=['music'])
def music_message(message):
    audiolist = []
    for i in range(2):
        while True:
            n = random.randint(1,45)
            if n not in audiolist:
                break
        audiolist.append(n)
        audio = open(str(n) + ".mp3", mode='rb')
        print("opened " + str(n) + ".mp3")
        bot.send_audio(message.from_user.id, audio)
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
                res = 'https://www.youtube.com' + links[0]

            else:
                res = 'https://www.youtube.com' + links[1]
            bot.send_message(message.chat.id, res)
        except:
            global questionstickerpack#
            bot.send_message(message.chat.id, 'Извините, в моей базе данных пока нет такого видео')
            bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    bot.send_message(message.chat.id, 'Напишите ваш вопрос/предложение или замеченный баг')
    bot.register_next_step_handler(message, get_feedback_message)
def get_feedback_message(message):
    Create_feedback(message.chat.id,message.text).create()
    bot.send_message(message.chat.id, 'Ваше предложение отправлено, вам в скором времени ответят')


#Блок для обработки текста
@bot.message_handler(content_types=['text'])
def text_analyze(message):
    global ddos_defend
    global lovestickerpack
    global angrystickerpack
    global questionstickerpack
    global search_info
    global ban_list

    user=str(message.chat.id)
    if user=="744417229":
        if "разбан" in message.text.lower():
            messag=message.text.lower().split[':']	
            id_r=str(messag[1])
            del ban_list[str(id_r)]
            now=datetime.datetime.now()
            ddos_defend.update({id_r:[now,1]})
        elif message.text.lower()=="разбанить всех":
            for i in ban_list:
                
                
                now=datetime.datetime.now()
                ddos_defend.update({i:[now,1]})
            ban_list=[]
        elif message.text.lower()=="забаненные":
            all=""
            for i in ban_list:
                all=all+str(i)+"\n"
            bot.send_message("744417229",str(all))
        elif message.text.lower()=='запросы':
                bot.send_message("744417229",read_feedback().read())
        elif 'отправить' in message.text.lower():
                ms= message.text.lower().split(":")
        	#отправить:id:message
                idd=ms[1]
                senddd=ms[2]
                bot.send_message(str(idd),senddd)
        elif message.text.lower()=="юзеры":
                bot.send_message('744417229',read_users().read())
    if user=="840787844":
        if "разбан" in message.text.lower():
            messag=message.text.lower().split[':']	
            id_r=str(messag[1])
            del ban_list[str(id_r)]
            now=datetime.datetime.now()
            ddos_defend.update({id_r:[now,1]})
        elif message.text.lower()=="разбанить всех":
            for i in ban_list:
                
                
                now=datetime.datetime.now()
                ddos_defend.update({i:[now,1]})
            ban_list=[]
        elif message.text.lower()=="забаненные":
            all=""
            for i in ban_list:
                all=all+str(i)+"\n"
            bot.send_message("840787844",str(all))
        elif message.text.lower()=='запросы':
                bot.send_message("840787844",read_feedback().read())
        elif 'отправить' in message.text.lower():
                ms= message.text.lower().split(":")
        	#отправить:id:message
                idd=ms[1]
                senddd=ms[2]
                bot.send_message(str(idd),senddd)
        elif message.text.lower()=="юзеры":
                bot.send_message('840787844',read_users().read())
    global count
    
    if user not in ban_list:
        try:
            prev=ddos_defend[user][0] #ищем время предыдущего сообщения
            #нашли время, то есть сообщение НЕ первое
            count=ddos_defend[user][1] #сколько сообщений отправил с маленьким таймингом, первое сообщение = 1
            now = datetime.datetime.now()
            difference=int((now-prev).total_seconds())
            search_info=1
            print("Не первый раз,счётчик равен "+str(count))
            if difference<3 and search_info==1:
                count=count+1
                now=datetime.datetime.now()
                ddos_defend.update({user:[now,count]})
                search_info=0
                print("разница во времени:"+str(difference))
            elif difference>=3 and search_info==1:
                try:
                
                    now=datetime.datetime.now()
                    count=1
                    ddos_defend.update({user:[now,count]})
                    print('пользователь:'+user+'; обновленный счётчик:'+str(count)+' Разница между сообщениями:'+str(difference))
                    search_info=0
                except:
                    print(' время больше 3 секунд, счётчик равен'+str(count))
        except KeyError:
            #чел написал первый раз
            count=1
            search_info=0
            
            now=datetime.datetime.now()
            ddos_defend.update({user:[now,count]}) #записываем в словарь время и счётчик=1
            

    if count == 4:
        ban_list.append(user)
        count  =6
        bot.send_message(message.chat.id,"Ваши сообщения были восприняты как спам, вы забанены... Автоматический разбан будет только на следующий день\n Ваш ид:"+str(user)+'сообщите его разработчикам для разбана')
    elif count == 3:
        bot.send_message(message.chat.id, 'Вы слишком быстро отвечаете,пожалуйста подождите около четырёх секунд, ваши сообщения воспринимаются мной как спам. При продолжении вы будете забанены')           
    if user not in ban_list:
        
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
            try:
                ai(message)
            except:
                bot.send_message(message.chat.id,'Я тебя не понимаю')
                bot.register_next_step_handler(message, start_message) 

def ai(message):
    request = apiai.ApiAI('588ff7875dc8440394e11ff2bbc9e367').text_request() # токен DialogFlow 
    request.lang = 'ru' 
    request.session_id = 'session_1' # сюда можно писать что захотите 
    request.query = message.text 
    response = json.loads(request.getresponse().read().decode('utf-8')) 
    answer = str(response['result']['fulfillment']['speech']) 
    if message.text.lower() == 'назад к функционалу': 
       bot.send_message(message.chat.id, 'Хорошо\nПриятно было с вами пообщаться', reply_markup=keyboard1) 
      # bot.register_next_step_handler(message, start_message) 
    if (answer != '') and (message.text.lower()!='назад к функционалу'): 
       bot.send_message(message.chat.id, answer,reply_markup=keyboardExit) 
       bot.register_next_step_handler(message, text_analyze) 
    
bot.polling(none_stop=True)

