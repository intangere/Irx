class hello():
	def __init__(self, *args):
		self.name = "hello"
		self.command = "hello"
		self.description = "Send hello to a user!"
		self.args = args[0]
	def run(self):
		print self.args
		user = self.args[3]
		return "Hello %s" % user