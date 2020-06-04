from flask import Flask
from flask import request
from flask import jsonify
# from flask_sslify import SSLify
import requests
import misc

from Porfirievich import Porfirievich

app = Flask(__name__)
# sslify = SSLify(app)

global porf
porf = Porfirievich()

PROXYES = misc.proxies
token = misc.token

def webhook(method, site=""):
    url = ""
    if method == "setWebhook" and site:
        url = f"https://api.telegram.org/bot{token}/setWebhook?url=" + site
    elif method == "deleteWebhook":
        url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    return requests.get(url, proxies=PROXYES)

@app.route('/', methods=['POST', 'GET'])
def index():
    global porf
    if request.method == 'POST':
        r = request.get_json()
        porf.questionHandler(r)
        return jsonify(r)
    else:
        return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    # print(webhook("deleteWebhook"))
    # print(webhook("setWebhook", "https://4fe71826cac2.ngrok.io"))
    app.run(debug=True)

# "https://api.telegram.org/bot1235053339:AAGTm95xRlCONKi0e8e5D-IG2JVo1TXFFWU/setWebhook?url=https://00mrx00.pythonanywhere.com"