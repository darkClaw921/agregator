from datetime import datetime, timedelta
import re
import postgreWork
from chromaDBwork import add_to_collection, query
from tqdm import tqdm
from pprint import pprint

def time_epoch():
    from time import mktime
    
    dt = datetime.now()
    sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond/1000000.0

    millis_since_epoch = sec_since_epoch * 1000
    return int(millis_since_epoch)

def parsetext(text):
    date = text.split('Дата: ')[1].split('\n')[0]
    time = text.split('Время: ')[1].split('\n')[0]
    theme = text.split('Тема: ')[1].split('\n')[0]
    location = text.split('Локация: ')[1].split('\n')[0]

    date = date.replace('(Понедельник)', '').replace('(Вторник)', '').replace('(Среда)', '').replace('(Четверг)', '')\
    .replace('(Пятница)', '').replace('(Суббота)', '').replace('(Воскресенье)', '')
    
    date_time_str = f"{date} {time}"
    date_time_obj = datetime.strptime(date_time_str, '%d.%m %H:%M') 
    print(date_time_str)
    return date, time, theme, location


def extract_date(text):
    # date_pattern = r'\d{1,2}\s\w+'  # Matches the pattern "24 января"
    date_pattern = r'\d{1,2}\s(?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)'

    date_match = re.search(date_pattern, text)
    if date_match:
        date = date_match.group(0)
        return date
    else:
        return None

def find_patterns(text):
    text = text.lower()
    time_pattern = r'\d{2}:\d{2}'  # Matches the pattern "18:00"
    date_pattern = r'\d{1,2}\.\d{2}'  # Matches the pattern "21.01"
    days_of_week_pattern = r'(понедельник|вторник|сред[ау]|четверг|пятниц[ау]|суббот[ау]|воскресень[ея])'  # Matches the days of the week in different cases

    time_matches = re.findall(time_pattern, text)
    date_matches = re.findall(date_pattern, text)
    days_of_week_matches = re.findall(days_of_week_pattern, text)
    extracted_date = extract_date(text)
    

    # Check for words like "завтра" and "сегодня" and convert them to datetime format
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    if "завтра" in text:
        date_matches.append(tomorrow.strftime("%d.%m"))
    if "сегодня" in text:
        date_matches.append(today.strftime("%d.%m"))
    if "послезавтра" in text:
        date_matches.append((tomorrow + timedelta(days=1)).strftime("%d.%m"))
    
    lenText=[]
    lensymbol=len(text)
    if lensymbol>=250: lenText.append(250)
        

    return time_matches, date_matches, days_of_week_matches, extracted_date, lenText

def check_pattern_count(text):
    time_matches, date_matches, days_of_week_matches, extracted_date, lenText = find_patterns(text)
    total_matches = len(time_matches) + len(date_matches) + len(days_of_week_matches) + (1 if extracted_date else 0) + len(lenText)
    print("Time matches:", time_matches)
    print("Date matches:", date_matches)
    print("Days of week matches:", days_of_week_matches)
    print("Extracted date:", extracted_date)
    return total_matches >= 2

def check_dublicate_post(text):
    posts=postgreWork.get_posts()
    for post in posts:
        if post.text == text:
            return True
    return False

def create_db():

    # with open(f'textPrepare_{datetime.now().strftime("%d-%m-%Y")}.txt', "a+") as file:
    #     if file.read() != '':
    #         return file.read()
        
    posts=postgreWork.get_posts()
    prepateText=''
    for post in tqdm(posts):
        pos=post.__dict__
        pos = {key: value for key, value in pos.items() if value is not None}
        
        pos.pop('_sa_instance_state')
        # pos['date']=pos['date'].strftime("%d.%m.%Y")
        pos['created_date']=pos['created_date'].strftime("%d.%m.%Y")

        # 
        separator='=========='

        # try:
            # theme = re.search(r'Тема: (.+)', pos['payload']).group(1)
        # except: continue
        # print(theme)
        prepateText+=f"{separator}\n{pos['text']}"
        
        # add_to_collection(pos['payload'],pos)
        # file.write(prepateText)
    return prepateText

def convert_text_to_variables(text):
    lines = text.split('\n')
    date = None
    time = ''
    topic = None
    location = None
    cost = None
    organizer = None
    language = None
    event = None
    print(text)
    for line in lines:
        if line.startswith('Дата:'):
            try:
                date = line.split(': ')[1]
            except: 
                date ='0'
        elif line.startswith('Время:'):
            time = line.split(': ')[1]
        elif line.startswith('Тема:'):
            topic = line.split(': ')[1]
        elif line.startswith('Локация:'):
            location = line.split(': ')[1]
        elif line.startswith('Стоимость участия:'):
            try:
                cost = line.split(': ')[1]
            except:
                cost = '0'
        elif line.startswith('Организатор:'):
            organizer = line.split(': ')[1]
        elif line.startswith('Язык:'):
            language = line.split(': ')[1]
        elif line.startswith('Мероприятие:'):
            event = line.split(': ')[1]

    return date, time, topic, location, cost, organizer, language, event

        
def create_db2():

    # with open(f'textPrepare_{datetime.now().strftime("%d-%m-%Y")}.txt', "a+") as file:
    #     if file.read() != '':
    #         return file.read()
        
    posts=postgreWork.get_posts()
    prepateText=''
    for post in tqdm(posts):
        pos=post.__dict__
        pos = {key: value for key, value in pos.items() if value is not None}
        
        pos.pop('_sa_instance_state')
        # pos['date']=pos['date'].strftime("%d.%m.%Y")
        pos['created_date']=pos['created_date'].strftime("%d.%m.%Y")

        # 
        separator='=========='
        date, time, topic, location, cost, organizer, language, event=convert_text_to_variables(pos['payload'])
        
        meta={
        'id': pos['id'],
        'date': date,
        'time': time,
        'topic': topic,
        'location': location,
        'cost': cost, 
        'organizer': organizer, 
        'language': language, 
        'event': event,
        'text': pos['text']}        
        # print(theme)
        pprint(meta)
        prepateText+=f"{separator}\n{pos['text']}"
        
        add_to_collection(topic,meta)
        # file.write(prepateText)
    return prepateText
        
# text="""Дата: 02.02.2024
# Время: 15.00
# Тема: Банная мистерия
# Локация: Убуда
# Стоимость участия: 0 (информация отсутствует)
# Организатор: Указано только, что запись обязательна
# Язык: русский
# Мероприятие: 1"""
# a =convert_text_to_variables(text)
# pprint(a)

# create_db2()
# while True:
#     text=input()
#     a=query(text,{'location':'02.02.2024'})
#     pprint(a)