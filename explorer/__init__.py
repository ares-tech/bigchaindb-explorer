import hashlib
import binascii

from flask import Flask
from flask import request, make_response, jsonify, url_for
from flask import render_template, redirect
import requests

application = Flask(__name__, instance_relative_config=True)
application.config.from_pyfile("default.py")
application.config.from_pyfile("config.py")

API_KEY = application.config["API_KEY"]
dk = hashlib.pbkdf2_hmac('sha256', API_KEY, b'salt', 100000)
API_KEY_HASHED = binascii.hexlify(dk)


@application.route("/", methods=["GET", "POST"])
def index():
    txid = request.values.get("txid")
    return render_template("index.html", txid=txid)


@application.route("/api/v1/transactions/<txid>")
def get_transaction(txid):
    global API_KEY_HASHED
    client_api_key = request.headers.get("X-Api-Key", "")
    if str.encode(client_api_key) != API_KEY_HASHED:
        return redirect(url_for('.index', txid=txid))

    if txid == 'None':
        return jsonify({})

    BIGCHAINDB_HOST = "http://{}:{}".format(application.config['BIGCHAINDB'].get('host', 'localhost'),
                                            application.config['BIGCHAINDB'].get('port', 9984))
    api_url = "/api/v1/transactions/{}".format(txid)
    url = BIGCHAINDB_HOST + api_url
    application.logger.info("bigchaindb's endpoint is {}".format(url))
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "server is down"})

    if resp.status_code >= 200 and resp.status_code < 300:
        return resp.text
    else:
        return jsonify(resp.text)
