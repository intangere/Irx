import irx.config
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
from irx import Irx

class Iris(irc.IRCClient):

	nickname = irx.config.nickname
	realname = irx.config.realname
	username = irx.config.username
	prefix   = irx.config.prefix

	def __init__(self):
		self.irx = Irx.Irx(self.sendLine, irx.config.nickname, irx.config.username, irx.config.realname)
		self.irx.loadPlugins("plugins")
		self.irx.buildCommandList()

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
	
	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
	
	def signedOn(self):
		for channel in irx.config.channels:
			self.join(channel)
	
	def topicUpdated(self, user, channel, topic):
		f = open("data/topics/current_topic_%s.txt" % channel, "w+")
		f.write(topic)
		f.close()

	def privmsg(self, user, channel, data):
		if data.startswith(self.prefix):
			self.irx.doCommand(channel, user, data)


class BotFactory(protocol.ClientFactory):

	def buildProtocol(self, addr):
		iris = Iris()
		iris.factory = self
		return iris
	
	def clientConnectionFailed(self, connector, reason):
		connector.connect()
	
	def clientConnectionLost(self, connector, reason):
		reactor.stop()

if __name__ == "__main__":
	Factory = BotFactory()
	reactor.connectTCP(irx.config.host, irx.config.port, Factory)
	reactor.run()
