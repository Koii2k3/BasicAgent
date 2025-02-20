import re
import requests


def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
        return f"Definition of '{word}': {meaning}"
    return "Not found the word in the dictionary."


def extract_keywords(text):
    words = text.split()

    keywords = {}
    for word in words:
        if word in keywords:
            keywords[word] += 1
        else:
            keywords[word] = 1

    keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, _ in keywords if len(word) > 5]
    return f"Keywords in the text: {', '.join(keywords[:5])}." if keywords else "No keywords found."


known_actions = {
    "define_word": define_word,
    "extract_keywords": extract_keywords
}
