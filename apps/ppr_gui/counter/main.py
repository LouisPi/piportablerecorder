from helpers import setup_logger

menu_name = "Counter"  # App name as seen in main menu while using the system

from subprocess import call
from time import sleep

from ui import Menu, Printer, DialogBox, Refresher

logger = setup_logger(__name__, "info")

def call_internal():
        Printer(["Calling internal", "command"], i, o, 1)
        logger.info("Success")

def call_external():
        Printer(["Calling external", "command"], i, o, 1)
        call(['echo', 'Success'])

#Callback global for ZPUI. It gets called when application is activated in the main menu
callback = None

i = None #Input device
o = None #Output device
counter = None

def increase_counter(start_at, num):
        start_at += num
	return str(start_at)

def confirm_exit():
	choice = DialogBox("yn", i, o).activate()
	if choice:
		refresher.deactivate()
	else:
		pass

def init_app(input, output):
        global callback, i, o
        i = input;
        o = output  # Getting references to output and input device objects and saving them as globals

def callback():
	global counter
        counter = 0
	keymap = {
	"KEY_LEFT":confirm_exit,
	"KEY_ENTER":increase_counter
	}
	number = int(raw_input("Increase by: "))
	refresher = Refresher(increase_counter(counter, number), i, o, 1, keymap, "Counter")
	refresher.activate()
	print(counter)
