import os.path

class topicdel():
	
	def __init__(self, *args):
		self.name = "topicdel"
		self.command = "topicdel"
		self.description = "Delete from the topic "
		self.args = args[0]

	def run(self, sendLine):

		user = self.args[0]
		chan = self.args[1]
		delete_topic = ' '.join(self.args[3:])
		topic = self.getTopic(chan)

		if delete_topic in topic:
			topic = topic.replace('%s | ' % delete_topic, '') \
					.replace(' | %s' % delete_topic, '') \
					.replace('%s' % delete_topic, '') \
					.strip()

			sendLine("TOPIC %s :%s" % (chan, topic))
		else:
			sendLine("PRIVMSG %s :%s" % (chan, "Topic delete substring not found"))

	def getTopic(self, chan):
		if os.path.isfile('data/topics/current_topic_%s.txt' % chan):
			with open('data/topics/current_topic_%s.txt' % chan) as f:
				return f.read().strip()
		else:
			return None