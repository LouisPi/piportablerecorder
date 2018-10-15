from time import sleep

from base_ui import BaseUIElement
from canvas import Canvas

class TimePicker(BaseUIElement):

	def __init__(self, i, o, name="TimePicker"):

		BaseUIElement.__init__(self, i, o, name)

		self.c = Canvas(self.o)
		self.font = self.c.load_font("Fixedsys62.ttf", 32)

		self.currentHour = 12
		self.currentMinute = 30

		# Position 0 = hour, position 1 = minute
		self.position = 0

	def get_return_value(self):
		pass

	def generate_keymap(self):
		return {
			"KEY_RIGHT": "move_right",
			"KEY_LEFT": "move_left",
			"KEY_UP": "increase_one",
			"KEY_DOWN": "decrease_one",
			"KEY_ENTER": "accept_value",
			"KEY_F1": "exit_time_picker"
		}

	def move_right(self):
		if self.position == 0:
			self.position = 1
		self.refresh()

	def move_left(self):
		if self.position == 1:
			self.position = 0
		self.refresh()

	def increase_one(self):
		if self.position == 0:
			if self.currentHour == 23:
				self.currentHour = 0
			else:
				self.currentHour = min(23, self.currentHour+1)

		elif self.position == 1:
			if self.currentMinute == 59:
				self.currentMinute = 0
			else:
				self.currentMinute = min(59, self.currentMinute+1)

		self.refresh()

	def decrease_one(self):
		if self.position == 0:
			if self.currentHour == 0:
				self.currentHour = 23
			else:
				self.currentHour = max(0, self.currentHour-1)
				
		elif self.position == 1:
			if self.currentMinute == 0:
				self.currentMinute = 59
			else:
				self.currentMinute = max(0, self.currentMinute-1)

		self.refresh()

	def idle_loop(self):
		sleep(0.1)

	def exit_time_picker(self):
		self.deactivate()

	def accept_value(self):
		pass

	def draw_clock(self):
		self.c.clear()

		# Draw the clock string centered on the screen
		clock_string = "{:02d}:{:02d}".format(self.currentHour, self.currentMinute)
		clock_text_bounds = self.c.get_text_bounds(clock_string, font=self.font)

		width_padding = (self.c.width-clock_text_bounds[0])/2
		height_padding = (self.c.height-clock_text_bounds[1])/2
		self.c.text(clock_string, (width_padding, height_padding-2), font=self.font)

		# Draw the arrows either on the left or right side depending on whether hours or minutes are being edited
		bx = 0
		if self.position == 0:
			bx = 0
		elif self.position == 1:
			bx = self.c.width/2-width_padding+6

		# Base coordinates for arrows
		triangle_top = ((bx+width_padding+6, height_padding-5), (bx+self.c.width/2-10, height_padding-5), 
			(bx+width_padding-2+((self.c.width/2-width_padding)/2), height_padding-15))

		triangle_bottom = ((bx+width_padding+6, self.c.height-height_padding+5), (bx+self.c.width/2-10, self.c.height-height_padding+5), 
			(bx+width_padding-2+((self.c.width/2-width_padding)/2), self.c.height-height_padding+15))

		self.c.polygon(triangle_top, fill="white")
		self.c.polygon(triangle_bottom, fill="white")

		self.c.display()

	def refresh(self):
		self.draw_clock()