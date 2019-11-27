from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time, re
from threading import Thread
from selenium.webdriver.support.ui import WebDriverWait
import datetime
from selenium.webdriver.support import expected_conditions as EC



rzd_dict={}
s7_dict={}

class Parsers:
    def __init__(self,fromInput,fromOutput,date,user):
        self.fromInput=fromInput
        self.fromOutput=fromOutput
        self.date=date
        self.user=str(user)
    def threader(self):
        global rzd_dict
        global s7_dict
        s7_dict={}
        rzd_dict={}
        
        thread1 = Thread(target=get_r,args=(self.fromInput,self.fromOutput,self.date,self.user))
        thread2 = Thread(target=get_s, args=(self.fromInput,self.fromOutput,self.date,self.user))

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        try:
            return(str(self.user)+':'+'Расписание на ж/д маршруты:'+str(rzd_dict[self.user])+'\n'+'Расписание на авиарейсы:'+str(s7_dict[self.user]))
        except:
            return(str(self.user)+':'+'ничего не найдено')
        
def get_r(fromInput,fromOutput,date,user):
    ur_rzd= ""
    global rzd_dict
    options = webdriver.ChromeOptions()
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument('headless')
    prefs = {
    'profile.managed_default_content_setting_values': {
    'cookies': 1,
    'images': 2,
    'javascript': 2,
    'plugins': 2,
    'popups': 2,
    'geolocation': 2,
    'notifications': 2,
    'auto_select_certificate': 2,
    'fullscreen': 2,
    'mixed_script': 2,
    'media_stream': 2,
    'media_stream_mic': 2,
    'media_stream_camera': 2,
    'protocol_handlers': 2,
    'push_messaging': 2,
    'ppapi_broker': 2,
    'automatic_downloads': 2,
    'midi_sysex': 2,
    'ssl_cert_decisions': 2,
    'metro_switch_to_desktop': 2,
    'protected_media_identifier': 2,
    'app_banner': 2,
    'site_engagement': 2,
    'durable_storage': 2
    },
    "profile.managed_default_content_settings.images": 2
    }
    options.add_experimental_option("prefs", prefs)    
    options.add_argument('--no-sandbox')        
    
    rzd = webdriver.Chrome(chrome_options=options)
    rzd.implicitly_wait(30)
    rzd_url = "http://rzd.ru/"
    rzd.get(rzd_url)
    datin=rzd.find_element_by_css_selector('#date0')
    datin.click()
    for i in range(10):
        datin.send_keys(Keys.BACK_SPACE)
    datin.send_keys(date)
    gray_box=rzd.find_element_by_css_selector('#container > tbody > tr > td > table > tbody > tr > td.leftCol > div:nth-child(3)')
    gray_box.click()
    print('ввёл дату')
    time.sleep(0.1)
    inp=rzd.find_element_by_id("name0")
    inp.click() 
    time.sleep(0.1)
    inp.send_keys(str(fromInput))
    inp.click()
    time.sleep(0.5)

    inp.send_keys(Keys.ARROW_DOWN,Keys.ENTER)
    time.sleep(0.7)
    print('ввожу город отправления')
    try:
        outp=rzd.find_element_by_id('name1')
        outp.click()
    except:
        time.sleep(0.5)
        outp=rzd.find_element_by_id('name1')
        outp.click()
    time.sleep(0.2)
    outp.send_keys(str(fromOutput))
    outp.click()
    time.sleep(0.5)
    print('ввожу город прибытия')
    outp.send_keys(Keys.ARROW_DOWN,Keys.ENTER)
    time.sleep(0.1)
    print('ввёл')
    try:
        button=rzd.find_element_by_xpath('//*[@id="Submit"]')
        button.click()
        print('кликаю кнопку найти')
    except:
        rzd.quit()
        rzd_dict.update({user:'извините,но ссылки не будет,так как один из городов не найден'})
        return('извините,но ссылки не будет,так как город не найден')
        #return('в одном из городов не найден вокзал, пожалуйста впишите город, в котором есть вокзал')
    ur_rzd=rzd.current_url
    count=0
    rzd.quit()
    rzd_dict.update({user:ur_rzd})
    ur_rzd=""

