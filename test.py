# import pandas as pd

# df = pd.read_csv('/Users/igorgerasimov/Downloads/data-1708074942033.csv')

# # print(df.to_string()) 
# for i in df.element:
#     print(i)


from chat import GPT
from promt import clasificatorPromt, historyList
gpt=GPT()

# a=gpt.asnwer_tools(historyList)
a =gpt.answer(system=clasificatorPromt, topic=historyList, temp=1)
print(a)
