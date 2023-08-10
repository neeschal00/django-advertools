#!/bin/bash

#activate venv
source venv/bin/activate

# download stopwords for nltk
python -m nltk.downloader stopwords

# download punkt package of nltk
python -m nltk.downloader punkt

# download punkt package of nltk
python -m nltk.downloader averaged_perceptron_tagger
