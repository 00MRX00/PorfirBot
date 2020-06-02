import requests
import json
from time import sleep

import misc

URL = 'https://api.telegram.org/bot' + misc.token + '/'
PROXYES = misc.proxies

global lastUpdateId
lastUpdateId = 0

def getUpdates():
    url = URL + 'getUpdates'
    responce = requests.get(url, proxies=PROXYES)
    return responce.json()


def resultsToFile(fileName, text):
    with open(f"{fileName}.json", "w", encoding="utf-8") as file:
        json.dump(text, file, indent=4, ensure_ascii=False)


def getMessage():
    data = getUpdates()
    lastObject = data["result"][-1]
    currentUpdateId = lastObject["update_id"]
    
    global lastUpdateId
    if lastUpdateId != currentUpdateId:
        lastUpdateId = currentUpdateId
        return {
            "chatId": lastObject["message"]["chat"]["id"],
            "messageText": lastObject["message"]["text"]
        }
    else:
        return None


def sendMessage(chatId, text="Wait a second? please..."):
    url = URL + 'sendMessage'
    data = {
        "chat_id": chatId,
        "text": text
    }
    requests.get(url, params=data, proxies=PROXYES)


def questionHandler(question):
    chatId = question["chatId"]
    messageText = question["messageText"]
    if messageText == "/porf":
        sendMessage(chatId, "Придумайте начало истории...")
        
        url = "https://models.dobro.ai/gpt2/medium/"
        message = "Привет, как дела?"
        text = {
            "prompt": message,
            "num_samples": 4,
            "length": 30
        }
        data = {
            "chat_id": chatId,
            "text": json.dumps(text)
        }
        headers = {
            "Content-Type": "application/json"
        }
        responce = requests.post(url, data=data["text"], headers=headers)
        answer = ""
        for i in range(3, -1, -1):
            answer += f"[{abs(i-3)}] - {message + responce.json()['replies'][i]}\n\n"
        sendMessage(chatId, answer)
    else:
        pass


def main():
    while True:
        question = getMessage()
        if question != None:
            questionHandler(question)
        else:
            continue
    sleep(2)


if __name__ == '__main__':
    main()
