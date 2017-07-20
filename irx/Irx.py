from twisted.internet import protocol, reactor
from twisted.words.protocols import irc
from irx.config import prefix
import os

class Irx(object):
	
	def __init__(self, s, nick, user, real):
		self.sendLine = s
		self.channel = ""
		self.nickname = nick
		self.realname = real
		self.username = user
		self.plugins = []
		self.commands = {}
		self.reserved_commands = [".reload", ".help"]
		self.prefix = prefix
		self.plugins_folder = "plugins"

	def doAction(self, data):
		pass
	
	def getMessage(self, channel, data):
		self.channel = channel
		if " :" in data:
			msg = data.split(" :")[1]
			return msg
		return ""

	def buildCommandList(self):
		for name in self.plugins:
			command = "%s%s" % (self.prefix, name)
			self.commands[command] = self.getClassByName(self.plugins[name], "%s.%s.%s" % (self.plugins_folder, name, name))

	def getClassByName(self, module, className):
		if not module:
			if className.startswith(".%s" % self.plugins_folder):
				className = className.split(".%s" % self.plugins_folder)[1]
			l = className.split(".")
			m = __services__[l[0]]
			return getClassByName(m, ".".join(l[1:]))
		elif "." in className:
			l = className.split(".")
			m = getattr(module, l[2])
			return m
		else:
			return getattr(module, className)

	def loadPlugins(self, folder):
		self.plugins_folder = folder
		res = {}
		lst = os.listdir(folder)
		dir = []
		if "__init__.py" in lst:
			for d in [p for p in lst if p.endswith(".py")]:
				dir.append(d[:-3])
		for d in dir:
			if d != "__init__":
				res[d] = __import__(folder + "." + d, fromlist = ["*"])
		self.plugins = res
		return res

	def doCommand(self, chan, user, command):
		user = user.split("!")[0]
		if command in self.reserved_commands:
			self.nativeCall(user, chan, command)
		else:
			spt = command.split(" ")
			args = [spt[0], user, chan]
			for value in spt:
				args.append(value)
			print(self.commands)
			self.commands[args[0]](args[1:]).run(self.sendLine)

	def respondToPing(self, data):
		hsh = data.split(" ")[1]
		self.sendLine("PONG %s" % hsh)

	def nativeCall(self, user, chan, call):
		call = call[1:]
		if call == "reload":
			self.plugins = []
			self.commands = {}
			self.loadPlugins(self.plugins_folder)
			self.buildCommandList()
			self.send(chan, "Reloaded plugins")

		if call == "help":
			for command in self.commands:
				self.send(chan, "%s - %s " % (command, self.commands[command]([]).description))

	def send(self, chan, msg):
		self.sendLine("PRIVMSG %s :%s" % (chan, msg))

