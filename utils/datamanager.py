import re

# Non-English or German characters, used to filter out foreign tweets
non_ende_char = ["á", "à", "ã", "ă", "â", "é", "è", "ê", "í", "ì",
                 "ĩ", "ó", "ò", "õ", "ô", "ơ", "ú", "ù", "ũ", "ư", "ý", "ỳ", "đ", "ñ"]


class DataManager:
    """

    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def filter(data):
        """
        """
        #Building our tweet filter
        filtered = []
        for i in data:
            for char in non_ende_char:
                if char in i[4]:
                    filtered.append(i[1])
        data_dict = {}
        for i in range(len(data)):
            #extracting the filtered tweets and IDs
            if data[i][1] not in filtered:
                data_dict[data[i][1]] = data[i][4]

        return data_dict