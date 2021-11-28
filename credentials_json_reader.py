import json


def __load_json_data():
    with open('credentials.json') as json_file:
        return json.load(json_file)


def is_credentials_json_valid():
    try:
        __load_json_data()
        return True
    except:
        return False


def get_bot_token():
    json_data = __load_json_data()
    return json_data['BotToken']


def get_authorized_chat_ids():
    json_data = __load_json_data()
    return json_data['AuthorizedChatIds']

