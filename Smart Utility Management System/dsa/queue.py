class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear  = None
        self.size  = 0

    # Add alert to back of queue
    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear:
            self.rear.next = new_node
        self.rear  = new_node
        if not self.front:
            self.front = new_node
        self.size += 1

    # Remove alert from front of queue
    def dequeue(self):
        if not self.front:
            return None
        data       = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self.size -= 1
        return data

    # See front without removing
    def peek(self):
        return self.front.data if self.front else None

    def is_empty(self):
        return self.size == 0

    def to_list(self):
        result  = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result