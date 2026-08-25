# Each node stores one day's consumption record
class Node:
    def __init__(self, date, utility_type, amount):
        self.date         = date
        self.utility_type = utility_type  # electricity, water, gas
        self.amount       = amount
        self.next         = None          # points to next node

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    # Add new record at the beginning (most recent first)
    def insert_at_front(self, date, utility_type, amount):
        new_node      = Node(date, utility_type, amount)
        new_node.next = self.head
        self.head     = new_node
        self.size    += 1

    # Get all records as a list (for displaying in dashboard)
    def to_list(self):
        records = []
        current = self.head
        while current:
            records.append({
                "date"         : current.date,
                "utility_type" : current.utility_type,
                "amount"       : current.amount
            })
            current = current.next
        return records

    # Get only records of one type (electricity/water/gas)
    def filter_by_type(self, utility_type):
        records = []
        current = self.head
        while current:
            if current.utility_type == utility_type:
                records.append({
                    "date"  : current.date,
                    "amount": current.amount
                })
            current = current.next
        return records

    # Display all (for testing)
    def display(self):
        current = self.head
        while current:
            print(f"{current.date} | {current.utility_type} | {current.amount}")
            current = current.next