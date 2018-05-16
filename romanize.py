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

	roman = ""
	for number, symbol in special_chars:
		while decimal >= number:
			roman += symbol
			decimal -= number
	return roman

class RomanizeCommand(sublime_plugin.TextCommand):
    def get_number_selections(self):
        for region in self.view.sel():
            if region.empty(): break

            text = self.view.substr(region)
            if not re.match(r'[0-9]+', text): break

            number = int(text)
            if int(text) > 1000000000: break
            
            yield (region, int(text))

    def is_enabled(self):
        return any(self.get_number_selections())
    
    def run(self, edit):
        for region, number in self.get_number_selections():
            self.view.replace(edit, region, to_romans(number))

class ToDecimalCommand(sublime_plugin.TextCommand):
	
	def get_number_selections(self):
		for region in self.view.sel():
			if region.empty(): break

			text = self.view.substr(region)
			if not re.match(r'[mcdlxviMCDLXVI]+', text): break
            
			yield (region, text)

	def is_enabled(self):
		return any(self.get_number_selections())
    
	def run(self, edit):
		for region, number in self.get_number_selections():
			self.view.replace(edit, region, str(from_romans(number)))
