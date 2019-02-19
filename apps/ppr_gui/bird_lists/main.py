from csv import reader, writer, QUOTE_MINIMAL
import difflib
import os.path
import os

from helpers import setup_logger

menu_name = "Bird Lists"  # App name as seen in main menu while using the system

from subprocess import call
from time import sleep

from ui import Menu, Printer, PrettyPrinter, Listbox, DialogBox

logger = setup_logger(__name__, "info")

def call_internal():
        Printer(["Calling internal", "command"], i, o, 1)
        logger.info("Success")

def call_external():
        Printer(["Calling external", "command"], i, o, 1)
        call(["echo", "Success"])

def load_into_dict(d):
	select_list()
	global csvfile
	with open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + selected_file) as csvfile:
		readCSV = reader(csvfile, delimiter = ',', skipinitialspace = True)
		name = selected_file.split(".")[0]
		d[name] = []
		for row in readCSV:
			if row:
				d[name].append(row)

def select_list():
	files = []
	list_names = []
        for file in os.listdir("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists"):
		if file.endswith(".csv"):
			files.append(file)
	for file_name in files:
		file_name = file_name.replace("_", " ")
                file_name = file_name[:-4].title()
		list_names.append(file_name)
	selected_list = Listbox(list_names, i, o, "List selection").activate()
	file_number = list_names.index(selected_list)
	global selected_file
	selected_file = files[file_number]

def read_list():
	with open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + selected_file, "r") as csvfile:
		csv_reader = reader(csvfile, delimiter=",", quotechar='"')
		for row in csv_reader:
			print(', '.join(row))

def search_list():
        target = raw_input("What bird are you looking for? ").lower() # Need to add the option to do same for date and location
	data_values = data.values()
	match = False
	for value in data_values:
		for list_item in value:
 			if match:
 				continue
			if list_item[0].lower() == target:
				PrettyPrinter("{} on {} at {}".format(list_item[0], str(list_item[1]), list_item[2]), i, o, 5, None)
				match = True
	if not match:
		birds = [list_item[0] for value in data_values for list_item in value]
		dates = [list_item[1] for value in data_values for list_item in value]
		locations = [list_item[2] for value in data_values for list_item in value]
		best_match = difflib.get_close_matches(target, birds, 1)
		if best_match:
			yes_no = DialogBox("yn", i, o, message = "Did you mean {}".format(best_match[0])).activate()
			if yes_no:
				match_index = birds.index(best_match[0])
				PrettyPrinter("{} on {} at {}".format(best_match[0], str(dates[match_index]), str(locations[match_index])), i, o, 5, None)
			else:
				PrettyPrinter("No match found", i, o, 5, None)
		else:
			PrettyPrinter("No match found", i, o, 5, None)

def add_to_list():
	with open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + selected_file, "a") as csvfile:
		a_bird = raw_input("Bird to add: ")
		a_date = raw_input("Date to add: ")
        	a_location = raw_input("Location to add: ")
		csv_writer = writer(csvfile, delimiter=",", quotechar='"', quoting=QUOTE_MINIMAL)
		csv_writer.writerow([a_bird, a_date, a_location])

def create_list():
	file_name = raw_input("What would you like your list to be called? ").lower()
	if os.path.exists("/home/piportablerecorder/ppr_gui/bird_lists/" + file_name + ".csv"):
		print("File already exists!")
	else:
		open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + file_name + ".csv", "a+")

# Callback global for ZPUI. It gets called when application is activated in the main menu
callback = None

i = None # Input device
o = None # Output device

def init_app(input, output):
        global callback, i, o
        i = input;
        o = output  # Getting references to output and input device objects and saving them as globals

def callback():
	global data
	data = {}
	load_into_dict(data)
	menu_contents = [
	["Read", read_list],
	["Search", search_list],
	["Add to list", add_to_list],
	["Create new list", create_list]
	]
	Menu(menu_contents, i, o, "Lister").activate()

