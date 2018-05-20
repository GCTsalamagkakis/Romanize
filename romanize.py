import sublime
import sublime_plugin
import re
from .romans import *

class RomanizeCommand(sublime_plugin.TextCommand):
    def get_number_selections(self):
        for region in self.view.sel():
            if region.empty(): break

            text = self.view.substr(region)
            if not re.match(r'[1-9]+', text): break

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
