from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from operator import itemgetter

import ipywidgets as widgets

import re
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

import tiktoken
import sys
from loguru import logger
from pprint import pprint
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.output_parsers import JsonOutputToolsParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage


key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=key,)
                   
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


USERS_THREADS = {}

# @tool
# def count_emails(last_n_days: int) -> int:
#     """Multiply two integers together."""
#     return last_n_days * 2


# @tool
# def send_email(message: str, recipient: str) -> str:
#     "Add two integers."
#     return f"Successfully sent email to {recipient}."


@tool(return_direct=True)
def find_events(theme: str, location: str, date: str) -> str:
    "поиск мероприятий в базе по theme, location и date."
    return f"Вот что я нашел по вашему запросу: {theme} {location} {date}."


tools = [find_events]
modelTools = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0).bind_tools(tools)

def call_tool(tool_invocation: dict) -> Runnable:
    """Function for dynamically constructing the end of the chain based on the model-selected tool."""
    tool_map = {tool.name: tool for tool in tools}
    tool = tool_map[tool_invocation["type"]]
    return RunnablePassthrough.assign(output=itemgetter("args") | tool)

call_tool_list = RunnableLambda(call_tool).map()
# pprint(call_tool_list)
# pprint(modelTools)
# pprint(JsonOutputToolsParser())

chain = modelTools | JsonOutputToolsParser() | call_tool_list
# a = chain.invoke("сколько электронных писем я получил за последние 5 дней?")
# a = chain.invoke("отправь писмо на адрес datkclaw@yandex.ru")
# a = chain.invoke("Send sally@gmail.com an email saying 'What's up homie")
# a = chain.invoke("Есть что-нибудь на завтра в Москве по танцам?")
# history="""Клиент: привет, я хочу узнать о мероприятии на завтра 
# Ассистент: Здравствуйте, уточните пожалуйста, в каком городе вы хотите найти мероприятие?
# Клиент: Бали
# Ассистент: какая тема мероприятия вас интересует?
# Клиент: танцы"""
history="""Клиент: привет, я хочу узнать о мероприятии на завтра по танцам"""
# a=chain.invoke(
#     [
#         HumanMessage(
#             content="привет, я хочу узнать о мероприятии на завтра"
#         ),
#         AIMessage(content="Здравствуйте, уточните пожалуйста, в каком городе вы хотите найти мероприятие?"),
#         HumanMessage(content="Бали"),
#         AIMessage(content="какая тема мероприятия вас интересует?"),
#         HumanMessage(content="танцы"),
#     ]
# )
a=chain.invoke(
  history
)
print(a)

