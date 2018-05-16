import sublime
import sublime_plugin
import re

special_chars = [(1000, 'M'),
				(900, 'CM'),
				(500, 'D'),
				(400, 'CD'),
				(100, 'C'),
				(90, 'XC'),
           		(50, 'L'),
           		(40, 'XL'),
           		(10, 'X'),
           		(9, 'IX'),
           		(5, 'V'),
           		(4, 'IV'),
           		(1, 'I')]


def from_romans(str):

	i = 0
	decimal = 0
	while i < len(str):
		for number, symbol in special_chars:
			if str[i] == symbol or str[i].upper() == symbol:
				symbol1 = number
		if i+1 < len(str):
			for number, symbol in special_chars:
				if str[i+1] == symbol or str[i+1].upper() == symbol:
					symbol2 = number
			if symbol1 >= symbol2:
				decimal += symbol1
				i += 1
			else:
				decimal += symbol2 - symbol1
				i += 2
		else:
			decimal += symbol1
			i += 1
	return decimal

def to_romans(decimal):

	if decimal <= 1000000000:
		roman = ""
		for number, symbol in special_chars:
			while decimal >= number:
				roman += symbol
				decimal -= number
	else:
		roman = decimal
	return roman

class RomanizeCommand(sublime_plugin.TextCommand):

	def is_enabled(self, lint=False, integration=False, kill=False):

		if self.view.has_non_empty_selection_region():
			return True
		return False
	
	def run(self, edit):

		for selected_text in self.view.sel():
			if not selected_text.empty():
				if re.match(r'[0-9]+', self.view.substr(selected_text)):
					to_modify = int(self.view.substr(selected_text))
					roman = to_romans(to_modify)
					self.view.replace(edit, selected_text, roman)

class To_DecimalCommand(sublime_plugin.TextCommand):
	
	def is_enabled(self, lint=False, integration=False, kill=False):

		if self.view.has_non_empty_selection_region():
			return True
		return False

	def run(self, edit):

		for selected_text in self.view.sel():
			if not selected_text.empty():
				if re.match(r'[mcdlxviMCDLXVI]+', self.view.substr(selected_text)):
					to_modify = self.view.substr(selected_text)
					decimal = from_romans(to_modify)
					self.view.replace(edit, selected_text, str(decimal))
