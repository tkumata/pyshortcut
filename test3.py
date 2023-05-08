from pynput import keyboard

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

current = set()


def on_press(key):
    # Punch in
    if key in COMBINATION_IN:
        current.add(key)
        if all(k in current for k in COMBINATION_IN):
            print('punch in')
    # Punch out
    if key in COMBINATION_OUT:
        current.add(key)
        if all(k in current for k in COMBINATION_OUT):
            print('punch out')
    # Away from keyboard
    if key in COMBINATION_AWAY:
        current.add(key)
        if all(k in current for k in COMBINATION_AWAY):
            print('away from keyboard')
    # Im back
    if key in COMBINATION_BACK:
        current.add(key)
        if all(k in current for k in COMBINATION_BACK):
            print('I am back')
    # Escape from listening
    if key == keyboard.Key.esc:
        listener.stop()


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
