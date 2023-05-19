import logging
import os

from pynput import keyboard

from controller.slack import SlackCtrl

# init
print('> Receiving hotkey')

if __debug__:
    print('> DEBUG mode')
else:
    print('> Production mode')

# get home dir
homedir = os.path.expanduser('~')

# set logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_fmt = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
log_handler = logging.FileHandler(homedir + '/.slack-hotkey/slack-hotkey.log')
log_handler.setFormatter(log_fmt)
logger.addHandler(log_handler)


COMBINATION_IN = {
    keyboard.Key.shift,
    keyboard.Key.ctrl,
    keyboard.Key.alt,
    keyboard.KeyCode(char='h')
}

COMBINATION_OUT = {
    keyboard.Key.shift,
    keyboard.Key.ctrl,
    keyboard.Key.alt,
    keyboard.KeyCode(char='j')
}

COMBINATION_AWAY = {
    keyboard.Key.shift,
    keyboard.Key.ctrl,
    keyboard.Key.alt,
    keyboard.KeyCode(char='k')
}

COMBINATION_BACK = {
    keyboard.Key.shift,
    keyboard.Key.ctrl,
    keyboard.Key.alt,
    keyboard.KeyCode(char='l')
}

COMBINATION_TEST = {
    keyboard.Key.shift,
    keyboard.Key.ctrl,
    keyboard.Key.alt,
    keyboard.KeyCode(char='t')
}


def on_press(key):
    if key in COMBINATION_IN:
        current.add(key)
        if all(k in current for k in COMBINATION_IN):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postPunchIn()
    if key in COMBINATION_OUT:
        current.add(key)
        if all(k in current for k in COMBINATION_OUT):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postPunchOut()
    if key in COMBINATION_AWAY:
        current.add(key)
        if all(k in current for k in COMBINATION_AWAY):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postAway()
    if key in COMBINATION_BACK:
        current.add(key)
        if all(k in current for k in COMBINATION_BACK):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postBack()
    if key in COMBINATION_TEST:
        current.add(key)
        if all(k in current for k in COMBINATION_TEST):
            os.system('clear')
            print(usage)
            logger.info(current)
    if key == keyboard.Key.esc:
        logger.info(key)
        listener.stop()


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


usage = '''<ctrl>+<alt>+<shift>+h = Begin working
<ctrl>+<alt>+<shift>+j = Finish working
<ctrl>+<alt>+<shift>+k = AFK
<ctrl>+<alt>+<shift>+l = Back
<ctrl>+<alt>+<shift>+t = Test
<esc> = Quit
'''

os.system('clear')
print(usage)

current = set()
slack = SlackCtrl(homedir, logger)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
