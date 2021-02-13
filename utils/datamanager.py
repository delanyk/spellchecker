import re

# Non-English or German characters, used to filter out foreign tweets
non_ende_char = ["á", "à", "ã", "ă", "â", "é", "è", "ê", "í", "ì",
                 "ĩ", "ó", "ò", "õ", "ô", "ơ", "ú", "ù", "ũ", "ư", "ý", "ỳ", "đ", "ñ"]
# contractions can be miss categorized as incorrect when you strip and filter the data
contractions = ["´", "‘", "’", "it's", "he's", "she's", "that's", "what's", "there's", "aren't",
                "[newline]", "'m", "'ve", "n't", "'ll", "'re", "won't", "'d", "geht's", "gibt's", "'s", " xd"]
# fixes are uncontracted contractions
fixes = ["'", "'", "'", "it is", "he is", "she is", "that is", "what is", "there is", "are not",
         " ", " am", " have", " not", " will", " are", "will not", " would", "geht es", "gibt es", "", " "]


class DataManager:
    """

    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def load_data(filename):
        with open('filename', 'r') as f:
            raw_text = f.read()
        tab_seperated = [item.split('\t') for item in raw_text.split('\n') if len(item.split('\t')) >= 4]

        return tab_seperated

    @staticmethod
    def filter(data):
        """
        """
        # Building our tweet filter
        filtered = []
        for i in data:
            for char in non_ende_char:
                if char in i[4]:
                    filtered.append(i[1])
        data_dict = {}
        for i in range(len(data)):
            # extracting the filtered tweets and IDs
            if data[i][1] not in filtered:
                data_dict[data[i][1]] = data[i][4]

        return data_dict
