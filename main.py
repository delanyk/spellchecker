from re import S
import sys
from utils.datamanager import DataManager
from checker.spellchecker import Spellchecker



if __name__ == "__main__":
    filename = sys.argv[1]
    data = DataManager.load_data(filename)
    filtered_data = DataManager.filter(data)

    checker = Spellchecker()
    