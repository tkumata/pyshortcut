#
# Slack  API を使うだけの責務。
#

import json
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError


# Slack controller class
class SlackCtrl():
    def __init__(self, homedir, logger):
        f = open(homedir + '/.slack-hotkey/config.json', 'r')
        config_json = json.load(f)
        f.close()

        self.TOKEN = config_json['token']
        self.MEMBER_ID = config_json['member_id']
        self.CHANNEL = config_json['channel']
        self.logger = logger

    def dummySlack(self, message):
        self.logger.debug('> ' + message)

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
                self.logger.info('> Post to channel ' + message)
                urllib.request.urlopen(req)
            except HTTPError as e:
                if i + 1 == 3:
                    raise
                else:
                    self.logger.error('> Error code: ', e.code)
            except URLError as e:
                self.logger.error('> Reason: ', e.reason)
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
                self.logger.info('> Change status: ' + status_text)
                urllib.request.urlopen(req)
            except HTTPError as e:
                if i + 1 == 3:
                    raise
                else:
                    self.logger.error('> Error code: ', e.code)
            except URLError as e:
                self.logger.error('> Reason: ', e.reason)
            else:
                break

    def postPunchIn(self, msg='Begin working.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: Working')
        else:
            self.postToChannel(':keyboard:' + msg)
            self.changeStatus('Working', ':working-from-home:')

    def postPunchOut(self, msg='Finish working.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: Zzz')
        else:
            self.postToChannel(':keyboard:' + msg)
            self.changeStatus('Zzz.', ':syu:')

    def postAway(self, msg='Away from keyboard.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: AFK')
        else:
            self.postToChannel(':keyboard:' + msg)
            self.changeStatus('AFK', ':ri:')

    def postBack(self, msg='I am back.'):
        if __debug__:
            self.dummySlack(':keyboard:' + msg)
            self.dummySlack('Change status: Working')
        else:
            self.postToChannel(':keyboard:' + msg)
            self.changeStatus('Working', ':working-from-home:')