def get_s(fromInput,fromOutput,date,user):
    ur_s7=''
    global s7_dict
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    prefs = {
    'profile.managed_default_content_setting_values': {
    'cookies': 1,
    'images': 2,
    'javascript': 2,
    'plugins': 2,
    'popups': 2,
    'geolocation': 2,
    'notifications': 2,
    'auto_select_certificate': 2,
    'fullscreen': 2,
    'mixed_script': 2,
    'media_stream': 2,
    'media_stream_mic': 2,
    'media_stream_camera': 2,
    'protocol_handlers': 2,
    'push_messaging': 2,
    'ppapi_broker': 2,
    'automatic_downloads': 2,
    'midi_sysex': 2,
    'ssl_cert_decisions': 2,
    'metro_switch_to_desktop': 2,
    'protected_media_identifier': 2,
    'app_banner': 2,
    'site_engagement': 2,
    'durable_storage': 2
    },
    "profile.managed_default_content_settings.images": 2
    }
    options.add_experimental_option("prefs", prefs)    
    options.add_argument('--no-sandbox')        
    year1=int(date[-4:])
    month1=date[3:5]
    day1=int(date[:2])
    s7 = webdriver.Chrome(chrome_options=options)
    s7.implicitly_wait(30)
    s7_url = "http://s7.ru/"
    s7.get(s7_url)
    time.sleep(0.2)
        # windows=s7.window_handles
        # for window in windows:
        #     s7.switch_to.window(window)
    town1=s7.find_element_by_css_selector('#flights_origin2')
    time.sleep(0.1)
    print('пауза 0.2 секунды,потом стираю город отправления')
    town1.clear()
    time.sleep(0.2)
    town1.send_keys(str(fromInput))
    time.sleep(0.7)
    print('пауза  0.8 сек и подтверждаю')
    town1.send_keys(Keys.ENTER)
    time.sleep(0.2)
    #driver.find_element_by_xpath('//*[@id="aviaBot"]/div[2]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div/div/ul/li/div[2]').click()
    outp=s7.find_element_by_xpath('//*[@id="flights_destination2"]') #город прибвтия
    print('пауза две секунды,потом ввожу город прибытия')
    time.sleep(0.2)
    outp.send_keys(str(fromOutput))
    print('пауза 0.9 сек и подтверждаю')
    time.sleep(0.6)
    outp.send_keys(Keys.ENTER)
    time.sleep(0.2)
    datefalse=s7.find_element_by_xpath('//*[@id="date-opener2"]') #календарь
    print('ебашу календарь')
    WebDriverWait(s7, 4).until(EC.element_to_be_clickable((By.ID, "date-opener2")))
    datefalse.click()
    datefalse.click()
    WebDriverWait(s7, 4).until(EC.element_to_be_clickable((By.ID, "aviaBot")))
    try:
        to_one=s7.find_element_by_xpath('//*[@id="aviaBot"]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/label') #месяц
        to_one.click()
    except:
        s7.quit()
        s7_dict.update({user:'извините,но ссылки не будет,так как один из городов не найден'})
        return(0)
    now=datetime.datetime.now()
    then=datetime.datetime(year=year1,month=int(month1),day=day1)
    delta=then-now
    key=str(month1)+str(year1)
    calendar={'112019':[5,5,6,30],'122019':[6,7,2,31],'012020':[5,3,5,31],'022020':[5,6,6,29],'032020':[6,7,2,31],'042020':[5,3,4,30],'052020':[5,5,7,31],'062020':[5,1,2,30],'072020':[5,3,5,31],'082020':[6,6,1,31],'092020':[5,2,3,30],'102020':[5,4,6,31],'112020':[6,7,1,30]}
    cl=(delta.days//30)
    if (now.day+delta.days) < calendar[key][3]:
        print('pass select month')
            
        print('key:'+key)
        print('delta.month=0')
    elif(now.day+delta.days)//calendar[key][3] == 1:
        try:
            WebDriverWait(s7, 4).until(EC.element_to_be_clickable((By.ID, "ui-datepicker-next-avia")))
        except:
            return(0)
        next_month=s7.find_element_by_xpath('//*[@id="ui-datepicker-next-avia"]')
        next_month.click()
        
        print('delta.month='+str(delta.days//30))
        try:
            WebDriverWait(s7, 4).until(EC.element_to_be_clickable((By.ID, "ui-datepicker-next-avia")))
        except:
            return(0)
    else:
        next_month=s7.find_element_by_xpath('//*[@id="ui-datepicker-next-avia"]') #месяц
        next_month.click()
        
        print('delta.month=')
        try:
            WebDriverWait(s7, 4).until(EC.element_to_be_clickable((By.ID, "datepicker2")))
        except:
            return(0)
        for i in range(cl):
            next_m=s7.find_element_by_xpath('//*[@id="datepicker2"]/div/div/a[2]')
            next_m.click()
    if delta.days>=359:
        print('нема,вводи меньше')
        return("извините,но билетов на эту дату нет,т.к. компанией s7 еще не составлено расписание.Вы можете искать билеты на любой день, который будет не более чем через 359 дней")
    else:
        print('in calendar')
        
        # print(calendar['112019'][0]) #строки
        # print(calendar['112019'][1]) #первый столбик
        # print(calendar['112019'][2]) #последний столбик
        # print(calendar['112019'][3]) #Дни
        print('key:'+key)
        
        raw=1
        max=7
        day=calendar[key][1]
        for i in range(day1-1):
            print('Цикл номер:'+str(i))
            # if(day==max):
            #     raw=raw+1
            #     day=1
            #     print(raw)
            #     print(day)
            # else:
            #     day=day+1
            #     print(day)
            if(day<7):
                day+=1
                print('day'+str(day))

            else:
                raw+=1
                day=1
                print('raw'+str(raw))
                print('day'+str(day))
        print(raw)
        print(day)
        time.sleep(0.1)
        x=s7.find_element_by_css_selector('#datepicker2 > div > table > tbody > tr:nth-child('+str(raw)+') > td:nth-child('+str(day)+') > a')
        x.click()
        #datepicker2 > div > table > tbody > tr:nth-child(5) > td:nth-child(6) > a
    # x=driver.find_element_by_css_selector('#datepicker2 > div > table')
    #datepicker2 > div > table > tbody > tr:nth-child(5) > 
    # submit=driver.find_element_by_css_selector('#date-opener2')


        time.sleep(0.2)
        print('кликаем на кнопку..')
        
        try:
            confirm=s7.find_element_by_xpath('//*[@id="search-btn-expand-bot"]')
            WebDriverWait(s7, 4).until(EC.element_to_be_clickable((By.ID, "search-btn-expand-bot")))
            confirm.click()
        except:
            #return('в одном из городов нет аэропорта, введите город, в котором есть аэропорт или попробуйте еще раз')
            return(0)
        ur_s7=s7.current_url
        s7.quit()
        s7_dict.update({user:ur_s7})
        ur_s7=''
          
