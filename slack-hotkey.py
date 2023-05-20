#
# ここでやることはキーが押下されたら関数を叩くだけの責務
# それ以外は依存先から持ってくる。
#

import os

from pynput import keyboard

from common.Common import Common
from controller.SlackCtrl import SlackCtrl
from domain.keybind.KeyBind import KeyBind
from interface.logger.logger import Logger

# オブジェクトやインスタンスの生成
initVar = Common()
homedir = initVar.getHome()

log = Logger(homedir)
logger = log.getLogger()

slack = SlackCtrl(homedir, logger)

keybind = KeyBind(logger)
hotkeyPunchin = keybind.punchIn()
hotkeyPunchout = keybind.punchOut()
hotkeyAwway = keybind.away()
hotkeyBack = keybind.back()
hotkeyTest = keybind.test()


print('> Receiving hotkey')

if __debug__:
    print('> DEBUG mode')
else:
    print('> Production mode')

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


# TODO: ロジックになっているので多純な呼び出しだけにできないか考える。
def on_press(key):
    if key in hotkeyPunchin:
        current.add(key)
        if all(k in current for k in hotkeyPunchin):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postPunchIn()
    if key in hotkeyPunchout:
        current.add(key)
        if all(k in current for k in hotkeyPunchout):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postPunchOut()
    if key in hotkeyAwway:
        current.add(key)
        if all(k in current for k in hotkeyAwway):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postAway()
    if key in hotkeyBack:
        current.add(key)
        if all(k in current for k in hotkeyBack):
            os.system('clear')
            print(usage)
            logger.info(current)
            slack.postBack()
    if key in hotkeyTest:
        current.add(key)
        if all(k in current for k in hotkeyTest):
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


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
