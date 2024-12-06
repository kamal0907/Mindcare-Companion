from flask import Flask, request, jsonify
import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
from tensorflow.keras.models import load_model
from flask_cors import CORS  # Make sure you have flask_cors imported

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # Allow all domains by default, or specify an origin if needed

# Load model and data
lemmatizer = WordNetLemmatizer()
model = load_model("chatbot_model.h5")
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

with open("intents.json") as file:
    data = json.load(file)

# Function to clean up user input
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Function to create a bag of words
def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

# Function to predict the intent
def predict_class(sentence):
    bow_vector = bow(sentence, words)
    res = model.predict(np.array([bow_vector]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]
    return return_list

# Function to get a response from the chatbot
def get_response(intents_list, intents_json):
    if not intents_list:
        return "I'm sorry, I didn't quite understand that. Could you rephrase?"

    tag = intents_list[0]["intent"]
    for intent in intents_json["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

# API endpoint for chatbot
@app.route('/chatbot', methods=['POST', 'OPTIONS'])
def chatbot_response():
    if request.method == 'OPTIONS':  # Handle preflight request
        response = jsonify({"message": "Preflight request handled"})
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow any origin
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Allow POST and OPTIONS methods
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow Content-Type header
        return response

    if request.method == 'POST':
        user_input = request.json.get("message")
        intents = predict_class(user_input)
        response = get_response(intents, data)
        return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)