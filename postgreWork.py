from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON, ARRAY, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pprint import pprint

load_dotenv()
userName = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
print(f'{userName=}')
print(f'{password=}')
print(f'{db=}')
# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{userName}:{password}@localhost:5432/{db}')
# engine = create_engine('mysql://username:password@localhost/games')




 
# Определяем базу данных
Base = declarative_base()



class User(Base):
    __tablename__ = 'user'
    
    id = Column(BigInteger, primary_key=True)
    created_date = Column(DateTime)
    nickname = Column(String)
    targets = Column(ARRAY(String)) 
    all_token=Column(Float)
    all_token_price=Column(Float)
    payload=Column(String)
    model=Column(String)

class Post(Base):
    __tablename__ = 'post'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_date = Column(DateTime)
    post_id=Column(BigInteger)
    chat_id=Column(BigInteger)
    sender_nickname=Column(String)
    text=Column(String)
    date=Column(DateTime)
    location=Column(ARRAY(String))
    theme=Column(String)
    targets=Column(ARRAY(String)) 
    token=Column(Float)
    token_price=Column(Float)
    payload=Column(String) 
    

class Statistick(Base):
    __tablename__ = 'statistick'

    id=Column(BigInteger, primary_key=True, autoincrement=True)
    created_date=Column(DateTime)
    nickname=Column(String)
    query_text=Column(String)
    theme=Column(String)
    query_array=Column(ARRAY(String))
    targets=Column(ARRAY(String))


Base.metadata.create_all(engine)
# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

def add_new_user(userID:int, nickname:str):
    with Session() as session:
        newUser=User(
            id=userID,
            nickname=nickname,
            created_date=datetime.now(),
        )
        session.add(newUser)
        session.commit()

def add_new_post(postID:int, chatID:int, text:str, senderNickname:str=None, date:datetime=None, location:list[str]=None, theme:str=None, targets:list[str]=None, token:float=None, tokenPrice:float=None, payload:str=None):
    with Session() as session:
        newPost=Post(
            created_date=datetime.now(),
            post_id=postID,
            chat_id=chatID,
            text=text,
            date=date,
            location=location,
            theme=theme,
            targets=targets,
            token=token,
            token_price=tokenPrice,
            payload=payload,
            sender_nickname=senderNickname,
        )
        session.add(newPost)
        session.commit()



def update_targets_for_user(userID:int, targets:list[str]):
    with Session() as session:
        session.query(User).filter(User.id==userID)\
            .update({User.targets:targets})
        session.commit()    

def update_payload(userID:int, payload:str):
    with Session() as session:
        session.query(User).filter(User.id==userID)\
            .update({User.payload:payload}) 
        session.commit()

def update_model(userID:int, model:str):
    
    with Session() as session:
        session.query(User).filter(User.id==userID)\
            .update({User.model:model})
        session.commit()
        
def update_token_for_user(userID:int, token:float):
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        user.all_token+=token
        session.commit()

def update_token_price_for_user(userID:int, tokenPrice:float):
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        user.all_token_price+=tokenPrice
        session.commit()



def get_model(userID:int)->str:
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        return user.model

def get_posts():
    with Session() as session:
        posts=session.query(Post).filter(Post.token != None,
                                        #  Post.created_date==(Post.created_date>=(datetime.now()-timedelta(days=2)))).all()
                                         Post.created_date>=(datetime.now()-timedelta(days=2))).all()
        return posts

def get_payload(userID:int)->str:
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        return user.payload

def get_targets_for_user(userID)->list[str]:
    with Session() as session:
        user=session.query(User).filter(User.id==userID).one()
        return user.targets

def check_post(textPost:str)->bool:
    with Session() as session:
        posts=session.query(Post).filter(Post.text==textPost).all()
        if len(posts) > 0:
            return True
        else:
            return False
