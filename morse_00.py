import os
import json
import matplotlib.pyplot as plt


def func_encoder(dictionatry: dict, text: str) -> list:
	"""
	Description...
	"""
	code = []
	for t in text:
		if t == " ":
			code.append("|")
		else:
			code.append(dictionatry[t])
	code.append("|")
	return code


def func_decoder(dictionatry: dict, code: list) -> str:
	"""
	Descritpion...
	"""
	text = ""
	for c in code:
		if c == "|":
			text += " "
		else:
			text += func_get_key(dictionary=dictionatry, value_to_find=c)
	return text[:-1]


def func_get_key(dictionary: dict, value_to_find) -> str:
	"""
	Description...
	"""
	for key, value in dictionary.items():
		if value_to_find == value:
			return key


def func_print_code(code: list, delimiter: str = " ") -> None:
	"""
	Description...
	"""
	return delimiter.join(code)


def func_plot_sign(sign: list) -> None:
	"""
	Plot list of signals
	Args:
		sign:	list of signals
	Returns:
		None
	"""
	plt.plot(sign, 'k.-', label="sign")
	plt.title("Sign")
	plt.xlabel("time")
	plt.ylabel("sign")
	plt.legend(loc="upper right")
	plt.grid()
	plt.show()

def func_simulator_reciever(sign: list) -> list:
	"""
	Description... 
	"""
	i = 0
	sig0 = 0
	sig1 = 0
	code = []
	code_letter = ""
	while (True):
		if sig0 > 7:
			break
		if sign[i] == 0:
			sig1 = 0
			sig0 += 1
			if sig0 == 3:
				code.append(code_letter)
				code_letter = ""
			if sig0 == 7:
				code.append("|")
		else:
			sig0 = 0
			sig1 += 1
			if sig1 > 1:
				code_letter = code_letter[:-1]
				code_letter += "-"
			else:
				code_letter += "."
		i += 1
	return code


def func_morse2sign(code: list) -> list:
	"""
	Discription...
	"""
	sign = []
	for c in " ".join(code):
		if c == ".":
			sign.append(1)
			sign.append(0)
		if c == "-":
			for _ in range(3):
				sign.append(1)
			sign.append(0)
		if c == " ":
			for _ in range(2):
				sign.append(0)
		if c == "|":
			for _ in range(2):
				sign.append(0)
	for _ in range(7):
		sign.append(0)
	return sign


if __name__ == "__main__":
	path_json = os.path.join(os.getcwd(), "morse_dict.json")
	with open(path_json) as f:
		dictionary_morse = json.load(f)
	print(json.dumps(dictionary_morse, indent=4))

	text_list =  [
		"NULL",
		"SOS 42 SOS"
	]
	for text in text_list:
		code = func_encoder(
			dictionatry=dictionary_morse,
			text=text
		)
		sign = func_morse2sign(
			code=code
		)
		code_ = func_simulator_reciever(sign=sign)
		text_ = func_decoder(
			dictionatry=dictionary_morse,
			code=code_
		)
		print(f"{text} --> {func_print_code(code)}")
		print(f"{text_} <-- {func_print_code(code_)}")
		func_plot_sign(sign=sign)
