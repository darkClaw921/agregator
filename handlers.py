from aiogram import types, F, Router, html, Bot
from aiogram.types import (Message, CallbackQuery,
                           InputFile, FSInputFile,
                            MessageEntity, InputMediaDocument,
                            InputMediaPhoto, InputMediaVideo, Document)
from aiogram.filters import Command, StateFilter
from aiogram.types.message import ContentType
from pprint import pprint
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Any, Dict
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# from helper import (get_all_user_list, get_dates, 
#                     timestamp_to_date, time_epoch,
#                     get_future_events, prepare_message_event,
#                     get_today_pracktik,prepare_message_pracktik,
#                     langList, langListKeybord, typeFiles)
# # from createKeyboard import *
# from payments import *
from dotenv import load_dotenv
import os
from chat import GPT
import postgreWork 
import chromaDBwork
from loguru import logger
from workRedis import *
# from calendarCreate import create_calendar
from helper import create_db,convert_text_to_variables,create_db2,get_next_weekend,find_and_format_date,find_patterns_date,create_db_for_user
from datetime import datetime,timedelta
from workGS import Sheet
import uuid
import time
import speech_recognition as sr
from promt import clasificatorPromt

load_dotenv()
TOKEN = os.getenv('TOKEN')
# PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')

gpt=GPT()


USER_EVENTS={}
ids=postgreWork.get_all_user_ids()
for id in ids:
    USER_EVENTS[id]=[]
# textAllPosts=create_db()
# create_db2()
# model_index=gpt.load_search_indexes(textAllPosts)

class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()
    spam = State()
    selectLang=State()
    selectPhone=State()
    selectTarif=State()
    inputTarget=State()
    selectTimePracktik=State()
    sendHelp=State()

    #Мероприятия
    addEvent=State()
    inputEvent=State()
    inputDateEvent=State()
    inputTimeEvent=State()
    inputDescriptionEvent=State()
    inputDurationEvent=State()

    #Практики
    addPracktik=State()
    inputPracktik=State()
    inputDatePracktik=State()
    inputTimePracktik=State()
    inputDescriptionPracktik=State()
    inputDurationPracktik=State()
    inputMediaPracktik=State()

# sql = Ydb()

router = Router()

bot = Bot(token=TOKEN,)
sheet = Sheet('profzaboru-5f6f677a3cd8.json','Афиша - Разработка бота')

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    userID=msg.chat.id
    # lang = await sql.get_lang(userID)
    # text = langList[lang]
    nickname=msg.from_user.username
    try: 
        postgreWork.add_new_user(userID,nickname)
        postgreWork.update_model(userID,'gpt')
    except:
        1+0
    # # await state.set_state(Form.selectLang)
    # mess='Здравствуйте, я агрегатор мероприятий бали, проосто напишите куда и когда хотите сходить. Например(12.03 йога) или (завтра танцы) '
    mess="""Привет! Я твой персональный помощник в поиске идеальных мероприятий и развлечений на острове Бали🌴 
Можешь общаться со мной на естественном языке, будь то текст или голосовые сообщения, и рассказать мне о своих предпочтениях. Я помогу подобрать для тебя что-то особенное 💫

Какой тип событий тебя интересует?"""
    await msg.answer(mess)
    return 0

@router.message(Command("gpt"))
async def gpt_handler(msg: Message, state: FSMContext):
    userID=msg.chat.id
    try: 
        postgreWork.update_model(userID,'gpt')
    except:
        1+0
    
    mess="""Вы перешли в режим GPT"""
    await msg.answer(mess)


@router.message(Command("assis"))
async def assis_handler(msg: Message, state: FSMContext):
    userID=msg.chat.id
   
    postgreWork.update_model(userID,'assis')
    
    
    mess="""Вы перешли в режим ассистента"""
    await msg.answer(mess)

@router.message(Command("clear"))
async def clear_handler(msg: Message, state: FSMContext):
    userID=msg.chat.id
    # lang = await sql.get_lang(userID)
    # text = langList[lang]
    
    
    clear_history(userID)
    # # await state.set_state(Form.selectLang)
    # mess='Здравствуйте, я агрегатор мероприятий бали, проосто напишите куда и когда хотите сходить. Например(12.03 йога) или (завтра танцы) '
    mess='История диалога очищена'
    await msg.answer(mess)
    return 0

@router.message(Command("help"))
async def help_handler(msg: Message, state: FSMContext):
    mess="/start - начало работы\n/gpt - перейти в режим GPT\n/assis - перейти в режим ассистента\n/clear - очистить историю диалога"
    await msg.answer(mess)
    return 0

#Обработка калбеков
@router.callback_query()
async def message(msg: CallbackQuery):
    pprint(msg.message.message_id)
    userID = msg.from_user.id
    await msg.answer()
    callData = msg.data
    # pprint(callData)
    logger.debug(f'{callData=}')

           
    return 0

