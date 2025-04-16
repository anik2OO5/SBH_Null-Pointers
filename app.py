from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.corpus import wordnet as wn
import re

app = Flask(__name__)
CORS(app)

# Load the word list
def load_word_list():
    with open('sowpods.txt', 'r') as file:
        return [line.strip().lower() for line in file]

word_list = load_word_list()

# Get synonyms using WordNet
def get_synonyms(clue):
    synonyms = set()
    for syn in wn.synsets(clue):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace('_', ' '))
    return list(synonyms)

# Match pattern using regex
def match_pattern(word_list, pattern):
    regex_pattern = pattern.replace("_", ".").lower()
    return [word for word in word_list if re.fullmatch(regex_pattern, word.lower())]

# Combine both: clue interpretation + pattern match
@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    clue = data.get('clue', '')
    pattern = data.get('pattern', '')

    clue_words = get_synonyms(clue)
    possible_words = match_pattern(word_list, pattern)
    final_words = [word for word in possible_words if word in clue_words]

    #print("Clue words (synonyms):", clue_words)
    #print("Pattern matches:", possible_words)
    #print("Final matches:", final_words)

    return jsonify({
        'matches': final_words,
        'synonyms': clue_words,
        'pattern_matches': possible_words
    })

if __name__ == '__main__':
    app.run(debug=True)
