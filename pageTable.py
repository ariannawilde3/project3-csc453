

PAGE_TABLE_SIZE = 256


class PageTable:

    def __init__(self):
        self.table = [[-1, 0] for _ in range(PAGE_TABLE_SIZE)]

    def lookup(self, page):
        frame, present = self.table[page]
        if present:
            return frame
        return None

    def setEntry(self, page, frame):
        self.table[page] = [frame, 1]

    def invalidate(self, page):
        self.table[page] = [-1, 0]