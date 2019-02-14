from csv import reader, writer, QUOTE_MINIMAL
import difflib
import os.path
import os

from helpers import setup_logger

menu_name = "Bird Lists"  # App name as seen in main menu while using the system

from subprocess import call
from time import sleep

from ui import Menu, Printer, PrettyPrinter, Listbox

logger = setup_logger(__name__, "info")

def call_internal():
        Printer(["Calling internal", "command"], i, o, 1)
        logger.info("Success")

def call_external():
        Printer(["Calling external", "command"], i, o, 1)
        call(["echo", "Success"])

def csv_setup():
	select_list()
	global csvfile
	with open("/home/pi/piportablerecorder/apps/ppr_gui/bird_lists/" + selected_file) as csvfile:
    		readCSV = reader(csvfile, delimiter=',', skipinitialspace=True)
		global birds
		global dates
		global locations
    		birds = []
    		dates = []
		locations = []
    		for row in readCSV:
        		bird = row[0].lower()
			date = row[1].lower()
			location = row[2].lower()
        		birds.append(bird)
        		dates.append(date)
			locations.append(location)

    		print(birds)
    		print(dates)
		print(locations)

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
		target = raw_input("What bird are you looking for? ") # Do same for date and location
		try:
			match = birds.index(target.lower())
			the_date = dates[match].lower()
                        the_location = locations[match].title()
                        PrettyPrinter("{} on {} at {}".format(target, str(the_date), the_location), i, o, 5, None)
		except:
			best_match = difflib.get_close_matches(target.lower(), birds, 1)
                        score = difflib.SequenceMatcher(None, target, best_match).ratio()
                        print(score)
			if score:
				yes_no = raw_input("Did you mean " + best_match + "? ").lower()
				if yes_no == "yes":
					match = birds.index(best_match.lower())
                        		the_date = dates[match].lower()
                        		the_location = locations[match].title()
                        		PrettyPrinter("{} on {} at {}".format(best_match, str(the_date), the_location), i, o, 5, None)

			elif not score or yes_no != "yes":
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
	csv_setup()
	menu_contents = [
	["Read", read_list],
	["Search", search_list],
	["Add to list", add_to_list],
	["Create new list", create_list]
	]
	Menu(menu_contents, i, o, "Lister").activate()

