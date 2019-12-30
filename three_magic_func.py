'''
OOP之必需掌握的magic
'''

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return '《%s》' % self.title
    
    def __call__(self):
        print('《%s》 is written by %s' % (self.title, self.author))

if __name__ == "__main__":
    py_book = Book('core python', 'Wesly', 800) # 调用_init__
    print(py_book)  # 调用 __str__
    py_book()  # 调用 __call__