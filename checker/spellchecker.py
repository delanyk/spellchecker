import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as wnl
from nltk.metrics.distance import edit_distance as lev


class Spellchecker:
    """"""

    def __init__(self, acronyms=False):
        self.de_dic = set()
        with open("german.dic", "r", encoding="latin-1") as f:
            for row in f:
                if len(row) > 1:
                    self.de_dic.add(row.strip().lower())
        self.en_dic = set()
        with open(
            "english.dic",
            "r",
        ) as f:
            for row in f:
                self.en_dic.add(row.strip().lower())

        self.en_dic |= add_english
        self.de_dic |= add_german
        self.term_index = dict()
        self.top_en = []
        self.top_de = []

        self.en_dic |= add_english
        self.de_dic |= add_german
        if acronyms:
            self.en_dic |= add_acronyms
            self.de_dic |= add_acronyms
        with open(
            "english.dic",
            "r",
        ) as f:
            for row in f:
                self.en_dic.add(row.strip().lower())

    def is_language(self, term):
        """
        this function determines if a word is German or English
        Given on number of tweets within the postings list based on stop words and foreign characters
        """
        de_char = ["ä", "ö", "ü", "ß"]
        de_score = 0
        en_score = 0
        for post in self.term_index[term]:
            for i in data_index[post].strip().split():
                for char in de_char:
                    if char in i:
                        de_score += 1
                if i in stop_germ:
                    de_score += 1
                if i in stop_en:
                    en_score += 1
        if de_score > en_score:
            return "german"
        elif de_score < en_score:
            return "english"
        else:
            return None

    def language(self, post):
        """
        determines if the tweet is English or German
        Here we use a refined search to better identify if a tweet is english or Germn
        given stop words and our most frequent words occuring in English or German
        If it fails to identify, it will return none
        """
        de_char = ["ä", "ö", "ü", "ß"]
        de_score = 0
        en_score = 0
        for i in post.split():
            for char in de_char:
                if char in i:
                    de_score += 1
            if i in stop_germ or i in self.top_de[:200]:
                de_score += 1
            if i in stop_en or i in self.top_en[:200]:
                en_score += 1
        if de_score > en_score:
            return "german"
        elif en_score > de_score:
            return "english"
        else:
            return None
