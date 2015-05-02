class Hello:

    __gui = None

    def __init__(self, gui):
        self.__gui = gui 
    
    def hello(self, arg):
        print 'Hello ' + arg + '!'
 
    def run(self):
        print 'Hello world!'
