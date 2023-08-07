import os
# from celery import shared_task


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