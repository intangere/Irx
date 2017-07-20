import os.path
class topic():
	
	def __init__(self, *args):
		self.name = "topic"
		self.command = "topic"
		self.description = "Set the topic"
		self.args = args[0]

	def run(self, sendLine):
		
		user = self.args[0]
		chan = self.args[1]
		topic = ' '.join(self.args[3:])
		sendLine("TOPIC %s :%s" % (chan, topic))