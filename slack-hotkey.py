import json
import logging
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

from pynput import keyboard

logger = logging.getLogger(__name__)

if __debug__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

log_fmt = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
log_handler = logging.FileHandler('slack-hotkey.log')
log_handler.setFormatter(log_fmt)
logger.addHandler(log_handler)


# Get current dir.
if os.path.dirname(__file__):
    exepath = os.path.dirname(__file__) + '/'
else:
    exepath = './'

# Open config file.
f = open(exepath + 'config.json', 'r')
config_json = json.load(f)
f.close()


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

    def postPunchIn(self, msg):
        if __debug__:
            self.dummySlack(':keyboard:' + msg + ':si: (test)')
            self.dummySlack('Change status: Working (test)')
        else:
            self.postToChannel(':keyboard:' + msg + ':si:')
            self.changeStatus('Working', ':working-from-home:')

    def postPunchOut(self, msg):
        if __debug__:
            self.dummySlack(':keyboard:' + msg + ':syu: (test)')
            self.dummySlack('Change status: Zzz. (test)')
        else:
            self.postToChannel(':keyboard:' + msg + ':syu:')
            self.changeStatus('Zzz.', ':syu:')

    def postAway(self, msg):
        if __debug__:
            self.dummySlack(':keyboard:' + msg + ':ri: (test)')
            self.dummySlack('Change status: AFK (test)')
        else:
            self.postToChannel(':keyboard:' + msg + ':ri:')
            self.changeStatus('AFK', ':ri:')

    def postBack(self, msg):
        if __debug__:
            self.dummySlack(':keyboard:' + msg + ':modo: (test)')
            self.dummySlack('Change status: Working (test)')
        else:
            self.postToChannel(':keyboard:' + msg + ':modo:')
            self.changeStatus('Working', ':working-from-home:')


slack = SlackCtrl()


# Begin working function
def function_punchin():
    logger.info('Call punch in function.')
    slack.postPunchIn(' Begin working. ')


# Finish working function
def function_punchout():
    logger.info('Call punch out function.')
    slack.postPunchOut(' Finish working. ')


# Away from keyboard function
def function_away():
    logger.info('Call away function.')
    slack.postAway(' AFK. ')


# Come back function
def function_back():
    logger.info('Call back function.')
    slack.postBack(' I am back. ')


# Quit script function
def function_quit():
    logger.debug('Quit')
    hotkey.stop()


with keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+<shift>+h': function_punchin,
    '<ctrl>+<alt>+<shift>+j': function_punchout,
    '<ctrl>+<alt>+<shift>+k': function_away,
    '<ctrl>+<alt>+<shift>+l': function_back,
    '<ctrl>+<alt>+<shift>+c': function_quit
}) as hotkey:
    hotkey.join()
