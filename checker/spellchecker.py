import re 
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as wnl
from nltk.metrics.distance import edit_distance as lev

class Spellchecker:
    def __init__(self):
        pass