TARGET = slack-hotkey
SRC = slack-hotkey.py
BIN = dist/slack-hotkey

all: $(TARGET)

$(TARGET): $(SRC)
	python3 -O -m PyInstaller $(SRC) --onefile --name $(TARGET)

debug: $(SRC)
	python3 -m PyInstaller $(SRC) --onefile --name $(TARGET)

install: $(BIN)
	cp $(BIN) ~/bin/

clean:
	rm -rf *.spec dist build

nuitka:
	nuitka3 --onefile --standalone --macos-create-app-bundle --follow-imports -o slack-hotkey slack-hotkey.py
