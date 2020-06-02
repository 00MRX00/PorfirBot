import requests
import json
from time import sleep

import misc


class Porfirievich:
    def __init__(self):
        self.__URL = 'https://api.telegram.org/bot' + misc.token + '/'
        self.__PROXYES = misc.proxies
        self.__hystory = {
            "lastUpdateId": 0,
            "messages": []
        }

    def getUpdates(self):
        url = self.__URL + 'getUpdates'
        responce = requests.get(url, proxies=self.__PROXYES)
        return responce.json()

    def resultsToFile(self, fileName, text):
        with open(f"{fileName}.json", "w", encoding="utf-8") as file:
            json.dump(text, file, indent=4, ensure_ascii=False)

    def getMessage(self):
        data = self.getUpdates()
        lastObject = data["result"][-1]
        currentUpdateId = lastObject["update_id"]

        if self.__hystory["lastUpdateId"] != currentUpdateId:
            self.__hystory["lastUpdateId"] = currentUpdateId
            self.__hystory["messages"].append(lastObject)
            return {
                "chatId": lastObject["message"]["chat"]["id"],
                "messageText": lastObject["message"]["text"]
            }
        else:
            return None

    def sendMessage(self, chatId, text="Wait a second? please..."):
        url = self.__URL + 'sendMessage'
        data = {
            "chat_id": chatId,
            "text": text
        }
        requests.get(url, params=data, proxies=self.__PROXYES)

    def questionHandler(self, question):
        chatId = question["chatId"]
        messageText = question["messageText"]
        if messageText == "/porf":
            self.sendMessage(chatId, "Придумайте начало истории...")

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
            self.sendMessage(chatId, answer)
        else:
            pass


def main():
    porf = Porfirievich()
    while True:
        question = porf.getMessage()
        if question != None:
            porf.questionHandler(question)
        else:
            continue
    sleep(2)


if __name__ == '__main__':
    main()
