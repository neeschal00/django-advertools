import os
# from celery import shared_task
import re
from collections import Counter
from advertools import stopwords

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
    stop_words = set(stopwords['english'])
    words = text.split()
    stopwords_found = [word for word in words if word.lower() in stop_words]
    return stopwords_found


def extract_words(text):
    words = re.findall(r'\b\w+\b', text)
    return words

def getKeywords(body_text):    
    pattern = r'[^a-zA-Z0-9@\s]'
    body_text = re.sub(pattern,"",body_text)
    numPattern = r'\d+'
    body_text = re.sub(numPattern,"",body_text)
    body_text = re.sub(r'\b\w\b', '', body_text)
    whiteSpacePattern = r'\s+'
    body_text = re.sub(whiteSpacePattern," ",body_text)
    for text in stopwords["english"]:
        body_text = body_text.replace(" "+text.lower()+" "," ")
    keywords = body_text.split()
    keywords = dict(Counter(keywords))
    keywords = sorted(keywords.items(),key=lambda x: x[1])[::-1]

    return keywords


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