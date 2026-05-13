from collections import deque

TLB_SIZE = 16

class TLB:

    def __init__(self):
        self.entries = deque()

    def lookup(self, page):
        for p, f in self.entries:
            if p == page:
                return f
        return None
    
    def insert(self, page, frame):
        newEntries = deque()
        for p, f in self.entries:
            if p != page:
                newEntries.append((p, f))
        
        self.entries = newEntries

        if len(self.entries) >= TLB_SIZE:
            
            self.entries.popleft()
        self.entries.append((page, frame))

    def invalidate(self, page):

        newEntries = deque()
        for p, f in self.entries:
            if p != page:
                newEntries.append((p, f))
        self.entries = newEntries
    