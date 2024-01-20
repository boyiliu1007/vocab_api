from flask import Flask, jsonify
from data_helper import get_random_words, get_example
import random

app = Flask(__name__)

@app.route("/api/get-random-words", methods=["GET"])
def get_random_words_route():
    word_list = get_random_words()
    random_index = random.randint(0, 3)
    print(word_list[random_index]['word'])
    example, res = get_example(word_list[random_index]['word'], word_list[random_index]['pos'])
    dict = {"wordList": word_list, "question": example, "answer": random_index, "allData":res}
    return jsonify(dict)

@app.route("/api/get-example/<word>/<ptos>", methods=["GET"])
def get_example_route(word, ptos):
    example = get_example(word, ptos)
    return jsonify(example)

if __name__ == "__main__":
    app.run(debug=True)
