import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as wnl
from nltk.metrics.distance import edit_distance as lev

# stop_en and stop_germ are the stopwords
stop_en = set(stopwords.words("english"))
stop_germ = set(stopwords.words("german"))

add_english = {
    "anymore",
    "adhd",
    "asshole",
    "fucking",
    "porn",
    "fuck",
    "proud",
    "others",
    "mom",
    "ptsd",
    "europe",
    "tumour",
    "tumours",
    "stats",
    "favourite",
    "boyfriend",
    "fortnite",
    "bts",
}
add_acronyms = {
    "lol",  # laugh out loud
    "omg",  # oh my god
    "af",  # as fuck
    "tbh",  # to be honest
    "bc",  # because
    "idk",  # i don't know
    "rn",  # right now
    "ppl",  # people
    "lmao",  # laugh my ass off
    "wtf",  # what the fuck
    "btw",  # by the way
    "pls",  # please
    "thx",  # thanks
    "aml",  # anti-money laundering
}

add_german = {"sowas"}

# Non-English or German characters, used to filter out foreign tweets
non_eng_char = ["á", "à", "ã", "ă", "â", "é", "è", "ê", "í", "ì", "ĩ",
                "ó", "ò", "õ", "ô", "ơ", "ú", "ù", "ũ", "ư", "ý", "ỳ", "đ", "ñ"]


class Spellchecker:
    """"""

    def __init__(self, acronyms=False):
        self.de_dic = set()
        self.en_dic = set()
        self.terms = {}
        self.term_index = dict()
        self.terms_en = set()
        self.terms_de = set()
        self.top_en = []
        self.top_de = []

        self.chars = {
                    "en" : "abcdefghijklmnopqrstuvwxyz",
                    "de" : "abcdefghijklmnopqrstuvwxyzäöüß"
                    }

        # Load language dictionaries
        with open("data/english.dic", "r") as f:
            for row in f:
                self.en_dic.add(row.strip().lower())
        with open("data/german.dic", "r", encoding="latin-1") as f:
            for row in f:
                if len(row) > 1:
                    self.de_dic.add(row.strip().lower())
        self.en_dic |= add_english
        self.de_dic |= add_german
        if acronyms:
            self.en_dic |= add_acronyms
            self.de_dic |= add_acronyms

    def is_language(self, term, data):
        """
        this function determines if a word is German or English
        Given on number of tweets within the postings list based on stop words and foreign characters
        """
        de_char = ["ä", "ö", "ü", "ß"]
        de_score = 0
        en_score = 0
        for post in self.term_index[term]:
            for i in data[post].strip().split():
                for char in de_char:
                    if char in i:
                        de_score += 1
                if i in stop_germ:
                    de_score += 1
                if i in stop_en:
                    en_score += 1
        if de_score > en_score:
            return "de"
        elif de_score < en_score:
            return "en"
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
            return "de"
        elif en_score > de_score:
            return "en"
        else:
            return None

    def top_freq(self,dict):
        """
        find which words are the most frequent in there respective langauges
        """
        freq = []
        for term, val in dict.items():
            freq.append((val, term))
        freq = sorted(freq)[::-1]
        freq_de = []
        freq_en = []
        for i,j in freq:
            if self.is_language(j) == 'de':
                freq_de.append(j)
            else:
                freq_en.append(j)
        return freq_de, freq_en

    #This function finds misspelled words
    def get_misspells(self,):
        """
        finds misspelled words
        """
        #Here we generate a list of terms and list to partition them in
        words =sorted([key for key in self.terms.keys()])
        de = []
        en = []
        for word in words:
            g_count = 0
            e_count = 0
            e_posts = []
            g_posts = []
            #here we sort correct words separate correct_addicitonal terms
            if word in self.en_dic:
                self.terms_en.add(word)
                continue
            elif word in self.de_dic:
                self.terms_de.add(word)
                continue
            #pos tags for lemmatization generation
            tags = ['n','v','a','s','r']
            en_lemma = {}
            for tag in tags:
                lemma = wnl.lemmatize(wnl,word=word, pos=tag) 
                en_lemma[lemma]= 1
