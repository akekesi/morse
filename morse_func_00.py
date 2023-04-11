import os
import json
import matplotlib.pyplot as plt


def open_load_json(path_json: str) -> dict:
	"""
	Open and load json file
	Args:
		path:	relativ path of json
	Returns:
		dictionary
	"""
	path_json = os.path.join(os.getcwd(), path_json)
	with open(path_json) as f:
		dictionary = json.load(f)
	return dictionary


def func_encoder(dictionary: dict, text: str, space: str = "|") -> list:
	"""
	Encoder
	Args:
		dictionary:	dictionary
		text:		text to encode
		space:		space between codes
	Returns:
		list of codes
	"""
	code = []
	for t in text:
		if t == " ":
			code.append(space)
		else:
			code.append(func_get_value(dictionary=dictionary, key_to_find=t))
	return code


def func_decoder(dictionary: dict, code: list, space: str = "|") -> str:
	"""
	Decoder
	Args:
		dictionary:	dictionary
		code:		list of codes
		space:		space between codes
	Returns:
		decoded text
	"""
	text = ""
	for c in code:
		if c == space:
			text += " "
		else:
			text += func_get_key(dictionary=dictionary, value_to_find=c)
	return text


def func_get_value(dictionary: dict, key_to_find) -> str:
	"""
	Get value of key from dictionary
	Args:
		dictionary:		dictionary
		key_to_find:	key which belongs to value
	Returns:
		value of key
	"""
	value = ""
	if key_to_find in dictionary.keys():
		value = dictionary[key_to_find]
	return value


def func_get_key(dictionary: dict, value_to_find) -> str:
	"""
	Get key of value from dictionary
	Args:
		dictionary:		dictionary
		value_to_find:	value which belongs to key
	Returns:
		key of value
	"""
	key = ""
	for key_, value in dictionary.items():
		if value_to_find == value:
			key = key_
			break
	return key


def func_code2str(code: list, delimiter: str = " ") -> str:
	"""
	Join list of codes
	Args:
		code:		list of codes
		delimiter:	delimiter to join codes
	Returns:
		string (joined list of codes)
	"""
	return delimiter.join(code)


def func_plot_sign(sign: list) -> None:
	"""
	Plot list of signs
	Args:
		sign:	list of signs
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


def func_sign2morse(sign: list) -> list:
	"""
	Convert sign to morse code
	Args:
		sign: list of signs
		morse codes
	Return:
		list of morse codes
	"""
	sum_0 = 0
	sum_1 = 0
	code = []
	code_letter = ""
	for s in sign:
		if s == 0:
			sum_1 = 0
			sum_0 += 1
			if sum_0 == 3 and code_letter:
				code.append(code_letter)
				code_letter = ""
			if sum_0 == 3 + 7:
				code.append("|")
				sum_0 = 0
		else:
			sum_0 = 0
			sum_1 += 1
			if sum_1 > 1:
				code_letter = code_letter[:-1]
				code_letter += "-"
			else:
				code_letter += "."
	return code


def func_morse2sign(code: list) -> list:
	"""
	Convert morse code to sign
	Args:
		code: list of morse codes
	Return:
		list of signs
	"""
	sign = [0]
	for c in " ".join(code):
		if c == ".":
			if sign[-1]:
				sign.extend([0] * 1)
			sign.extend([1] * 1)
		if c == "-":
			if sign[-1]:
				sign.extend([0] * 1)
			sign.extend([1] * 3)
		if c == " ":
			sign.extend([0] * 3)
		if c == "|":
			sign.extend([0] * 7)
	sign.extend([0] * 3)
	return sign[1:]


if __name__ == "__main__":
	path_json = "morse_dict.json"
	dictionary_morse = open_load_json(path_json=path_json)
	print(json.dumps(dictionary_morse, indent=4))

	text_list =  [
		"NULL",
		"NULL ",
		"NULL  ",
		"NUL L  ",
		"NUL  L  ",
		"NUL   L  ",
		"NUL   L   ",
		" NUL   L   ",
		"  NUL   L   "
	]
	for text in text_list:
		code = func_encoder(
			dictionary=dictionary_morse,
			text=text
		)
		sign = func_morse2sign(
			code=code
		)
		print(f"{text} --> {func_code2str(code)} --> {sign}")
		code = func_sign2morse(sign=sign)
		text = func_decoder(
			dictionary=dictionary_morse,
			code=code
		)
		print(f"{text} <-- {func_code2str(code)} <-- {sign}")
		func_plot_sign(sign=sign)
