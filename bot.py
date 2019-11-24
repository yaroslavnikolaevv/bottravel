#Блок импорта
import telebot
import random
import time, re
import time
import pyowm
import requests
from mqtt import *
import datetime
import reader
import os
from dotenv import load_dotenv
import codecs
import urllib.request
from bs4 import BeautifulSoup as bs
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
commandlist = {'/start': 'start_message(message)', '/help' : 'help_message(message)', '/tickets' : 'tickets_message(message)', '/route' : 'tickets_message(message)', '/weather' : 'weather_message(message)', '/music' : 'music_message(message)', '/developers' : 'developers_message(message)', '/taxi' : 'taxi_message(message)', '/video' : 'video_message(message)'}
commandlist_ru = {'старт': 'start_message(message)', 'помощь' : 'help_message(message)','билеты' : 'tickets_message(message)', 'маршрут' : 'tickets_message(message)', 'погода' : 'weather_message(message)', 'музыка' : 'music_message(message)', 'разработчики' : 'developers_message(message)', 'такси' : 'taxi_message(message)', 'видео' : 'video_message(message)'}
lovestickerpack = ['CAADAgAD2QADVp29CtGSZtLSYweoFgQ', 'CAADAgAD0gADVp29Cg4FcjZ1gzWKFgQ', 'CAADAgAD0wADVp29CvUyj5fVEvk9FgQ', 'CAADAgAD2AADVp29CokJ3b9L8RQnFgQ', 'CAADAgAD3gADVp29CqXvdzhVgxXEFgQ', 'CAADAgADFQADwDZPE81WpjthnmTnFgQ', 'CAADAgADBQADwDZPE_lqX5qCa011FgQ', 'CAADAgADDQADwDZPE6T54fTUeI1TFgQ', 'CAADAgADHQADwDZPE17YptxBPd5IFgQ', 'CAADAgAD4QcAAnlc4gndRsN-Tyzk1xYE', 'CAADAgAD3wcAAnlc4gmeYgfVO_CEsxYE', 'CAADAgAD4AcAAnlc4gmXqeueTbWXlRYE', ]
questionstickerpack = ['CAADAgAD4wADVp29Cg_4Isytpgs3FgQ', 'CAADAgADEgADwDZPEzO8ngEulQc3FgQ', 'CAADAgADEAADwDZPE-qBiinxHwLoFgQ', 'CAADAgADIAADwDZPE_QPK7o-X_TPFgQ', 'CAADAgAD2wcAAnlc4gkSqCLudDgLbhYE', 'CAADAgADzwcAAnlc4gnrZCnufdBTahYE', 'CAADAgAD2QcAAnlc4gn3Ww8qzk3S3BYE', 'CAADAgAD0gcAAnlc4gmLqZ82yF4OlxYE']
angrystickerpack = ['CAADAgAD3AADVp29Cpy9Gm5Tg192FgQ', 'CAADAgAD2wADVp29Clxn-p9taVttFgQ', 'CAADAgADywADVp29CllGpcs9gzQoFgQ']
loadstickerpack = ['CAADAgADGAADwDZPE9b6J7-cahj4FgQ', 'CAADAgAD1QADVp29CveXwRdcmk7nFgQ', 'CAADAgADwAADVp29Ct1dnTI9q-YvFgQ', 'CAADAgAD4QADVp29ClvBlItA-NOgFgQ', 'CAADAgAD5QADVp29CggLFmSVBdGKFgQ']
#Блок имен
developerslist = ['рустам', 'ярослав', 'владимир', 'даниэль', 'игорь']
nongratlist = ['арина', 'ариша', 'алия']
#Блок кнопок
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('start', 'help', 'weather', 'developers')
keyboard1.row('music', 'tickets', 'taxi', 'video')
#Блок погоды
owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = 'ru')
bot = telebot.TeleBot(token)
#Блок переменных
fromplace = str()
toplace = str()
dateregistration = str()
video_search = ''
video_search_list = []
res = ''
status = ''
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
		ttnumbers = taxidict[message.text.lower()]
		ttnumbers = ttnumbers.split('. ')
		ttnumbers = '\n'.join(ttnumbers)
		bot.send_message(message.chat.id, ttnumbers)
#Блок для разработчиков
@bot.message_handler(commands=['developers'])
def developers_message(message):
	print('пока в разработке')
#Блок для поиска билетов
@bot.message_handler(commands=['tickets', 'route'])
def tickets_message(message):
	bot.send_message(message.chat.id, 'Введите город отправления')
	bot.register_next_step_handler(message, fromplace_registration)
	
def fromplace_registration(message):
	global commandlist
	global fromplace
	if message.text.lower() in commandlist:
		exec(commandlist[message.text.lower()])
	elif message.text.lower() in commandlist_ru:
		exec(commandlist_ru[message.text.lower()])
	elif '/' + message.text.lower() in commandlist:
		exec(commandlist['/' + message.text.lower()])
	else:
		fromplace = message.text.lower()
		bot.send_message(message.chat.id, 'Введите город назначения')
		bot.register_next_step_handler(message, toplace_registration)
		
