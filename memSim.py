
#!/usr/bin/env python3 
import sys

from tlb import TLB
from pageTable import PageTable
from backingStore import BackingStore
from physicalMemory import PhysicalMemory

ADDRESS_MASK = 0xFFFF
PAGE_MASK = 0xFF00
OFFSET_MASK = 0x00FF


def parseArgs(argv):

    if len(argv) < 2 or len(argv) > 4 :
        sys.stderr.write("Usage: memSim <reference-file> [FRAMES] [PRA]\n")
        sys.exit(1)

    referenceFile = argv[1]
    
    if (len(argv) >= 3):
        frames = int(argv[2])
    else:
        frames =256
    
    if len(argv) == 4:
        pra = argv[3].upper()
    else:
        pra = "FIFO"

    if frames <= 0 or frames > 256:
        sys.stderr.write("FRAMES must be in range (0, 256]\n")
        sys.exit(1)
    if pra not in ("FIFO", "LRU", "OPT"):
        sys.stderr.write("PRA must be FIFO, LRU, or OPT\n")
        sys.exit(1)
    
    return referenceFile, frames, pra 

def readReferences(path):

    references = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                references.append(int(line))
    
    return references

def decodeAddress(address):

    address &= ADDRESS_MASK
    page = (address & PAGE_MASK) >> 8
    offset = address & OFFSET_MASK

    return page, offset

def formatOutputLine(address, signedByte, frameNum, frameData):

    hexContents = frameData.hex().upper()
    return f"{address}, {signedByte}, {frameNum}, {hexContents}"


def main():

    referenceFile, numberOfFrames, pra = parseArgs(sys.argv)
    references = readReferences(referenceFile)

    backing = BackingStore()
    tlb = TLB()
    pageTable = PageTable()
    memory = PhysicalMemory(numberOfFrames)

    tlbHits = 0
    tlbMisses = 0
    pageFaults = 0

    for address in references:
        page, offset = decodeAddress(address)

        frame = tlb.lookup(page)
        if frame is not None:
            tlbHits += 1
        else:
            tlbMisses += 1
            frame = pageTable.lookup(page)
            if frame is None:
                pageFaults += 1
                pageData = backing.readPage(page)
                frame = memory.loadPage(page, pageData, pageTable, tlb)
                pageTable.setEntry(page, frame)
            tlb.insert(page, frame)

        byteValue = memory.frames[frame][offset]

        if (byteValue >= 128) :
            byteValue -= 256

        print (formatOutputLine(address & ADDRESS_MASK, byteValue, frame, memory.frames[frame]))
    

    total = len(references)

    if total:
       faultRate = pageFaults / total
    else:
       faultRate = 0
   
    if total:
       hitRate = tlbHits / total
    else:
       hitRate = 0

    print(f"Number of Translated Addresses = {total}")
    print(f"Page Faults = {pageFaults}")
    print(f"Page Fault Rate = {faultRate:.3f}")
    print(f"TLB Hits = {tlbHits}")
    print(f"TLB Misses = {tlbMisses}")
    print(f"TLB Hit Rate = {hitRate:.3f}")

if __name__ == "__main__":
    main()