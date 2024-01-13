from flask import Flask, jsonify
from data_helper import get_random_words

app = Flask(__name__)

@app.route("/api/get-random-words", methods=["GET"])
def get_random_words_route():
    word_list = get_random_words()
    return jsonify(word_list)

if __name__ == "__main__":
    app.run(debug=True)
