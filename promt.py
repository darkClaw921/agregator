
clasificatorPromt="""
Я буду отправлять тебе диалоги Ассистента с Клиентом. Твоя задача - четко классифицировать, чего хочет клиент. Для классификации используй категории. Примерный список категорий: 
танцы,
медитация,
вечеринка,
музыка,
йога,
чайнаяцеремония,
бизнес,
мастеркласс,
бали,
маркетинг,
психология,
кино,
нетворкинг,
рисование,
встреча,
игра,
творчество,
отношения,
ретрит,
трансформация,
здоровье,
саундхилинг,
бизнесзавтрак,
искусство,
концерт,
релаксация,
девичник,
энерготерапия,
завтрак,
нумерология,
семинар,
продвижение,
энергия,
знакомства,
самопознание,
развитие,
Другое.

В ответе укажи ТОЛЬКО категории через запятую.

ПРИМЕР 1:
Клиент: привет
Ассистент: Привет! Я могу помочь тебе найти мероприятия, которые тебе интересны.
Клиент: йога,чайная церемония или медитация
Ассистент: Когда ты хочешь найти мероприятия?
Клиент: завтра
Ассистент: Где ты хочешь найти мероприятия?
Клиент: убуд

ТВОЙ ОТВЕТ: йога, медитация, чайнаяцеремония

ПРИМЕР 2:
Клиент: привет, хочу развлечься на выходных
ТВОЙ ОТВЕТ: танцы, вечеринка, музыка, концерт, игра, кино

ПРИМЕР 3:
Клиент: какие есть ближайшие бизнес-мероприятия?
ТВОЙ ОТВЕТ: бизнесзавтрак, нетворкинг, мастеркласс, бизнес

НЕ ДОБАВЛЯЙ НИЧЕГО ОТ СЕБЯ, ПИШИ ТОЛЬКО КАТЕГОРИИ.
в ответе укажи только категории через запятую и ничего больше.
Не продолжай диалог, только классифицируй, чего хочет клиент.

Вот диалог, который ты должен классифицировать:



"""

historyPromt="""
Клиент: привет
Ассистент: Привет! Я могу помочь тебе найти мероприятия, которые тебе интересны.
Клиент: йога,чайная церемония или медитация
Ассистент: Когда ты хочешь найти мероприятия?
Клиент: завтра
Ассистент: Где ты хочешь найти мероприятия?
Клиент: убуд
"""
historyPromt="""
Клиент: привет, когда ближайший бизнес-завтрак
Ассистент: Привет! Когда ты хотел бы посетить ближайший бизнес-завтрак?
Клиент: завтра
Клиент: а что еще есть по бизнесу?

"""
historyList = [
      {"role": "user", "content": 'привет'},
      {"role": "system", "content": "Привет! Я могу помочь тебе найти мероприятия, которые тебе интересны."},
      {"role": "user", "content": 'есть вечеринки или бизнез встречи?'},
      {"role": "system", "content": "Когда бы ты хотел пойти на мероприятия?"},
      {"role": "user", "content": 'сегодня'},
      {"role": "system", "content": "Где ты хочешь найти мероприятия?"},
      {"role": "user", "content": 'москва'}
      
      ]
# привет
# развлечения на выходные
# что есть в выходные?
# 24-25
# а в пятницу?
# привет, когда ближайший бизнес-завтрак
# Привет! Когда ты хотел бы посетить ближайший бизнес-завтрак?
# завтра
# а что еще есть по бизнесу?