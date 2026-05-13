

import sys

PAGE_SIZE = 256
BACKING_STORE = "BACKING_STORE.bin"


class BackingStore:
    
    def __init__(self, path=BACKING_STORE):
        self.f = open(path, "rb")

    def readPage(self, pageNum):
        self.f.seek(pageNum * PAGE_SIZE)
        data = self.f.read(PAGE_SIZE)
        if len(data) != PAGE_SIZE:
            sys.stderr.write(f"Short read for page {pageNum}\n")
            sys.exit(1)
        return bytearray(data)