# 1/0
class GPT():
  modelVersion = ''
  def __init__(self,modelVersion:str = 'gpt-3.5-turbo-16k'):
    self.modelVersion = modelVersion
    pass

  

 
  def load_search_indexes(self, text:str = '') -> str:
    # Extract the document ID from the URL
    print('попали в load_serch_index')
    # match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    # if match_ is None:
    #     raise ValueError('Invalid Google Docs URL')
    # doc_id = match_.group(1)

    # Download the document as plain text
    # response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    # response.raise_for_status()
    # text = response.text

    return self.create_embedding(text)

  def load_prompt(self, 
                  url: str) -> str:
    # Extract the document ID from the URL
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    doc_id = match_.group(1)

    # Download the document as plain text
    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()
    text = response.text
    return f'{text}'


  def create_embedding(self, data):
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
      """Returns the number of tokens in a text string."""
      encoding = tiktoken.get_encoding(encoding_name)
      num_tokens = len(encoding.encode(string))
      return num_tokens

    source_chunks = []
    #splitter = CharacterTextSplitter(separator="\n", chunk_size=1524, chunk_overlap=0)
    splitter = CharacterTextSplitter(separator="==========", chunk_size=1024, chunk_overlap=300)

    for chunk in splitter.split_text(data):
      source_chunks.append(Document(page_content=chunk, metadata={}))

    # Создание индексов документа
    search_index = Chroma.from_documents(source_chunks, OpenAIEmbeddings(), )
    search_index.similarity_search
    count_token = num_tokens_from_string(' '.join([x.page_content for x in source_chunks]), "cl100k_base")
    print('\n ===========================================: ')
    print('Количество токенов в документе :', count_token)
    print('ЦЕНА запроса:', 0.0004*(count_token/1000), ' $')
    return search_index

  
  def answer_assistant(self,text, temp = 1, userID:int=0):
    global USERS_THREADS
    assistant ='asst_ljJQn6stjMsgIcGj4PkMvxnD' 
    # openai.('')
    # Upload a file with an "assistants" purpose
    lista=client.files.list(purpose='assistants')
    pprint(lista)
    fileCSV=lista.data[0]
    # client.files.delete(fileCSV.id)
    # fileCSV=lista.data[1]
    # client.files.delete(fileCSV.id)
    # fileCSV=lista.data[2]
    # client.files.delete(fileCSV.id)
    
    # 1/0
    #fileID file-dJgl5L10OuqjzYNxfXTQEoWP
    # fileCSV = client.files.create( 
    #   file=open("event.json", "rb"),
    #   purpose='assistants')
    # # 1/0
    try:
      thread=USERS_THREADS[userID]
    except:
      thread = client.beta.threads.create()
      USERS_THREADS[userID] = thread 
    # text = topic[-1]['content']
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
        file_ids=[fileCSV.id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant,
        instructions="",
        tools=[{"type": "retrieval"}],
        
    )

    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
     
    pprint(run.status)

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        logger.debug(run.status)

    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

    pprint(run.usage)    
    
    totalToken = run.usage['total_tokens']
    #https://openai.com/pricing
    tokenPrice = 0.002*(totalToken/1000)
    print(totalToken)
    # pprint(thread.__dict__)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
        )

    # logger.info(f'{messages=}')
    # logger.info(f'{messages.content=}')
    pprint(messages.data[0].content[0].text)
    pprint(messages.data[0].content[0])
    pprint(messages.data[0])
    logger.info(f'{messages.data[0].content[0].text.value=}')
    answerText = messages.data[0].content[0].text.value 
    return answerText, totalToken, tokenPrice
  

  #def answer(self, system, topic, temp = 1):    
  def answer(self, system, topic:list, temp = 1):
    """messages = [
      {"role": "system", "content": system},
      {"role": "user", "content": topic}
      ]
    """
    messages = [
      {"role": "system", "content": system },
      #{"role": "user", "content": topic}
      #{"role": "user", "content": context}
      ]
    messages.extend(topic)
    pprint(messages)
    completion = client.chat.completions.create(model=self.modelVersion,
        messages=messages,
        temperature=temp,)
        # stream=False)
    # pprint(completion.choices[0].message.content)
    # pprint(completion.usage.total_tokens)
    totalToken = completion.usage.total_tokens
    answerText =completion.choices[0].message.content

    allToken = f'{totalToken} токенов использовано всего (вопрос-ответ).'
    allTokenPrice = f'ЦЕНА запроса с ответом :{0.002*(totalToken/1000)} $'
    #return f'{completion.choices[0].message.content}\n\n{allToken}\n{allTokenPrice}', completion["usage"]["total_tokens"], 0.002*(completion["usage"]["total_tokens"]/1000)
    return f'{answerText}', totalToken, 0.002*(totalToken/1000)
  
  @logger.catch
  def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            #logger.error(f'{messages}')
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        
  def insert_newlines(self, text: str, max_len: int = 170) -> str:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) > max_len:
            lines.append(current_line)
            current_line = ""
        current_line += " " + word
    lines.append(current_line)
    return "\n".join(lines)

  
  def asnwer_tools(self, history:list, temp = 1):
    
    historyText=''
    for i in history:
      if i['role'] == 'user':
        historyText+= f"Клиент: {i['content']}\n"
      if i['role'] == 'system':
        historyText+= f"Ассистент: {i['content']}\n"

    answer=chain.invoke(
      historyText
    )
    print('========================================================')
    pprint(answer)
    
    answer=answer

    # if answer['type'] == 'find_events':
    #   answerArgs = answer["args"]
    # answerText = answer['output']

    return answer

  def answer_index(self, system, topic, history:list, search_index, temp = 1, verbose = 0):
    
    #Выборка документов по схожести с вопросом 
    docs = search_index.similarity_search(topic, k=2)
    if (verbose): print('\n ===========================================: ')
    message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\nМероприятие №{i+1}\n=====================' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
    if (verbose): print('message_content :\n ======================================== \n', message_content)

    systemMess = 'Данные, на основании которых нужно продолжить диалог:'
    messages = [
      {"role": "system", "content": system + f"{systemMess} {message_content}"},
      {"role": "user", "content": 'Диалог с клиентом, который нужно продолжить:'},
      #{"role": "user", "content": context}
      ]
    
    messages.extend(history)
    pprint(messages)
    # example token count from the function defined above
    if (verbose): print('\n ===========================================: ')
    if (verbose): print(f"{self.num_tokens_from_messages(messages, 'gpt-3.5-turbo-0301')} токенов использовано на вопрос")

    completion = client.chat.completions.create(model=self.modelVersion,
        messages=messages,
        temperature=temp)
    totalToken = completion.usage.total_tokens
    answerText =completion.choices[0].message.content
    if (verbose): print('\n ===========================================: ')
    if (verbose): print(f'{totalToken} токенов использовано всего (вопрос-ответ).')
    if (verbose): print('\n ===========================================: ')
    if (verbose): print('ЦЕНА запроса с ответом :', 0.002*(totalToken/1000), ' $')
    if (verbose): print('\n ===========================================: ')
    print('ОТВЕТ : \n', self.insert_newlines(answerText))

    answer = answerText
    #allToken = f'{completion["usage"]["total_tokens"]} токенов использовано всего (вопрос-ответ).'
    #allTokenPrice = f'ЦЕНА запроса с ответом :{0.002*(completion["usage"]["total_tokens"]/1000)} $'
    
    return f'{answer}', totalToken, 0.002*(totalToken/1000), docs

#    return answer
  
  def get_summary(self, history:list, 
                  promtMessage = 'Write a concise summary of the following and CONCISE SUMMARY IN RUSSIAN:',
                  temp = 0.3):    
    """messages = [
      {"role": "system", "content": system},
      {"role": "user", "content": topic}
      ]
    """
    #promtMessage = """Write a concise summary of the following and CONCISE SUMMARY IN RUSSIAN:"""
    messages = [
      {"role": "system", "content": promtMessage},
      #{"role": "user", "content": topic}
      #{"role": "user", "content": context}
      ]
    messages.extend(history)
    logger.info(f'answer message get_summary {messages}')
    completion = client.chat.completions.create(model=self.modelVersion,
    #model="gpt-3.5-turbo",
    messages=messages,
    temperature=temp)
    logger.info(f'{completion["usage"]["total_tokens"]=}')
    logger.info(f'{completion["usage"]=}')
    answer =completion.choices[0].message.content  
    logger.info(answer)
    roleAsnwer= {'role': 'user', 'content': answer}
    return roleAsnwer

  
if __name__ == "__main__":   
  gpt = GPT()
  a = gpt.answer_assistant('Привет, я хочу узнать о мероприятии на завтра', 1, 0)
  print(a)
