'''
带参数的装饰器
'''

def color(func):
    def red(*args):
        return '\033[31;1m%s\033[0m' % func(*args)
    return red

# 返回不同颜色的字体
def colors(c):
    def set_color(func):
        def red(*word):
            return '\033[31;1m%s\033[0m' % func(*word)
        def green(*word):
            return '\033[32;1m%s\033[0m' % func(*word)
        adict = {'red': red, 'green': green}
        return adict[c]
    return set_color


@colors('red')
def hello_2(word):
    return 'Hello %s' % word

@colors('green')
def welcome_2():
    return 'How are you?'

@color
def hello(world):
    return 'Hello %s' % world

@color
def welcome():
    return 'How are you?'

if __name__ == "__main__":
    print(hello('China'))
    print(welcome())
    print(hello_2('China'))
    print(welcome_2())