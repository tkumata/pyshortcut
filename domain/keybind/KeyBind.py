from pynput import keyboard


class KeyBind():
    def __init__(self, logger):
        self.logger = logger

    def punchIn(self):
        self.logger.info('> Press hotkey, punch in.')
        return {
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.alt,
            keyboard.KeyCode(char='h')
        }

    def punchOut(self):
        self.logger.info('> Press hotkey, punch out.')
        return {
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.alt,
            keyboard.KeyCode(char='j')
        }

    def away(self):
        self.logger.info('Press hotkey, away.')
        return {
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.alt,
            keyboard.KeyCode(char='k')
        }

    def back(self):
        self.logger.info('> Press hotkey, back.')
        return {
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.alt,
            keyboard.KeyCode(char='l')
        }

    def test(self):
        self.logger.info('> Press hotkey, test.')
        return {
            keyboard.Key.shift,
            keyboard.Key.ctrl,
            keyboard.Key.alt,
            keyboard.KeyCode(char='t')
        }
