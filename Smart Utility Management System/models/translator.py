import json
from dsa.hash_table import HashTable

def load_translations(lang="en"):
    ht = HashTable(size=50)

    try:
        with open(f"translations/{lang}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for key, value in data.items():
                ht.insert(key, value)
    except:
        pass

    return ht

def translate(ht, key):
    result = ht.search(key)
    return result if result else key