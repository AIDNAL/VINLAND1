# Simple AI Chatbot Website (Python Mini Project)

A basic website, built only with Flask and simple Python (if/else, dictionaries,
tuples, lists), that connects to real AI chatbot APIs like **Google Gemini** or
**OpenAI GPT** and shows their replies on screen.

## Project Files
```
ai_chatbot_website/
├── app.py                 # Main server code (all the logic lives here)
├── templates/
│   └── index.html          # The webpage itself
├── requirements.txt        # Libraries needed
└── README.md
```

## How to Run It

### 1. Install Python libraries
Open a terminal in this folder and run:
```
pip install -r requirements.txt
```

### 2. Get a free API key
- **Gemini (recommended, free tier):** go to https://aistudio.google.com/app/apikey
  and click "Create API key".
- **OpenAI (paid):** go to https://platform.openai.com/api-keys

### 3. Add your API key
Open `app.py` and find this part near the top:
```python
API_KEYS = {
    "gemini": "PUT_YOUR_GEMINI_API_KEY_HERE",
    "openai": "PUT_YOUR_OPENAI_API_KEY_HERE",
}
```
Replace the text with your real key(s), for example:
```python
API_KEYS = {
    "gemini": "AIzaSyD-your-real-key-here",
    "openai": "PUT_YOUR_OPENAI_API_KEY_HERE",
}
```
(You only need to fill in the key for the chatbot you plan to use.)

### 4. Run the website
```
python app.py
```

### 5. Open it in your browser
Go to:
```
http://127.0.0.1:5000
```

Type a message, pick a chatbot from the dropdown, and hit Send!

## How the Code Works (Simple Explanation)

1. **Dictionary** `chatbot_info` stores each chatbot's API address and description.
2. **Dictionary** `API_KEYS` stores your secret keys.
3. **List of tuples** `conversation_history` remembers every message as
   `(sender, message)` so it can be displayed on the page.
4. Function `get_bot_reply()` uses simple `if / elif / else` statements to
   decide which chatbot function to call.
5. Functions `call_gemini()` and `call_openai()` use the `requests` library
   to send your message to the real AI over the internet and get a reply.
6. Flask `@app.route()` decorators connect these functions to actual web pages
   (`/`, `/chat`, `/clear`).

## Adding Another Chatbot Later
To add a new chatbot (say, an open-source one running locally), just:
1. Add a new entry to the `chatbot_info` dictionary.
2. Add a new entry to `API_KEYS`.
3. Write a new `call_yourbot()` function.
4. Add one more `elif` line inside `get_bot_reply()`.

That's it — no fancy Python features needed, just the basics!
