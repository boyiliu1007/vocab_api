from flask import Flask, jsonify
from data_helper import get_random_words, get_example

app = Flask(__name__)

@app.route("/api/get-random-words", methods=["GET"])
def get_random_words_route():
    word_list = get_random_words()
    return jsonify(word_list)

@app.route("/api/get-example/<word>", methods=["GET"])
def get_example_route(word):
    example = get_example(word)
    return jsonify(example)

if __name__ == "__main__":
    app.run(debug=True)
