import requests
import json
import urllib.parse
import os

# AnkiConnect API相关配置
ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "英语"
MODEL_NAME = "KaTeX and Markdown Basic"
FIELD_NAME_FRONT = "Front"
FIELD_NAME_BACK = "Back"

# Google Translate API相关配置
google_api_key = os.getenv("GOOGLE_API_KEY")

def translate_text(text, source_language, target_language):
    url = "https://translation.googleapis.com/language/translate/v2?key=" + google_api_key
    url += "&source=" + urllib.parse.quote(source_language)
    url += "&target=" + urllib.parse.quote(target_language)
    url += "&q=" + urllib.parse.quote(text)

    response = requests.get(url)
    if response.status_code == 200:
        translation = json.loads(response.text)['data']['translations'][0]['translatedText']
        return translation
    else:
        return None
    

# 连接到Anki
def connect_to_anki():
    try:
        response = requests.get(ANKI_CONNECT_URL)
        if response.status_code == 200:
            return True
        else:
            print("AnkiConnect is not running")
            return False
    except requests.exceptions.RequestException:
        print("AnkiConnect is not running")
        return False

# 获取指定Deck的所有卡片
def get_deck_cards(deck_name):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'deck:"{DECK_NAME}" note:"{MODEL_NAME}" "back:"'
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    return response['result']


# 获取指定卡片的内容
def get_card(card_id):
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": [card_id]
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    if response.status_code == 200:
        card_data = json.loads(response.text)
        return card_data
    else:
        return None


# 给卡片添加一个字段的内容
def add_field_to_card(card_id, field_name, field_value):
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": card_id,
                "fields": {
                    field_name: field_value
                }
            }
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    return response['result']

# 翻译指定Deck中所有卡片的Front字段内容
def translate_deck_front_to_back(deck_name, source_language, target_language):
    cards = get_deck_cards(deck_name)
    print(cards)
    for card_id in cards:
        print(card_id)
        card = get_card(card_id)["result"][0]
        if card is not None:
            front_text = card['fields'][FIELD_NAME_FRONT]['value']
            print(front_text)
            back_text = translate_text(front_text, source_language, target_language)
            print(back_text)
            result = add_field_to_card(card_id, FIELD_NAME_BACK, back_text)
            print(result)

# 运行程序
if connect_to_anki():
    translate_deck_front_to_back(DECK_NAME, "en", "zh-CN")

