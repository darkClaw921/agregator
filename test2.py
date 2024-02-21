from telethon import TelegramClient, events
from chat import GPT
from pprint import pprint
import postgreWork
from helper import check_pattern_count,convert_text_to_variables
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os


# Вставьте ваши данные для подключения к Telegram API
# api_id = 'YOUR_API_ID'
# api_hash = 'YOUR_API_HASH'
api_id =os.getenv('API_ID') 
api_hash = os.getenv('API_HASH')
# phone_number = 'YOUR_PHONE_NUMBER'
gpt=GPT()
# Создайте экземпляр клиента Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Авторизуйтесь в клиенте
# client.start(bot_token='6811604760:AAGTiF5eYAbMQKu4-fnbug7DzpMtEBPlgzc')
client.start()

# Определите список идентификаторов каналов, из которых вы хотите получать сообщения
# channel_ids = [-1001281274611, -1001747110091,-1001117865178,'SwiftBook','Герасимова и Игорь Новый','-1002010911633',-1002010911633]  # Замените на реальные идентификаторы каналов
# channel_ids = ['SwiftBook','Герасимова и Игорь Новый','-1002010911633',]  # Замените на реальные идентификаторы каналов
#см Разработка бота Афиша/ tg источники
chenalName = [-1001497691183,
              -1001481640229,
              -1001322025774,
            #   -1002010911633,
              -1001503673245,
              -1001703113785,
              -1001361144761,
              -1001492919625,
              -1001689586012,
              -1001180754166,
              -1001809336275,
              -1001314963617,
              -1001633209682,
              -1001808534933,
              -1001673441826,
              -1001626261360,
              -1002015019095] 
# @client.on(events.NewMessage())
# @client.on(events.NewMessage(chats=lambda x: x in chenalName))
@client.on(events.NewMessage(chats=chenalName))
async def new_message_listener(event):
    # Обработка новых сообщений
    messageID=event.message.id
    # try:
    chenalID=event.message.chat.id
    text=event.message.text

    userSendID=event.message.from_id.user_id
    try:
        userSendNickname=event.message.sender.username
    except:
        userSendNickname=None
    if userSendNickname is None:
        pprint(event.message.__dict__)
        userSendNickname=str(userSendID)
    print(text)
    print(userSendID)
    print(userSendNickname)

    # if len(text) <= 100: return 0
    #Проверяет меняется ли текст мероприятием
    if not check_pattern_count(text):
        postgreWork.add_new_post(
        postID=messageID,
        chatID=chenalID,
        text=text,
        senderNickname=userSendNickname,
        # payload=answer,
        # token=allToken,
        # tokenPrice=allPrice,
        )
        return 0
    
    # 1/0
    chenalID=event.message.chat.id
    print(chenalID)
    # if chenalID == 2010911633:
        # await client.send_message(-1002010911633, message='Это мероприятие!',reply_to=event.message)
        
    messagesList = [
      {"role": "user", "content": text}
      ]
    url='https://docs.google.com/document/d/1riRchaMaJC27ikxBx_02W2Z7GANDnFswzTUHy49qaqI/edit?usp=sharing'
    promt=gpt.load_prompt(url)
    
    dateNow = datetime.now().strftime("%d.%m.%Y %A")
    
    promt=promt.replace('[dateNow]',dateNow)
    answer, allToken, allPrice = gpt.answer(promt,messagesList)
    pprint(answer)
    # if chenalID == 2010911633:
        # await client.send_message(-1002010911633, message=answer,reply_to=event.message)

    # messageID=event.message.id
    # chenalID=event.message.chat.id
    postIsAdd=postgreWork.check_post(text)
    
    if postIsAdd: return 0
    date, time, topic, location, cost, organizer, language, event, hashtags=convert_text_to_variables(answer)
    
    if event == 0: return 0   
    date=datetime.strptime(date, "%d.%m.%Y") 
    if date == 'None' or date=='0': 
        try:
            date = datetime.now().strftime("%d.%m.%Y")
        except:
            date = datetime.now()
    if cost == 'None' or cost=='0': 
        cost = 0
    if event == 'None' or event=='0': 
        event = 0
    elif event=='1':
        event=1

    if organizer == 'None' or organizer=='0': 
        organizer=userSendNickname

    if hashtags == 'None' or hashtags=='0' or hashtags==None: 
        hashtags=['']

    print('добавляем пост')
    
    for i, a in enumerate(hashtags):
        hashtags[i]=a.lower() 

    postgreWork.add_new_post(
        date=date,
        time=time,
        theme=topic,
        location=[location.lower()],
        price=cost,
        organizer=organizer,
        language=language,
        event=event,
        postID=messageID,
        chatID=chenalID,
        text=text,
        payload=answer,
        token=allToken,
        tokenPrice=allPrice,
        senderNickname=userSendNickname,
        targets=hashtags,
        location_str=location.lower(),
         
    )
    #chenalID записывается без -100 в начале -1002010911633

# Запустите прослушивание новых сообщений
print('[OK]')
client.run_until_disconnected()