language='ru_RU'
r = sr.Recognizer()

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Sorry.. run again...')
            return "Sorry.. run again..."


@router.message(F.voice)
async def voice_processing(msg: Message, state: FSMContext):
    text = msg.text
    logger.debug(f'{text=}')
    filename = str(uuid.uuid4())
    file_name_full="voice/"+filename+".ogg"
    file_name_full_converted="ready/"+filename+".wav"
    file_info = await bot.get_file(msg.voice.file_id)

    downloaded_file = await bot.download_file(file_info.file_path,destination=file_name_full)
    # time.sleep(2)
    # print(downloaded_file)
    # with open(file_name_full_converted, 'wb') as new_file:
        # with open(file_name_full, 'rb') as file:
            # new_file.write(file.read())
        # new_file.write(downloaded_file)
    # time.sleep(1)
    print("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    # time.sleep(1) 
    text=recognise(file_name_full_converted)
    msg1=msg
    await msg.reply(text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    # a = msg.text
    # print(f'{a=}')
    # message.text = text
    # a = message.text
    # print(f'{a=}')

    # print(f'{message=}')
    
    msg1.__dict__['text'] = text
    pprint(msg1.__dict__)
    await message(msg1, state)  


#Обработка сообщений
@router.message()
async def message(msg: Message, state: FSMContext):
    global USER_EVENTS
    userID = msg.from_user.id
    messText = msg.text
    userName = msg.from_user.username 
    # pprint(msg.__dict__)
    typeModel = postgreWork.get_model(userID)

    if typeModel == 'assis':
        answer, token, tokenPrice=gpt.answer_assistant(messText,1,userID)
        dateNow = datetime.now().strftime("%d.%m.%Y")
        await msg.answer(answer)
        lst=[userName,dateNow, messText, answer, 'assis']
        postgreWork.add_statistick(userName=userName, text=messText, 
                                   queryText=answer, token=token, 
                                   tokenPrice=tokenPrice, theme='assis')
        sheet.insert_cell(data=lst)
        return 0

    

    add_message_to_history(msg.chat.id, 'user', msg.text)
    history = get_history(msg.chat.id)

    


    if len(history) > 20:
        clear_history(msg.chat.id)
        add_message_to_history(msg.chat.id, 'user', msg.text)
        history = get_history(msg.chat.id) 

    # pprint(msg.content_type)
    # chromaDBwork.query()
    print(messText)
    messagesList = [
      {"role": "user", "content": messText}
      ]
    # answer = gpt.answer(promtPreparePost,messagesList)
    

    date=datetime.now().strftime("%d.%m.%Y %A")
    # promt = f'Ты бот-помошник, который помогает пользователю найти мероприятие, которое ему подходит. Учитывай что сегодня {date}.  вот список мероприятий:'
    promt=gpt.load_prompt('https://docs.google.com/document/d/1oezrKsyGHXFie9BZxDLKVJwth8fZEcUq3jyZekL-oNo/edit?usp=sharing')
    promt=promt.replace('[dateNow]',date)
    # answer=gpt.answer_index(system=promt,topic=messText,history=history,search_index=model_index,verbose=False)
    answer = gpt.answer(promt, history, 1)
    token=answer[1]
    tokenPrice=answer[2]
    answer=answer[0]
    
    # answer=gpt.answer_index()
    # pprint(answer)
    # exitText = answer.find('Закончил опрос: 1')
    
    answerTools=gpt.asnwer_tools(history=history)
    
    # pprint(answerTools)
    if answerTools != []:
        typeTool=answerTools[0]['type']
        if typeTool == 'conduct_dialogue':
            add_message_to_history(msg.chat.id, 'system', answer) 
            # await msg.answer(f"Твой ID: {msg.from_user.id}")
            dateNow = datetime.now().strftime("%d.%m.%Y")
            await msg.answer(answer)
        
            postgreWork.add_statistick(userName=userName, text=messText, 
                                    queryText=answer, token=token, 
                                    tokenPrice=tokenPrice, theme='gpt') 
            return 0
        
            

        promt1=gpt.load_prompt('https://docs.google.com/document/d/1IYhd2AHfcw7jwvOO1qbvgFAXVGnYq-ddpj_LH8_oe_A/edit?usp=sharing')
        asnwerTargets=gpt.answer(promt1, history, 1)
        # asnwerTargets=gpt.answer_yandex(promt1, history, 1)
        pprint(asnwerTargets)
        # location=answerTools[1].lower()
        location = answerTools[0]['output']['location']
        date = answerTools[0]['output']['date']
        theme = answerTools[0]['output']['theme']

        targets=asnwerTargets[0].split(',')
        targets=[i.strip() for i in targets]
        print(f'{targets=}')
        print(f'{location=}')
        
        postgreWork.add_statistick(userName=userName, text=messText,
                                   token=asnwerTargets[1], tokenPrice=asnwerTargets[2],
                                    targets=targets, theme='targets', queryText=messText)

        match answerTools[0]['output']:
            case {'location': str() as location}:
                location=location.lower()
                posts=postgreWork.get_posts_for_targets_and_location(targets, location)
                print(f'есть локация')
            case {'location': None}:
                posts=postgreWork.get_posts_for_targets(targets)
            case _:
                print(f'нет локации')

         
        # if location != 'None' or location != '0' or location != '' or location is not None:
            
        # else: 
        

        create_db_for_user(str(userID), posts)
        
        distanceLimit=2 
        answerTools=answerTools[0]
        # date = answerTools['args']['date']
        try:
            date=date.strip()
            date=date.lower()
            date=find_patterns_date(date)
        except:
            date=None

       

       

        
        meta={'date':date}
        pprint(meta)

        if date == 'None' or date=='0' or date=='' or date is None:
            events=chromaDBwork.query(text=theme, result=5, collectionName=str(userID))
        else:
            events=chromaDBwork.query(text=theme, filter1=meta, result=5, collectionName=str(userID))

        events = chromaDBwork.prepare_query_chromadb(events)
        pprint(events)

        countEvent=0        
        # pprint(events)
        for event in events:
            try:
                print('++++++++++++++++++++++++++++++')
                print(event)

                distanseIS=event['distance']>=distanceLimit
                
            except Exception as e:
                print(e)
                answerText="""Прямо сейчас я не нашел мероприятий, соответствующих твоим пожеланиям😔 

Можем попробовать другие критерии. Что бы тебе хотелось еще найти?"""
                await msg.answer(answerText)  
                add_message_to_history(msg.chat.id, 'system', answerText)
                # distanseIS=False
                return 0
                # continue 
            if distanseIS:
                print('Пропускаем мероприятие с большим расстоянием')
                continue
            try:
                event['text']=event['text'].replace('\xa0','')
                event['text']=event['text']+"\n"+str(event['distance'])+"\n"+event['themeSearch']
                event
                if event['id'] in USER_EVENTS[userID]:
                    continue
                else:
                    USER_EVENTS[userID].append(event['id'])
                await msg.answer(event['text'], parse_mode='HTML')

            except Exception as e:
                await msg.answer(str(e))

            countEvent+=1

        if countEvent==0:
            answerText="""Прямо сейчас я не нашел мероприятий, соответствующих твоим пожеланиям😔 

Можем попробовать другие критерии. Что бы тебе хотелось еще найти?"""
            await msg.answer(answerText)  
            add_message_to_history(msg.chat.id, 'system', answerText)
        chromaDBwork.delete_collection(str(userID))
        add_message_to_history(msg.chat.id, 'system', "Мероприятие 1") 
        return 0
   

    add_message_to_history(msg.chat.id, 'system', answer) 
    # await msg.answer(f"Твой ID: {msg.from_user.id}")
    dateNow = datetime.now().strftime("%d.%m.%Y")
    await msg.answer(answer)
   

    postgreWork.add_statistick(userName=userName, text=messText, 
                               queryText=answer, token=token, 
                               tokenPrice=tokenPrice, theme='gpt')
    
    # lst=[userName,dateNow, messText, answer, 'gpt']
    # sheet.insert_cell(data=lst)
    # await msg.send_copy(chat_id=400923372)
    # await bot.send_message(chat_id=400923372, text=f"Твой ID: {msg.from_user.id}")    


if __name__ == '__main__':
    # posts=postgreWork.get_posts()
    # date=datetime.now().strftime("%d.%m.%Y %A")
    # url='https://docs.google.com/document/d/1riRchaMaJC27ikxBx_02W2Z7GANDnFswzTUHy49qaqI/edit?usp=sharing'
    # promt=gpt.load_prompt(url)
    # promt=promt.replace('[dateNow]',date)

    # for post in posts:
        
    # # promt = f'Ты бот-помошник, который помогает пользователю найти мероприятие, которое ему подходит. Учитывай что сегодня {date}.  вот список мероприятий:'
        
    #     # promtUrl=''
    #     messagesList = [
    #   {"role": "user", "content": post.text}
    #   ]
    #     answer=gpt.answer(promt,messagesList)[0]
    #     # print(answer)
    #     date, time, topic, location, cost, organizer, language, event, hashtags=convert_text_to_variables(answer)
    #     theme = topic
    #     location=[location.lower()]

    #     print(f'{theme=}')
    #     print(f'{location=}')
    #     # print(f'{post.__dict__=}')
    #     print(f'{hashtags=}')
    #     for i, a in enumerate(hashtags):
    #         hashtags[i]=a.lower()
            
    #     # 1/0
    #     postgreWork.update_post(post.id,theme=theme,location=location, targets=hashtags)




    # from aiogram import executor
    # executor.start_polling(router)
    pass