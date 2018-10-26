import re
import string

import nltk
from bs4 import BeautifulSoup


def extract_text(html):
    """Remove html markup, js and css from document"""
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = ''.join(soup.find('body').find_all(text=True))
    return text


def prepocess_text(text):
    """Remove unwanted symbols from text"""
    punctuation_table = str.maketrans("", "", string.punctuation)
    text = text.translate(punctuation_table).lower()
    return text


def count_words(text):
    """ Tokenize, tags POS and count verbs and nouns"""
    tokenizer = nltk.RegexpTokenizer(r'\w\w+')
    tokens = tokenizer.tokenize(text)
    tagged_tokens = [w[0] for w in nltk.pos_tag(tokens, tagset='universal') if w[1] in ['VERB', 'NOUN']]
    freq_dist = nltk.FreqDist(tagged_tokens)
    return dict(freq_dist.most_common(100))


def count_words_in_html(html):
    """ Just wraps `count_words` and preprocess functions for better usability"""
    text = extract_text(html).lower()
    return count_words(text)


def validate_link(link):
    return link and link.startswith('http')
