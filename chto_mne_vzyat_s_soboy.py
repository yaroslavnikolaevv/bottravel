# -*- coding: utf8 -*-
import telebot
bot = telebot.TeleBot("955705841:AAH2Pj9QrLas4Nk_UFWy4sh5swl05n2AKOU")

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == "что взять с собой":
		bot.send_message(message.chat.id, 'соси;\n sosi:Соси')
		bot.send_message(message.chat.id, 'Документы:\nпаспорт: внутренний или загран; документы для ребенка: 1) паспорт, 2) свидетельство о рождении, 3) согласие на выезд из России, если ребенок едет за границу без родителей; наличные деньги; билеты на самолет, поезд, автобус; брони отелей; водительские права; копия паспорта; страховой полис путешественника')
		bot.send_message(message.chat.id, 'Техника и гаджеты в дорогу: \ncмартфон и зарядка; внешний жесткий диск; дорожный утюг; маленький электрический чайник; наушники; ноутбук и зарядка; переходник для розеток; плеер; тройник, удлинитель или сетевой фильтр; фен; фотоаппарат, зарядка, карты памяти, сумка для камеры; штатив, монопод, палка для селфи; электронная книга')
		bot.send_message(message.chat.id, 'Бытовые мелочи и комфорт в поездке: \nсумочка или городской рюкзак для прогулок; блокнот и ручка; вилка, ложка, тарелка, чашка; зонт; карманное зеркало; карта; книга, путеводитель, журнал; маска для сна, беруши, надувная подушка; обычные пакеты; полотенце; разговорник; солнечные очки; туалетная бумага; швейный набор; швейцарский армейский нож')
		bot.send_message(message.chat.id, 'Гигиена и косметика в поездку: \nбритва; дезодорант; зубная паста и щетка; расческа; ватные палочки, ватные диски; Влажные салфетки, бумажные платочки; гигиеническая помада, бальзам для губ; гигиенические прокладки, тампоны; дезинфицирующий гель для рук; зубная нить, зубочистки; крем от солнца; кремы для лица и тела; ножницы и пилочка для ногтей; очки или контактные линзы с контейнером и раствором; парфюм; пена для и после бритья; помада, тушь для ресниц и другая декоративная косметика, средство для снятия макияжа; презервативы; репеллент от комаров; средство для укладки волос; фумигатор; шампунь, кондиционер для волос, мыло, гель для душа, мочалка')



bot.polling()