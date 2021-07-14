import math

class Pagination:
    def __init__(self, data={}):
        self.total = 0
        self.limit = 0
        self.currentPage = 1
        self.maxPages = 1
        self.endSize = 1
        self.midSize = 2
        self.prevNext = True
        self.prevText = 'Prev'
        self.nextText = 'Next'
        self.pages = []
        self.dots = False

        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    def run(self):
        if not self.total:
            return []

        self.maxPages = math.ceil(self.total / self.limit)

        if (self.maxPages < 2):
            return []

        if self.currentPage < 1:
            self.currentPage = 1

        self.pages = []

        for n in range(1, self.maxPages + 1):
            if n == self.currentPage:
                self.pages.append({
                    'label': n,
                    'page': n,
                    'class': 'current'
                })
                self.dots = True
            else:
                if (n <= self.endSize or \
                (self.currentPage and n >= self.currentPage - self.midSize and n <= self.currentPage + self.midSize) or \
                n > self.maxPages - self.endSize):
                    self.pages.append({
                        'label': n,
                        'page': n,
                        'class': ''
                    })
                    dots = True
                elif self.dots:
                    self.pages.append({
                        'label': '...',
                        'page': False,
                        'class': 'dots'
                    })
                    self.dots = False

        if self.prevNext and self.currentPage > 1:
            self.pages.insert(0, {
                'label': self.prevText,
                'page': (self.currentPage - 1),
                'class': 'prev'
            })

        if self.prevNext and self.currentPage < self.maxPages:
            self.pages.append({
                'label': self.nextText,
                'page': (self.currentPage + 1),
                'class': 'next'
            })

        return {
            'pages': self.pages,
            'offset': self.limit * (self.currentPage - 1),
            'limit': self.limit,
            'total': self.total
            }

