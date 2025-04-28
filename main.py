import pandas as pd
from twilio.rest import Client
import os
from dotenv import load_dotenv


load_dotenv()
ACCOUNT_SID = os.getenv('account_sid')
AUTH_TOKEN = os.getenv("auth_token")


def get_data_from_excel(filename):
    data = pd.read_excel(filename)
    return {"phone":list(data['Номер телефона']),"user_name":list(data['ФИО']), "game_name":list(data['Что нужно вставить в главынй текст'])}


def send_message(data:dict[str,list]):
    if not all(key in data.keys() for key in ['phone', 'user_name', 'game_name']):
        raise Exception("Invalid format data!")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for user in zip(list(data.values())[0], list(data.values())[1], list(data.values())[2]):
        phone = str(user[0])
        if '+380' not in phone:
            phone = f'+380{phone}'
        elif '+38' not in phone:
            phone = f'+38{phone}'
        elif '+'not in phone:
            phone = f'+{phone}'

        client.messages.create(
        from_='+13198204912',
        body=f'Вітаю, {user[1]}! Ви придбали гру в Steam під назвою {user[2]}. Бажаю вам приємної гри!',
        to=phone
        )
        break


if __name__ == "__main__":
    send_message(get_data_from_excel('data/Book.xlsx'))