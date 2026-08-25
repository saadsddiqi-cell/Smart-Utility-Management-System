class MinHeap:
    def __init__(self):
        self.heap = []

    # Insert alert — lower priority number = more critical
    def insert(self, priority, alert):
        self.heap.append((priority, alert))
        self._bubble_up(len(self.heap) - 1)

    # Bubble up to maintain heap property
    def _bubble_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._bubble_up(parent)

    # Remove and return most critical alert
    def extract_min(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root              = self.heap[0]
        self.heap[0]      = self.heap.pop()
        self._bubble_down(0)
        return root

    # Bubble down to maintain heap property
    def _bubble_down(self, index):
        smallest = index
        left     = 2 * index + 1
        right    = 2 * index + 2

        if left  < len(self.heap) and self.heap[left][0]  < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0

    def to_list(self):
        # Return sorted by priority
        return sorted(self.heap, key=lambda x: x[0])