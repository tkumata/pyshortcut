#
# ここでやることはキーが押下されたら関数を叩くだけの責務
# それ以外は依存先に任せるもしくは取得する。
#

from pynput import keyboard

from common.Common import Common
from controller.SlackCtrl import SlackCtrl
from domain.keybind.KeyBind import KeyBind
from interface.logger.Logger import Logger

# オブジェクトやインスタンスの生成
initVar = Common()
homedir = initVar.getHome()
initVar.refreshScreen()

log = Logger(homedir)
logger = log.getLogger()

slack = SlackCtrl(homedir, logger)

keybind = KeyBind(logger)
hotkeyPunchin = keybind.punchIn()
hotkeyPunchout = keybind.punchOut()
hotkeyAwway = keybind.away()
hotkeyBack = keybind.back()
hotkeyTest = keybind.test()

current = set()


# TODO: ロジックになっているので多純な呼び出しだけにできないか考える。
def on_press(key):
    if key in hotkeyPunchin:
        current.add(key)
        if all(k in current for k in hotkeyPunchin):
            initVar.refreshScreen()
            logger.info(current)
            slack.postPunchIn()
    if key in hotkeyPunchout:
        current.add(key)
        if all(k in current for k in hotkeyPunchout):
            initVar.refreshScreen()
            logger.info(current)
            slack.postPunchOut()
    if key in hotkeyAwway:
        current.add(key)
        if all(k in current for k in hotkeyAwway):
            initVar.refreshScreen()
            logger.info(current)
            slack.postAway()
    if key in hotkeyBack:
        current.add(key)
        if all(k in current for k in hotkeyBack):
            initVar.refreshScreen()
            logger.info(current)
            slack.postBack()
    if key in hotkeyTest:
        current.add(key)
        if all(k in current for k in hotkeyTest):
            initVar.refreshScreen()
            logger.info(current)
    if key == keyboard.Key.esc:
        initVar.refreshScreen()
        logger.info(key)
        listener.stop()


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
