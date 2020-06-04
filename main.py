from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import misc

from Porfirievich import Porfirievich

app = Flask(__name__)
sslify = SSLify(app)

global porf
porf = Porfirievich()

PROXYES = misc.proxies

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
    app.run(debug=True)