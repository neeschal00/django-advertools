import os

# from celery import shared_task
import re
from collections import Counter
from advertools import stopwords


import nltk


def delete_existing_files():
    if os.path.exists("output/crawl_output.jl"):
        os.remove("output/crawl_output.jl")
    if os.path.exists("logs/crawlLogs/output_file.log"):
        os.remove("logs/crawlLogs/output_file.log")


def validate_links(links):
    if not links.startswith("http"):
        raise ValueError("The URL is invalid")
        return False
    else:
        return True


def extract_stopwords(text):
    stop_words = set(stopwords["english"])
    words = text.split()
    stopwords_found = [word for word in words if word.lower() in stop_words]
    return stopwords_found


def extract_words(text):
    words = re.findall(r"\b\w+\b", text)
    return words


def get_word_count(text):
    words = re.findall(r"\b\w+\b", text)
    return len(words)


def extract_keywords(body_text):
    pattern = r"[^a-zA-Z0-9@\s]"
    body_text = re.sub(pattern, "", body_text)
    numPattern = r"\d+"
    body_text = re.sub(numPattern, "", body_text)
    body_text = re.sub(r"\b\w\b", "", body_text)
    whiteSpacePattern = r"\s+"
    body_text = re.sub(whiteSpacePattern, " ", body_text)
    for text in stopwords["english"]:
        body_text = body_text.replace(" " + text.lower() + " ", " ")
    keywords = body_text.split()
    # keywords = dict(Counter(keywords))
    # keywords = sorted(keywords.items(),key=lambda x: x[1])[::-1]
    return keywords


def text_readability(text):
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)

    num_sentences = len(sentences)
    num_words = len(words)
    num_syllables = 0

    for word in words:
        num_syllables += syllable_count(word)

    if num_sentences == 0:
        num_sentences = 1

    readability_score = (
        206.835
        - 1.015 * (num_words / num_sentences)
        - 84.6 * (num_syllables / num_words)
    )
    return readability_score


def syllable_count(word):
    vowels = "AEIOUaeiou"
    syllables = 0
    prev_char = None

    for char in word:
        if char in vowels and (prev_char is None or prev_char not in vowels):
            syllables += 1
        prev_char = char

    if word.endswith("e"):
        syllables -= 1

    if syllables == 0:
        syllables = 1

    return syllables


"""

import re
import json
from sklearn.ensemble import RandomForestClassifier

# Load config file
with open('page_type_config.json') as f:
    config = json.load(f)
    
# Compile regex patterns    
patterns = {label: re.compile(pattern)  
            for label, pattern in config['regex_patterns'].items()}
            
# Load pre-trained model   
clf = RandomForestClassifier()
clf.load('page_type_model.pkl') 

features = config['features']
vectorizer = config['vectorizer']

def classify_page_type(path):

  # Regex based classification
  for label, pattern in patterns.items():
    if pattern.search(path):
      return label
      
  # ML based classification
  vectorized_path = vectorizer.transform([features(path)])
  prediction = clf.predict(vectorized_path)[0]
  
  return prediction
  
# Sample usage
page_type = classify_page_type('/product/123')
print(page_type)
"""
