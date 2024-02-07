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
from chat import GPT, promtPreparePost
import postgreWork 
import chromaDBwork
from loguru import logger
from workRedis import *
# from calendarCreate import create_calendar
from helper import create_db,convert_text_to_variables,create_db2
from datetime import datetime
from workGS import Sheet
import uuid
import time
import speech_recognition as sr

load_dotenv()
TOKEN = os.getenv('TOKEN')
# PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')

gpt=GPT()


# textAllPosts=create_db()
create_db2()
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
    userID = msg.from_user.id
    messText = msg.text
    userName = msg.from_user.username 
    # pprint(msg.__dict__)
    typeModel = postgreWork.get_model(userID)

    if typeModel == 'assis':
        answer=gpt.answer_assistant(messText,1,userID)[0]
        dateNow = datetime.now().strftime("%d.%m.%Y")
        await msg.answer(answer)
        lst=[userName,dateNow, messText, answer, 'assis']
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
    

    date=datetime.now().strftime("%d.%m.%Y")
    # promt = f'Ты бот-помошник, который помогает пользователю найти мероприятие, которое ему подходит. Учитывай что сегодня {date}.  вот список мероприятий:'
    promt=gpt.load_prompt('https://docs.google.com/document/d/1oezrKsyGHXFie9BZxDLKVJwth8fZEcUq3jyZekL-oNo/edit?usp=sharing')
    promt=promt.replace('[dateNow]',date)
    # answer=gpt.answer_index(system=promt,topic=messText,history=history,search_index=model_index,verbose=False)
    answer = gpt.answer(promt, history, 1)[0]
    add_message_to_history(msg.chat.id, 'system', answer) 
    # answer=gpt.answer_index()
    # pprint(answer)
    exitText = answer.find('Закончил опрос: 1')
    print(exitText)
    if exitText != -1:
        answer = answer.replace('Закончил опрос: 1','')
        
        date, time, topic, location, cost, organizer, language, event=convert_text_to_variables(answer)
        meta={
        'date': date,
        # 'time': time,
        # 'topic': topic,
        'location': location,
        # 'cost': cost, 
        # 'organizer': organizer, 
        # 'language': language, 
        # 'event': event
        }        
        # print(theme)
        pprint(meta)
        print(topic)
        try:
            events=chromaDBwork.query(topic,meta)
            events = chromaDBwork.prepare_query_chromadb(events)
        except Exception as e:
            print(e)
            events='Мероприятий не найдено'
        # print(events)        
        
        # promt.replace('[dateNow]',date)
        promt+=f'\n\n{events}'
        answer = gpt.answer(promt, history, 1)[0]
        add_message_to_history(msg.chat.id, 'system', answer) 
        await msg.answer(answer)

        # await msg.answer('Все мероприятия закончились')
        return 0
    print(exitText)


    # await msg.answer(f"Твой ID: {msg.from_user.id}")
    dateNow = datetime.now().strftime("%d.%m.%Y")
    await msg.answer(answer)
    postgreWork.add_statistick(userName, messText, answer)
    lst=[userName,dateNow, messText, answer, 'gpt']
    sheet.insert_cell(data=lst)
    # await msg.send_copy(chat_id=400923372)
    # await bot.send_message(chat_id=400923372, text=f"Твой ID: {msg.from_user.id}")    


if __name__ == '__main__':
    
    # from aiogram import executor
    # executor.start_polling(router)
    pass