


from collections import deque


class PhysicalMemory:
    
    def __init__(self, numFrames):
        self.numFrames = numFrames
        self.frames = [None] * numFrames
        self.frameToPage = [-1] * numFrames
        self.fifoQueue = deque()
        self.nextFree = 0

    def loadPage(self, pageNum, pageData, pageTable, tlb):
        if self.nextFree < self.numFrames:
            frame = self.nextFree
            self.nextFree += 1
        else:
            frame = self.fifoQueue.popleft()
            oldPage = self.frameToPage[frame]
            if oldPage != -1:
                pageTable.invalidate(oldPage)
                tlb.invalidate(oldPage)

        self.frames[frame] = pageData
        self.frameToPage[frame] = pageNum
        self.fifoQueue.append(frame)
        return frame