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

def to_romans(decimal):

	roman = ""
	while decimal > 0:
		for number, symbol in special_chars:
			if decimal >= number:
				roman += symbol
				decimal -= number
	return roman


class RomanizeCommand(sublime_plugin.TextCommand):
	

	def run(self, edit):

		for selected_text in self.view.sel():
			if not selected_text.empty():
				if re.match(r'[0-9]+', self.view.substr(selected_text)):
					to_modify = int(self.view.substr(selected_text))

					roman = to_romans(to_modify)
                
					self.view.replace(edit, selected_text, roman)
