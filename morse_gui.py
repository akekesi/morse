import os
import json
import time

from tkinter import *
from class_colors import Colors
from morse_func_00 import func_sign2morse, func_decoder


class GUIMorse:
	"""Morse Machine"""

	def __init__(self, master) -> None:
		"""
		Set GUI
		"""
		# variables
		widget_bg = "white"
		path_morse_dict = r"morse_dict.json"
		path_morse_icon = r"morse_icon.png"
		self.after_ms = 100 # [ms]
		self.morse_unit = 0.3 # [s]
		self.func_set_initial_values()

		# load dictionary
		path_json = os.path.join(os.getcwd(), path_morse_dict)
		with open(path_json) as f:
			self.dictionary_morse = json.load(f)

		# master config
		master.title("Morse")
		master.configure(bg=widget_bg)
		master.iconphoto(False, PhotoImage(file=path_morse_icon))

		# frames
		frame_output = LabelFrame(master=master, text="Output", bg=widget_bg, padx=20, pady=20)
		frame_output.pack(side=TOP, fill=X, expand=True, padx=20, pady=(20, 10))
		frame_input = LabelFrame(master=master, text="Input", bg=widget_bg, padx=20, pady=20)
		frame_input.pack(side=TOP, fill=X, expand=True, padx=20, pady=(10, 20))

		# widgets
		self.entry_text = Entry(frame_output, state="readonly", width=25, justify=CENTER, readonlybackground=widget_bg)
		self.entry_text.pack(side=TOP, fill=X, expand=True)

		self.button_push = Button(master=frame_input, text="Push", bg=widget_bg, activebackground="red")
		self.button_push.pack(side=TOP, fill=X, expand=True)
		self.button_push.bind('<ButtonPress-1>', self.func_button_push_start)
		self.button_push.bind('<ButtonRelease-1>', self.func_button_push_stop)

		Button(master=frame_input, text="Clear", bg=widget_bg, command=self.func_clear).pack(side=TOP, fill=X, expand=True)
		Button(master=frame_input, text="Close", bg=widget_bg, command=lambda: self.func_close(master)).pack(side=TOP, fill=X, expand=True)

	def func_set_initial_values(self) -> None:
		"""
		Set initial variables
		"""
		self.print_step = 0
		self.print_time = 0
		self.click = False
		self.time_start = 0
		self.time_stop = 0
		self.after_id = ""
		self.sign_raw = []
		self.sign_clean = []
		self.sign_print = []

	def func_button_push_start(self, event=None) -> None:
		"""
		Start function for push button
		"""
		self.time_stop = 0
		if not self.time_start:
			self.time_start = time.time()
		self.func_button_push_run(run=True)
		if self.after_id: # ez kell, vagy legyen kulon start/stop id?
			self.button_push.after_cancel(id=self.after_id)
		self.after_id = self.button_push.after(ms=self.after_ms, func=self.func_button_push_start)

	def func_button_push_stop(self, event=None) -> None:
		"""
		Stop function for push button
		"""
		self.time_start = 0
		if not self.time_stop:
			self.time_stop = time.time()
		self.func_button_push_run(run=False)
		if self.after_id: # ez kell, vagy legyen kulon start/stop id?
			self.button_push.after_cancel(id=self.after_id)
		if sum(self.sign_raw[-15:]) != 0:
			self.after_id = self.button_push.after(ms=self.after_ms, func=self.func_button_push_stop)
		else:
			self.func_get_signal_clean(sign=0)

	def func_button_push_run(self, run: bool = True) -> None:
		"""
		Run function for push button
		"""
		self.print_step += 1
		t = time.time()
		if run:
			if self.click:
				self.func_get_signal_clean(sign=0)
				self.click = False
			self.print_time = t - self.time_start
			text_color = f"{Colors.FAIL}"
			self.sign_raw.append(1)
		else:
			if not self.click:
				self.func_get_signal_clean(sign=1)
				self.click = True
			self.print_time = t - self.time_stop
			text_color = f"{Colors.ENDC}"
			self.sign_raw.append(0)
		print(f"{text_color}{self.print_step}:\t{self.print_time:.3f}s{Colors.ENDC}")

	def func_get_signal_clean(self, sign: int = 0) -> None:
		"""
		Get clean sign and write letter in real time
		Args:
			sign:	type of signal 0/1
		Returns:
			None
		"""
		if sign:
			if self.print_time < self.morse_unit * 1.5:
				self.sign_print.extend([1] * 1)
			else:
				self.sign_print.extend([1] * 3)
		else:
			if self.print_time < self.morse_unit * 1.5:
				self.sign_print.extend([0] * 1)
			else:
				if self.print_time < self.morse_unit * 3 * 1.5:
					self.sign_print.extend([0] * 3)
				else:
					self.sign_print.extend([0] * 7)
				code = func_sign2morse(sign=self.sign_print)
				text = func_decoder(
					dictionary=self.dictionary_morse,
					code=code
				)
				self.entry_text.config(state="normal")
				self.entry_text.insert(END, text)
				self.entry_text.config(state="readonly")
				print(f"{self.sign_print} --> {code} --> {text}")
				self.sign_clean.extend(self.sign_print)
				self.sign_print = []

	def func_clear(self) -> None:
		"""
		Clear variables and widgets
		"""
		self.func_set_initial_values()
		self.entry_text.config(state="normal")
		self.entry_text.delete(0, END)
		self.entry_text.insert(0, "")
		self.entry_text.config(state="readonly")

	def func_close(self, master) -> None:
		"""
		Close gui
		"""
		code = func_sign2morse(sign=self.sign_clean)
		text = func_decoder(
			dictionary=self.dictionary_morse,
			code=code
		)
		print(f"all: {self.sign_clean} --> {code} --> {text}")
		master.quit()
		master.destroy()


if __name__ == "__main__":
	# run gui
	root = Tk()
	morse = GUIMorse(root)
	root.mainloop()
