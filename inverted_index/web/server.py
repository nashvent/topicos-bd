import flask
import json 
from flask import request, jsonify
import pandas as pd
from flask_cors import CORS

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

f = open('../output/index.json',) 
data = json.load(f)

f2 = open('../output/index_tf_idf.json',) 
data_tf = json.load(f2)

stories = pd.read_csv('../data/stories.csv', sep=',',header=None)
title_stories = pd.read_csv('../data/db_books.csv', sep=',',header=None)
#  METHODS 
def sortArrayByValue(data):
    data.sort(key=lambda x: x["value"], reverse = True)
    return data

def findWordInData(word):
    lemmaWord = lemmatizer.lemmatize(word)
    if lemmaWord in data:
        return {'word':lemmaWord, 'data': sortArrayByValue(data[lemmaWord]) }
    else:
        return {'word':lemmaWord, 'data':[]}

def findWordInDataTfIDF(word):
    lemmaWord = lemmatizer.lemmatize(word)
    if lemmaWord in data_tf:
        return {'word':lemmaWord, 'data': sortArrayByValue(data_tf[lemmaWord]) }
    else:
        return {'word':lemmaWord, 'data':[]}


def findPhraseInData(phrase):
    words = phrase.split(" ")
    result = []
    for word in words:
        result.append(findWordInData(word))
    return result

def findKeyInStories(key):
    for i in range(len(stories[0])):
        if(stories[0][i]==key):
            return {
                "title":title_stories[1][i],
                "text":stories[1][i]
            } 
    return None

@app.route('/', methods=['GET'])
def home():
    return jsonify({'data': "Server success init"})

@app.route('/find/word/invertindex/<word>', methods=['GET'])
def findByWordInvertIndex(word):
    return jsonify(findWordInData(word))

@app.route('/find/word/tfidf/<word>', methods=['GET'])
def findByWordTfIdf(word):
    return jsonify(findWordInDataTfIDF(word))

@app.route('/find/phrase', methods=['POST'])
def findByPhrase():
    content = request.get_json()
    if 'phrase' in content:
        return jsonify(findPhraseInData(content["phrase"]))
    return jsonify({'error':'Missing phrase'})

@app.route('/find/file/<key>', methods=['GET'])
def findFileByKey(key):
    return jsonify(findKeyInStories(key))



app.run()
