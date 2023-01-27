import flask
from flask import request, jsonify, Blueprint
import logging
from slack_client import SlackClient

app = flask.Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.DEBUG)
app.config["DEBUG"] = True

@app.route("/api/v1/translate",  methods = ['POST'])
def api_translate():
    try:
        req = request.get_json()
        app.logger.info(req)
        if (req.get("challenge") is not None) and (len(req.get("challenge")) > 0):
            return jsonify(req.get("challenge"))
        client = SlackClient(logger=app.logger)
        translated=client.onReactionAdded(req)
        return jsonify(translated)
    except Exception as e:
        app.logger.info("AAAAAAA")
        app.logger.error(e)
    return ""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
