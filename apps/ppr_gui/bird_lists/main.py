from csv import reader, writer, QUOTE_MINIMAL # Imports csv library to allow the program to read and write to the list which are saved as csv files
import difflib # To find close matches in the search
import os.path # To check if file already exists before creating new list
import os # Uses the listdir function to find lists in the bird_lists folder

from helpers import setup_logger # Logger for ZPUI

menu_name = "Bird Lists"  # App name as seen in main menu while using the system

from subprocess import call # Uses for ZPUI logging
from time import sleep # Used to pause the program for an amount of seconds

from ui import Menu, Printer, PrettyPrinter, Listbox, DialogBox # Import the UI functions we need from ZPUI

logger = setup_logger(__name__, "info") # Sets up the ZPUI logger

def call_internal():
        Printer(["Calling internal", "command"], i, o, 1)
        logger.info("Success")

def call_external():
        Printer(["Calling external", "command"], i, o, 1)
        call(["echo", "Success"])

# Function to load lists from the csv files into nested lists within a dictionary

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

# Allows the user to select a list from the bird_lists directory

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
	selected_list = Listbox(list_names, i, o).activate()
	file_number = list_names.index(selected_list)
	global selected_file
	selected_file = files[file_number] # Stores the selected list's file name to be used elsewhere

# Simply reads the selected list

def read_list():
	with open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + selected_file, "r") as csvfile:
		csv_reader = reader(csvfile, delimiter=",", quotechar='"')
		for row in csv_reader:
			print(', '.join(row))

# Searches the selected list by bird, date or location and finds the closest match if there isn't a exact one when possible

def search_list():
	target_type_contents = [
	["Bird", 0],
	["Date", 1],
	["Location", 2]]
	target_type = Listbox(target_type_contents, i, o).activate()
	if target_type in (0, 1, 2):
		if target_type == 0:
			target = raw_input("Bird: ").lower()
		elif target_type == 1:
                        target = raw_input("Date: ").lower()
              	else:
                        target = raw_input("Location: ").lower()
		data_values = data.values()
		matches = []
		match = False
		for value in data_values: # Need to add option to choose just one list
			for list_item in value:
				if list_item[target_type].lower() == target:
					matches.append("{} on {} at {}".format(str(list_item[0]), str(list_item[1]), str(list_item[2])))
					match = True
		if match:
			if len(matches) > 1:
				PrettyPrinter("{} and {}".format(", ".join(matches[:-1]), matches[-1]), i, o, 5, None)
			else:
				print(matches[0])
		if not match:
			birds = [list_item[0] for value in data_values for list_item in value]
			dates = [list_item[1] for value in data_values for list_item in value]
			locations = [list_item[2] for value in data_values for list_item in value]
			best_match = difflib.get_close_matches(target, birds, 1)
			if best_match:
				yes_no = DialogBox("yn", i, o, message = "Did you mean {}?".format(best_match[0])).activate()
				if yes_no:
					match_index = birds.index(best_match[0])
					PrettyPrinter("{} on {} at {}".format(best_match[0], str(dates[match_index]), str(locations[match_index])), i, o, 5, None)
				else:
					PrettyPrinter("No match found", i, o, 5, None)
			else:
				PrettyPrinter("No match found", i, o, 5, None)
# Adds a record to the selected list

def add_to_list():
	with open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + selected_file, "a") as csvfile:
		a_bird = raw_input("Bird to add: ")
		a_date = raw_input("Date to add: ")
        	a_location = raw_input("Location to add: ")
		csv_writer = writer(csvfile, delimiter=",", quotechar='"', quoting=QUOTE_MINIMAL)
		csv_writer.writerow([a_bird, a_date, a_location])

# Creates a new list

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
