import os


class Common():
    def __init__(self):
        self.usage = '''<ctrl>+<alt>+<shift>+h = Begin working
<ctrl>+<alt>+<shift>+j = Finish working
<ctrl>+<alt>+<shift>+k = AFK
<ctrl>+<alt>+<shift>+l = Back
<ctrl>+<alt>+<shift>+t = Test
<esc> = Quit
'''

    def getHome(self):
        return os.path.expanduser('~')

    def refreshScreen(self):
        if __debug__:
            print('> DEBUG mode')
        else:
            print('> Production mode')

        os.system('clear')
        print(self.usage)
