class test():
	def __init__(self, *args):
		self.name = "test"
		self.command = "test"
		self.description = "Send test!"
		self.args = args[0]
	def run(self):
		return "test command"