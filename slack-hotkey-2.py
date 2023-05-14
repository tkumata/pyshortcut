import json
import logging
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from pynput import keyboard

# init
print('> Receiving hotkey')

# get config file
homedir = os.path.expanduser('~')
f = open(homedir + '/.slack-hotkey/config.json', 'r')
config_json = json.load(f)
f.close()

# set logger
logger = logging.getLogger(__name__)
if __debug__:
    print('> DEBUG mode')
    logger.setLevel(logging.DEBUG)
else:
    print('> Production mode')
    logger.setLevel(logging.ERROR)
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


# Slack controller class
class SlackCtrl:
    def __init__(self):
        self.TOKEN = config_json['token']
        self.MEMBER_ID = config_json['member_id']
        self.CHANNEL = config_json['channel']

    def dummySlack(self, message):
        logger.debug(message)

    def postToChannel(self, message):
        headers = {
            'Authorization': 'Bearer %s' % self.TOKEN,
            'X-Slack-User': self.MEMBER_ID,
            'Content-Type': 'application/json; charset=utf-8'
        }
        params = {
            'channel': self.CHANNEL,
            'text': message,
            'as_user': True
        }
        req = urllib.request.Request(
            "https://slack.com/api/chat.postMessage",
            method='POST',
            data=json.dumps(params).encode('utf-8'),
            headers=headers
        )
        i = 0
        while True:
            try:
                logger.info('Post to channel ' + message)
                urllib.request.urlopen(req)
            except HTTPError as e:
                if i + 1 == 3:
                    raise
                else:
                    logger.error('Error code: ', e.code)
            except URLError as e:
                logger.error('Reason: ', e.reason)
            else:
                break

    def changeStatus(self, status_text, status_emoji):
        headers = {
            'Authorization': 'Bearer %s' % self.TOKEN,
            'X-Slack-User': self.MEMBER_ID,
            'Content-Type': 'application/json; charset=utf-8'
        }
        params = {
            'profile': {
                'status_text': status_text,
                'status_emoji': status_emoji
            }
        }
        req = urllib.request.Request(
            "https://slack.com/api/users.profile.set",
            method='POST',
            data=json.dumps(params).encode('utf-8'),
            headers=headers
        )
        i = 0
        while True:
            try:
                logger.info('Change status: ' + status_text)
                urllib.request.urlopen(req)
            except HTTPError as e:
                if i + 1 == 3:
                    raise
                else:
                    logger.error('Error code: ', e.code)
            except URLError as e:
                logger.error('Reason: ', e.reason)
            else:
                break

    def postPunchIn(self, msg='Begin working.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: Working')
        else:
            self.postToChannel(':keyboard:<ctrl>+<alt>+<shift>+h ' + msg)
            self.changeStatus('Working', ':working-from-home:')

    def postPunchOut(self, msg='Finish working.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: Zzz')
        else:
            self.postToChannel(':keyboard:<ctrl>+<alt>+<shift>+j ' + msg)
            self.changeStatus('Zzz.', ':syu:')

    def postAway(self, msg='Away from keyboard.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: AFK')
        else:
            self.postToChannel(':keyboard:<ctrl>+<alt>+<shift>+k ' + msg)
            self.changeStatus('AFK', ':ri:')

    def postBack(self, msg='I am back.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: Working')
        else:
            self.postToChannel(':keyboard:<ctrl>+<alt>+<shift>+l ' + msg)
            self.changeStatus('Working', ':working-from-home:')


def on_press(key):
    if key in COMBINATION_IN:
        current.add(key)
        if all(k in current for k in COMBINATION_IN):
            print(usage)
            logger.info(current)
            slack.postPunchIn()
    if key in COMBINATION_OUT:
        current.add(key)
        if all(k in current for k in COMBINATION_OUT):
            print(usage)
            logger.info(current)
            slack.postPunchOut()
    if key in COMBINATION_AWAY:
        current.add(key)
        if all(k in current for k in COMBINATION_AWAY):
            print(usage)
            logger.info(current)
            slack.postAway()
    if key in COMBINATION_BACK:
        current.add(key)
        if all(k in current for k in COMBINATION_BACK):
            print(usage)
            logger.info(current)
            slack.postBack()
    if key in COMBINATION_TEST:
        current.add(key)
        if all(k in current for k in COMBINATION_TEST):
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
print(usage)

current = set()
slack = SlackCtrl()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
