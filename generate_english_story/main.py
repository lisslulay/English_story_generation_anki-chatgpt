import openai
import os
from constant import *
from reader import *

import requests
import json

# 连接到 Anki
url = "http://localhost:8765"
deck_name = "try"
model_name = "KaTeX and Markdown Basic"

# 设置 OpenAI API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

# 定义要发送给 ChatGPT 模型的输入
input_vocabularies = read_file(VOCABULARY_FILE, GROUP_NUM)

count = 0
# 发送请求，并打印模型的回复
for vocabulary in input_vocabularies:
    count += 1
    prompt = f"{count}: {ENGLISH_STORY} {vocabulary[0]}"
    print(f"prompt:\n{prompt}")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.1,
    )

    message = response.choices[0].text.strip()
    print(f"{message}\n")


    fields = {
        "Front":f"{message}",
        "单词": f"```\n{vocabulary[1]}```"
    }
    
    payload ={
    "action": "addNote",
    "version": 6,
    "params":{
        "note":{
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "options":{
                "allowDuplicate": False
            }
        }
    }
    }
    response = requests.post(url, data=json.dumps(payload))
    print(response.json())

