import sdl2
import lucia
import string

WHITELIST_ALL = [i for i in string.printable if not i=="\r" or i=="\n"]
WHITELIST_LETTERS = [i for i in string.ascii_letters]
WHITELIST_DIGITS = [i for i in string.digits]
WHITELIST_HEXDIGITS = [i for i in string.hexdigits]

class VirtualInput():
	def __init__(self, message, password=False, whitelist=WHITELIST_ALL, callback=None):
		self.text = ""
		self.message = message
		self.password = password
		self.callback=callback
		#set by the callback and used to break out of the input loop at any given time
		self.input_break=False
		self.allowed_characters=whitelist

	def run(self):
		while True:
			if callable(self.callback):
				self.callback(self)
			if self.input_break:
				break
			events = lucia.process_events()
			for event in events:
				if event.type == sdl2.SDL_KEYDOWN:
					if event.key.keysym.sym in (sdl2.SDLK_DOWN, sdl2.SDLK_UP):
						lucia.output.output(self.text)
						continue
					if event.key.keysym.sym == sdl2.SDLK_BACKSPACE:
						if len(self.text) == 0:
							continue
						last = self.text[-1]
						self.text = self.text[:-1]
						lucia.output.output(last + " deleted") if self.password == False else lucia.output.output("hidden deleted")
					if event.key.keysym.sym == sdl2.SDLK_RETURN:
						return self.text
					if event.key.keysym.sym == sdl2.SDLK_SPACE:
						self.text += " "
						lucia.output.output("space") if self.password == False else lucia.output.output("hidden")
					try:
						if chr(event.key.keysym.sym) in self.allowed_characters:
							self.text += chr(event.key.keysym.sym)
							lucia.output.output(chr(event.key.keysym.sym)) if self.password == False else lucia.output.output("hidden")
					except ValueError:
						continue