def toplace_registration(message):
	global commandlist
	global toplace
	if message.text.lower() in commandlist:
		exec(commandlist[message.text.lower()])
	elif message.text.lower() in commandlist_ru:
		exec(commandlist_ru[message.text.lower()])
	elif '/' + message.text.lower() in commandlist:
		exec(commandlist['/' + message.text.lower()])
	else:
		toplace = message.text.lower()
		bot.send_message(message.chat.id, 'Введите дату отправления')#rzd
		bot.register_next_step_handler(message, date_registration)
		
def date_registration(message):
	global commandlist
	global fromplace
	global toplace
	global dateregistration
	global loadsticerpack
	if message.text.lower() in commandlist:
		exec(commandlist[message.text.lower()])
	elif message.text.lower() in commandlist_ru:
		exec(commandlist_ru[message.text.lower()])
	elif '/' + message.text.lower() in commandlist:
		exec(commandlist['/' + message.text.lower()])
	else:
		dateregistration = message.text.lower()
		print(fromplace)
		print(toplace)
		print(dateregistration)
		Sendler(fromInput=fromplace,fromOutput=toplace,date=dateregistration).send()
		bot.send_message(message.chat.id, 'Ищу билеты по выбранному направлению')
		bot.send_sticker(message.chat.id, random.choice(loadstickerpack))
		bot.send_message(message.chat.id, 'Билеты по маршруту {0} - {1} на {2} '.format(fromplace, toplace, dateregistration) + "\n" + reader.read())   
#Блок для команды старт
@bot.message_handler(commands=['start'])

def start_message(message):
	global weatherinformation
	global lovestickerpack
	bot.send_message(message.chat.id, 'Привет!\nМеня зовут...плевать, я же тестовый бот\nВот список моих функций на данный момент:\n1./start\n2./weather\n3./help\n4./rzd', reply_markup=keyboard1)
	bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
#Блок для погоды
@bot.message_handler(commands=['weather'])
def weather_message(message):
	bot.send_message(message.chat.id, 'Напишите город, погодные условия которого вы хотели бы узнать')
	bot.register_next_step_handler(message, weather_information)
	
def weather_information(message):
	place=''
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
			bot.send_message(message.chat.id, "Погода города " + weathercity + "\nТемпература: " + str(temp) + "°C" + "\nНа улице: " + str.title(status) + "\nСкорость Ветра: " + str(wind) + "м/c")
			if temp >= 15:
				bot.send_message(message.chat.id, "Погода-mood: Cамое-то ")
			elif 15 > temp  and temp > 0:
				bot.send_message(message.chat.id, "Погода-mood: Накинь что нибудь на себя ")
			elif temp < 0 and -25 < temp:
				bot.send_message(message.chat.id, "Погода-mood: Одевайся мать, пора воевать ")
			elif temp <= -25:
				bot.send_message(message.chat.id, "Погода-mood: Ты умрёшь, если уйдёшь")
		except pyowm.exceptions.api_response_error.NotFoundError:
			bot.reply_to(message, 'Врешь, такого города нет на картах')
			bot.send_sticker(message.chat.id, random.choice(angrystickerpack))
#Блок для помощи
@bot.message_handler(commands=['help'])
def help_message(message):
	global lovestickerpack
	bot.send_message(message.chat.id, '1./start - эта функция позволяет Вам сбросить наш диалог и вернуться к исходной точке\n2./weather - позволяет вам узнать состояние погоды в данном месте\n3./help - эта  функция сработала прямо сейчас')
	bot.send_sticker(message.chat.id,random.choice(lovestickerpack))
#Блок для музыки
@bot.message_handler(commands=['music'])
def music_message(message):
	audiolist = []
	for i in range(3):
		while True:
			n = random.randint(1,34)
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
		video_search = message.text
		video_search_list = video_search.split()
		video_search = 'https://www.youtube.com/results?search_query='
		for i in range(len(video_search_list)):
			video_search += video_search_list[i]
			video_search += '+'
		video_search = video_search[:-1]
		html = requests.get(video_search).text
		soup = bs(html,'html.parser')
		links = soup.find_all(attrs={'class':'yt-uix-tile-link'})
		links= [l['href'] for l in links]
		res = 'https://www.youtube.com/' + links[0]
		bot.send_message(message.chat.id, res)	
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
		developername = message.text[0].upper() + message.text.lower[1:]
		bot.reply_to(message, 'в моей системе рейтинга {0} стоит на первом месте'.format(developername))
		bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
	elif message.text.lower() in nongratlist:
		nongratname = message.text[0].upper() + message.text.lower()[1:]
		bot.reply_to(message, '{0}...{0}...звучит как что-то неприятное'.format(nongratname))
		bot.send_sticker(message.chat.id, random.choice(angrystickerpack))
	elif message.text.lower():
		bot.reply_to(message, 'RUSSIAN, MOTHERFUCKER, DO YOU SPEAK IT ?')
		bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
bot.polling()
