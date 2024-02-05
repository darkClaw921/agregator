from loguru import logger
from bitrix24 import Bitrix24
from telethon import TelegramClient, sync, events
from pprint import pprint
#webhook = 'https://dc33.bitrix24.ru/rest/38/wy7jmc5gzx0ekc2f/' # Прод
webhook='https://dc33.bitrix24.ru/rest/46/kpsyg6gs85b7vosj/'

bit = Bitrix24(webhook)
# где-то на сервере logan Wayne
#api_id = 16094438
#api_hash = '4495fd569584327f8f31d578bb293e24'
api_id =16763158 
api_hash = '91f00824c0f2482633a5ac986176b742'

@logger.catch
def connect_telegram(api_id: int, api_hash: str):
    
    client = TelegramClient('session_name', api_id, api_hash)
    return client

@logger.catch
def take_url(message:dict) -> str:
    """Для преобразования в словарь .to_dict()"""
    strUrl = '\n'
    for content in message['entities']:
        try:
            strUrl += content['url']+'\n'
        except:
            continue
    return strUrl    
    


@logger.catch
def get_last_message_id_chenal(chenalName: str):
    
    client = connect_telegram(api_id, api_hash)
    #иногда может приходить собщение вида %DC%%5BC
    #нужно заменить все символы % в строке на что-то другое символ = %25
    chenalName = [-1002010911633] 
    @client.on(events.NewMessage(chats=chenalName))
    async def normal_handler(event):
        print('message')
        message = event.message.text
        print(message)
        message = message.replace('%','%25')
        #urlMessage = take_url(event.message.to_dict())
        #message = event.message.to_dict()['message']
        # bit.callMethod('log.blogpost.add',POST_MESSAGE = f'{message}')
        print(message)
    client.start()
    client.run_until_disconnected()

@logger.catch
def main():
    # get_last_message_id_chenal('БалиЧат Мероприятия | Балифорум')
    get_last_message_id_chenal('Герасимова и Игорь Новый')
    
    print('[Fail] востаноление потока')
if __name__ == '__main__':
    print('[OK]')
    main()
    # while True:
    #     try:

    #         main()
    #     except:
    #         print('следующая итерация')

