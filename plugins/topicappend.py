import os.path

class topicappend():
	
	def __init__(self, *args):
		self.name = "topicappend"
		self.command = "topicappend"
		self.description = "Append to the topic "
		self.args = args[0]

	def run(self, sendLine):

		user = self.args[0]
		chan = self.args[1]
		append_topic = ' '.join(self.args[3:])
		topic = self.getTopic(chan)

		if topic:
			append_topic = ' | '.join([topic, append_topic])

		sendLine("TOPIC %s :%s" % (chan, append_topic))

	def getTopic(self, chan):

		if os.path.isfile('data/topics/current_topic_%s.txt' % chan):
			with open('data/topics/current_topic_%s.txt' % chan) as f:
				return f.read().strip()
		else:
			return None