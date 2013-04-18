# -*- coding: utf-8 -*-
import collections
import utilities

class Page(object):
    """A single Page"""

    def __init__(self, page_number):
        self.page_number = page_number

    def __str__(self):
        return "FIFO Page %d\n" % (self.page_number)


class SC_Page(Page):
    """Second-Chance Page"""
    def __init__(self, page_number):
        super(SC_Page, self).__init__(page_number)
        self.r_bit = 1

    def __str__(self):
        return "Second-Chance Page %d\n, R-bit: %d" % (self.page_number, self.r_bit)

class LRU_Page(Page):
    """Least Recently Used Page"""
    def __init__(self, page_number):
        super(LRU_Page, self).__init__(page_number)
        self.counter = -1

    def __str__(self):
        return "LRU Page %d\n, Counter: %d" % (self.page_number, self.counter)

class FIFO(object):
    """FIFO Replacement Algorithm"""

    def __init__(self, memory_size, access):
        self.memory_size = memory_size  # memory size (number of pages)
        self.access = access
        self._page_map = {}  # dictionary mapping page number to memory index
        self._queue = collections.deque()  # FIFO queue (queue of Page objects)
        self._memory_map = []  # current memory map (snapshot)
        self._memory_map_records = [] 
        self._page_fault = 0

    def start(self):
        for page_number in self.access:

            if self.is_full():
                if not self.has_page(page_number):
                    self.page_fault()
                    old_number = self._dequeue_page()
                    self._enqueue_page(page_number)
                    self.replace_page(old_number, page_number)
            else:
                self.page_fault()
                self.add_page(page_number)

            self.set_memory_map()
            #print self.get_memory_map()
            self.record_memory_map()

    def page_fault(self):
        """Increment page fault number
        """
        self._page_fault += 1

    def is_full(self):
        """Check whether the memory is full of pages"""
        if len(self._page_map) >= self.memory_size:
            return True
        return False

    def add_page(self, page_number):
        current_len = len(self._page_map)
        self._page_map[page_number] = current_len
        self._enqueue_page(page_number)

    def has_page(self, page_number):
        """Check whether a page is in memory"""
        if page_number in self._page_map and self._page_map[page_number] >= 0:
            return True
        return False

    def replace_page(self, old_number, new_number):
        """
        Replace a page in the memory
            * Update self._page_map
        """
        index = self._page_map[old_number]
        self._page_map[old_number] = -1
        self._page_map[new_number] = index

    def access_page(self, page_number):
        """Do nothing in FIFO algorithm"""
        pass

    def set_memory_map(self):
        """Set the memory map derived from page map"""
        sorted_list_tuple = sorted([(key, value) for key, value in 
                            self._page_map.iteritems() if value >= 0], 
                            key=lambda pair: pair[1])
        self._memory_map = [pair[0] for pair in sorted_list_tuple]

    def get_memory_map(self):
        """Get and derive memory map from page map"""
        return self._memory_map

    def _enqueue_page(self, page_number):
        page = Page(page_number)
        self._queue.append(page)
        return page

    def _dequeue_page(self):
        page = self._queue.popleft()
        return page.page_number

    def record_memory_map(self):
        """Record current memory map"""
        memory_map = self.get_memory_map()
        self._memory_map_records.append(memory_map)

    def get_memory_map_records(self):
        memory_map_records = []
        for memory_map in self._memory_map_records:
            memory_map_records.append(" ".join(map(str, memory_map)))
        return "\n".join(memory_map_records)

    def get_page_faults_percent(self):
        return utilities.roundup_2(float(self._page_fault)/len(self.access))

    def get_output(self):
        return "%s\n\nPercentage of page faults: %.2f\n" \
               % (self.get_memory_map_records(), self.get_page_faults_percent())

