from telethon import TelegramClient, events
from chat import GPT, promtPreparePost
from pprint import pprint
import postgreWork
from helper import check_pattern_count
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
              -1002010911633,
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
    chenalID=event.message.chat.id
    text=event.message.text

    userSendID=event.message.from_id
    userSendNickname=event.message.sender.username
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
    if chenalID == 2010911633:
        await client.send_message(-1002010911633, message='Это мероприятие!',reply_to=event.message)
        
    messagesList = [
      {"role": "user", "content": text}
      ]
    url='https://docs.google.com/document/d/1riRchaMaJC27ikxBx_02W2Z7GANDnFswzTUHy49qaqI/edit?usp=sharing'
    promt=gpt.load_prompt(url)
    
    dateNow = datetime.now().strftime("%d.%m.%Y")
    
    promt=promt.replace('[dateNow]',dateNow)
    answer, allToken, allPrice = gpt.answer(promt,messagesList)
    pprint(answer)
    if chenalID == 2010911633:
        await client.send_message(-1002010911633, message=answer,reply_to=event.message)

    # messageID=event.message.id
    # chenalID=event.message.chat.id
    postIsAdd=postgreWork.check_post(text)
    
    if postIsAdd: return 0
    
    postgreWork.add_new_post(
        postID=messageID,
        chatID=chenalID,
        text=text,
        payload=answer,
        token=allToken,
        tokenPrice=allPrice,
        senderNickname=userSendNickname, 
    )
    #chenalID записывается без -100 в начале -1002010911633

# Запустите прослушивание новых сообщений
print('[OK]')
client.run_until_disconnected()
