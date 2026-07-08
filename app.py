"""
=========================================================
 SIMPLE AI CHATBOT WEBSITE - Python Mini Project
=========================================================
This is a simple website made using Flask.
It connects to open source / free AI chatbot APIs
(like Google Gemini or OpenAI GPT) and shows the
reply on a webpage.

Only simple Python topics are used here:
- if / elif / else
- dictionaries
- tuples
- lists
- functions
- loops (inside the HTML template)

How it works (in simple words):
1. User types a message on the webpage and picks a chatbot.
2. The message is sent to our Flask server.
3. Our server sends that message to the real AI's API
   using the "requests" library.
4. The AI sends back an answer.
5. We show that answer back on the webpage.
=========================================================
"""

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# ---------------------------------------------------------
# STEP 1: Store information about each chatbot in a dictionary
# key   = name of the chatbot
# value = tuple containing (API URL, short description)
# ---------------------------------------------------------
chatbot_info = {
    "gemini": (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "Google's Gemini AI (free tier available)"
    ),
    "openai": (
        "https://api.openai.com/v1/chat/completions",
        "OpenAI's GPT model (needs paid API key)"
    ),
}


# ---------------------------------------------------------
# STEP 2: Put your own API keys here.
# You get these keys for free by signing up on:
#   Gemini -> https://aistudio.google.com/app/apikey
#   OpenAI -> https://platform.openai.com/api-keys
# ---------------------------------------------------------
API_KEYS = {
    "gemini": "PUT_YOUR_GEMINI_API_KEY_HERE",
    "openai": "PUT_YOUR_OPENAI_API_KEY_HERE",
}


# ---------------------------------------------------------
# STEP 3: This list stores the whole chat history.
# Each entry is a tuple: (who_said_it, message)
# Example: ("You", "Hello!"), ("gemini", "Hi, how can I help?")
# ---------------------------------------------------------
conversation_history = []


# ---------------------------------------------------------
# STEP 4: Functions that actually talk to each AI's API
# ---------------------------------------------------------

def call_gemini(user_message, api_key):
    """Sends the user message to Gemini API and returns the reply text."""

    url = chatbot_info["gemini"][0] + "?key=" + api_key
    headers = {"Content-Type": "application/json"}

    # This is the format Gemini's API expects
    data = {
        "contents": [
            {"parts": [{"text": user_message}]}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        # Try to dig into the JSON reply safely
        if "candidates" in result and len(result["candidates"]) > 0:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = "Gemini did not send a proper answer."
    else:
        reply = "Error talking to Gemini. Status code: " + str(response.status_code)

    return reply


def call_openai(user_message, api_key):
    """Sends the user message to OpenAI API and returns the reply text."""

    url = chatbot_info["openai"][0]
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_message}
        ],
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "OpenAI did not send a proper answer."
    else:
        reply = "Error talking to OpenAI. Status code: " + str(response.status_code)

    return reply


def get_bot_reply(bot_name, user_message):
    """
    Decides which chatbot function to call.
    This is where simple if / elif / else logic is used.
    """

    api_key = API_KEYS.get(bot_name, "")

    if api_key == "" or "PUT_YOUR" in api_key:
        reply = "Please add your API key for '" + bot_name + "' inside app.py first!"

    elif bot_name == "gemini":
        reply = call_gemini(user_message, api_key)

    elif bot_name == "openai":
        reply = call_openai(user_message, api_key)

    else:
        reply = "Sorry, this chatbot is not supported yet."

    return reply


# ---------------------------------------------------------
# STEP 5: Flask routes (these decide what shows on the website)
# ---------------------------------------------------------

@app.route("/")
def home():
    # list() turns the dictionary keys into a list of bot names
    bot_names = list(chatbot_info.keys())
    return render_template("index.html", bots=bot_names, info=chatbot_info, history=conversation_history)


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")
    selected_bot = request.form.get("bot")

    # Simple validation using if / else
    if user_message is None or user_message.strip() == "":
        bot_reply = "Please type something before sending!"
    else:
        bot_reply = get_bot_reply(selected_bot, user_message)

    # Save this exchange in our history list as tuples
    conversation_history.append(("You", user_message))
    conversation_history.append((selected_bot, bot_reply))

    bot_names = list(chatbot_info.keys())
    return render_template("index.html", bots=bot_names, info=chatbot_info, history=conversation_history)


@app.route("/clear")
def clear_chat():
    # empty the list to clear chat history
    conversation_history.clear()
    bot_names = list(chatbot_info.keys())
    return render_template("index.html", bots=bot_names, info=chatbot_info, history=conversation_history)


# ---------------------------------------------------------
# STEP 6: Run the website
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