#             #German lemmatiziaton/stemming
            de_lemma = word
            
        #here we search post by post to determin if term in index
        # is German or English, to see if in the context it is a misspell
            for post in self.term_index[word]:
                if self.language(post) == 'de':
                    ## get german misspelling count
                    if de_lemma not in self.de_dic:
                        if len([i for i in en_lemma.keys() if i in self.en_dic]) == 0:
                            g_count += 1
                            g_posts.append(post)
                    else:
                        self.terms_de.add(word)
                        
                elif self.language(post) == 'en':

                    ## get german misspelling count
                    if len([i for i in en_lemma.keys() if i in self.en_dic]) == 0:
                        e_count += 1
                        e_posts.append(post)
                    else:
                        self.terms_en.add(word)
                
            #Here if the refined methon is not able to solve,
            #It falls back to the likelihood of based on occurance in German or English Tweets 
                else:
                    lang = self.is_language(word)
                    if lang == 'de':
                        
                        ## get german misspelling count    
                        if de_lemma not in self.de_dic:
                            if len([i for i in en_lemma.keys() if i in self.en_dic]) == 0:
                                g_count += 1
                                g_posts.append(post)
                        else:
                            self.terms_de.add(word)
                    if lang == 'en':
                        ## get english misspelling count
                        if len([i for i in en_lemma.keys() if i in self.en_dic]) == 0:
                            e_count += 1
                            e_posts.append(post)
                        else:
                            self.terms_en.add(word)
                            
            if g_count > 0:
                de.append((g_count, word, g_posts))
            if e_count > 0:
                en.append((e_count, word, e_posts))
            
        #retruning list of misspells and correct lists
        return sorted(de)[::-1], sorted(en)[::-1]

    
    def _damerau(self, word, lang):
        """
        calculates the Damerau distance of the misspelled words 
        """
        #here we reduce the workload by reducing same characters 
        #that occur more than twice in a row to just two characters to increase accuracy 
        term = ''
        for i in range(len(word)):
            try:
                if word[i] != word[i+2]:
                    term += word[i]
            except: 
                term += word[i]
        
        alphabet = self.chars[lang]
        possible = {}
        
        #we are genearting a dictionary of terms that are 1 damerau distance from the term
        chunks = [(term[:i], term[i:])for i in range(len(term) + 1)]
        for chunk1, chunk2 in chunks:
            if chunk2:
                #subtraction
                possible[chunk1+chunk2[1:]] = 1
                for char in alphabet:
                    #substitution
                    possible[chunk1+char+chunk2[1:]] = 1
            if len(chunk2) > 1:
                #transposition
                possible[chunk1+chunk2[1]+chunk2[0]+chunk2[2:]] = 1
            for char in alphabet:
                #addition
                possible[chunk1+char+chunk2] = 1
        
        return possible
    #This function finds the suggested terms based on the damerau distance for English words
    def _en_suggested(self,term):
        """
        Finds the suggested terms based on the damerau distance for English words
        """
        #Some terms such as the following can be force edited
        #They are slang to represent expressions
    #     if term == 'kinda':
    #         return "kind of"
    #     if term == 'gonna':
    #         return 'going to'
    #     if term == 'wanna':
    #         return 'want to'
        suggestions = self._damerau(term,"en")
        suggested = []
        #Lemmatizing the suggestions to get a more accurate reference
        for i in suggestions.keys():
            tags = ['n','v','a','s','r']
            lemmas = []
            for tag in tags:
                lemmas.append(wnl.lemmatize(wnl,word=i, pos=tag))
            lemmas = set(lemmas)
            for j in lemmas:
                if j in self.en_dic:
                    suggested.append(i)
        #Refining the words that were suggested using edited distance again
        refined = [word for word in suggested if lev(term, word) == min(lev(term,word) for word in suggested)] 
        try:
            #further refining the search
            best = sorted([(self.terms[word],word) for word in refined if word in self.terms_en])[::-1]
            return [i for j,i in best][:3]
        except:
            return refined

    def _de_suggested(self,term):
        """
        Finds the suggested terms based on the damerau distance for German words
        """
        suggestions = self._damerau(term, "de")
        suggested = []
        for i in suggestions:
            if i in self.de_dic:
                suggested.append(i)
        #Refining the words that were suggested using edited distance again
        refined = [word for word in suggested if lev(term, word) == min(lev(term,word) for word in suggested)]
        try:
            #further refining the search
            best = sorted([(self.terms[word],word) for word in refined if word in self.de_dic and word in self.terms_de])[::-1]
            return [i for j,i in best][:3]
        except:
            return refined

    def display_top_mispells(self, en_mis, de_mis):
        top_mis_en = []
        for count, word, posts in en_mis[:10]:
            top_mis_en.append((word, count, self._en_suggested(word)))

        #This gives us the top misspelled German words
        top_mis_de = []
        for count, word, posts in de_mis[:10]:
            top_mis_de.append((word, count, self._de_suggested(word)))
        
        print("Top mispelled English words")
        for entry in top_mis_en:
            print(entry)
        
        print("\nTop mispelled German words")
        for entry in top_mis_de:
            print(entry)