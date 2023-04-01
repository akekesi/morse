import time
import numpy as np

from tkinter import *


class GUIMorse:
	"""Morse Machine"""

	def __init__(self, master) -> None:
		# title
		master.title("Morse")

		# variables
		self.v = 0
		self.t = 0
		self.after_id = ""
		self.timeout = 100

		# frames
		frame_input = LabelFrame(master=master, text="Input", padx=20, pady=10)
		frame_input.grid(row=0, column=0, sticky=W+E, padx=10, pady=20)
		frame_output = LabelFrame(master=master, text="Output", padx=20, pady=10)
		frame_output.grid(row=1, column=0, sticky=W+E, padx=10, pady=20)

		# widgets
		self.button_push = Button(master=frame_input, text="PUSH", width=25)
		self.button_push.grid(row=0, column=0)
		self.button_push.bind('<ButtonPress-1>', self.func_button_push_start)
		self.button_push.bind('<ButtonRelease-1>', self.func_button_push_stop)

		Button(master=frame_input, text="CLOSE", width=25, command=lambda: self.func_close(master)).grid(row=1, column=0)

		self.label_led = Label(frame_output, text="", width=25, relief=SUNKEN, anchor="c")
		self.label_led.grid(row=0, column=0)

	def func_button_push_start(self, event=None) -> None:
		"""
		Description...
		"""
		if not self.t:
			self.t = time.time()
		self.func_button_push_run()
		self.after_id = self.button_push.after(ms=self.timeout, func=self.func_button_push_start)

	def func_button_push_stop(self, event=None) -> None:
		"""
		Description...
		"""
		self.t = 0
		self.button_push.after_cancel(id=self.after_id)
		self.label_led.configure(bg="SystemButtonFace")

	def func_button_push_run(self) -> None:
		"""
		Description...
		"""
		self.v += 1
		print(f"{self.v}: {time.time()-self.t:.3f}")
		self.label_led.configure(bg="red")

	def func_close(self, master) -> None:
		"""
		Description...
		"""
		master.quit()
		master.destroy()


if __name__ == "__main__":
	# run gui
	root = Tk()
	morse = GUIMorse(root)
	root.mainloop()
