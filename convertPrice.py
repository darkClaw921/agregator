import requests

def convert_ars_to_rub(amount):
    # response = requests.get('https://api.exchangerate-api.com/v4/latest/ARS')
    # data = response.json()
    # try:
        # rub_rate = data['rates']['RUB']
    # except:
        # print(response.text)
        # 1/0
        # rub_rate = 0
    rub_rate = 0.11
    rub_amount = amount * rub_rate
    return round(rub_amount,2)

# Пример использования
# ars_amount = 1
# print(float(ars_amount))
# rub_amount = convert_ars_to_rub(ars_amount)
# print(f'{ars_amount} Argentine Peso is equal to {rub_amount} Russian Ruble')