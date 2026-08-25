class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(self.size)]  # list of empty lists

    # Hash function — converts key to index
    def hash_function(self, key):
        total = 0
        for char in key:
            total += ord(char)   # ASCII value of each character
        return total % self.size # fit within table size

    # Insert key-value pair
    def insert(self, key, value):
        index = self.hash_function(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # update if already exists
                return
        bucket.append((key, value))        # add new entry

    # Search by key
    def search(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v           # found!
        return None                # not found

    # Delete by key
    def delete(self, key):
        index = self.hash_function(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)      # remove it
                return True
        return False

    # Display all entries (for testing)
    def display(self):
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Index {i}: {bucket}")