class Second_Chance(FIFO):
    """Second-Chance Algorithm"""

    def start(self):
        for page_number in self.access:

            if self.is_full():
                if not self.has_page(page_number):
                    self.page_fault()
                    while self.second_chance(page_number):
                        pass
                self.access_page(page_number)
            else:
                self.page_fault()
                self.add_page(page_number)
                self.access_page(page_number)

            self.set_memory_map()
            #print self.get_memory_map()
            self.record_memory_map()

    def add_page(self, page_number):
        current_len = len(self._page_map)
        page = self._enqueue_page(page_number)
        self._page_map[page_number] = (current_len, page)
    
    def second_chance(self, page_number):
        """Second-Chance inspection upon page fault"""
        page = self._queue[0]
        if page.r_bit == 0:
            old_number = self._dequeue_page()
            new_page = SC_Page(page_number)
            self.replace_page(old_number, page_number, new_page)
            self._enqueue(new_page)
            return False

        if page.r_bit == 1:
            page = self._dequeue()
            page.r_bit = 0
            self._enqueue(page)
            return True

    def has_page(self, page_number):
        """Check whether a page is in memory"""
        if page_number in self._page_map and self._page_map[page_number][0] >= 0:
            return True
        return False

    def replace_page(self, old_number, new_number, new_page):
        """
        Replace a page in the memory
            * Update self._page_map
        """
        index = self._page_map[old_number][0]
        old_page = self._page_map[old_number][1]
        self._page_map[old_number] = (-1, old_page)
        self._page_map[new_number] = (index, new_page)

    def _enqueue_page(self, page_number):
        page = SC_Page(page_number)
        self._queue.append(page)
        return page

    def _enqueue(self, page):
        """Enqueue a Page object"""
        self._queue.append(page)

    def _dequeue(self):
        """Dequeue a Page object"""
        return self._queue.popleft()

    def access_page(self, page_number):
        page = self._page_map[page_number][1]
        page.r_bit = 1

    def set_memory_map(self):
        """Set the memory map derived from page map"""
        sorted_list_tuple = sorted([(key, value) for key, value in 
                            self._page_map.iteritems() if value[0] >= 0], 
                            key=lambda pair: pair[1])
        self._memory_map = [pair[0] for pair in sorted_list_tuple]

class LRU(Second_Chance):
    """Least Recently Used Algorithm"""

    def __init__(self, memory_size, access):
        self.memory_size = memory_size
        self.access = access
        self._page_map = {}
        self._memory_map = []  # current memory map (snapshot)
        self._memory_map_records = [] 
        self._page_fault = 0
        self._lru_page_number = -1  # page number of the LRU page

    def start(self):
        counter = 0
        for page_number in self.access:
            if self.is_full():
                if not self.has_page(page_number):
                    self.page_fault()
                    self.lru(page_number)
                self.access_page(page_number, counter)
            else:
                self.page_fault()
                self.add_page(page_number)
                self.access_page(page_number, counter)

            self.set_memory_map()
            #print self.get_memory_map()
            self.record_memory_map()
            counter += 1

    def add_page(self, page_number):
        current_len = len(self._page_map)
        page = LRU_Page(page_number)
        self._page_map[page_number] = (current_len, page)

    def lru(self, page_number):
        old_number = self.get_lru_page()
        new_page = LRU_Page(page_number)
        self.replace_page(old_number, page_number, new_page)


    def access_page(self, page_number, counter):
        page = self._page_map[page_number][1]
        page.counter = counter

    def replace_page(self, old_number, new_number, new_page):
        """
        Replace a page in the memory
            * Update self._page_map
        """
        index = self._page_map[old_number][0]
        del self._page_map[old_number]
        self._page_map[new_number] = (index, new_page)

    def get_lru_page(self):
        """Get the page number of the LRU page"""
        lru = min(self._page_map.items(), key=lambda t: t[1][1].counter)
        return lru[0]



if __name__ == '__main__':
    utilities.output.warning("Please run main.py script from project's directory.")  






