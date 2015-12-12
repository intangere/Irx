from twisted.internet import protocol, reactor
from twisted.words.protocols import irc
from blackjack import BlackJack
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
		self.reserved_commands = [".reload", ".help", ".deal", ".join", ".hit", ".stand", ".split", ".double", ".shuffle", ".hand"]
		self.prefix = "."
		self.plugins_folder = "plugins"
		self.bjk = BlackJack()

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
			msg = self.commands[args[0]](args[1:]).run()
			self.send(chan, msg)

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

		if call == "hit" or call == "stand":
			if call == "hit":
				res = self.bjk.hit(user)
			else:
				res = self.bjk.stand(user)
			if type(res) == type(list()):
				print res
				if len(res) == 0:
					self.send(chan, "Dealer won")
					self.send(chan, "Dealer's hand was : %s" % (self.bjk.winning_hands[0]))
				elif res[0] == "dealer":
					self.send(chan, "Dealer's hand: %s" % (self.bjk.winning_hands[0]))
					self.send(chan, "Dealer won!")
				elif res[0] == "Not standing":
					self.send(chan, "%s is now standing.." % user)
					self.send(chan, "Waiting for other players to decide...")
				elif res[0] == "pushed":
					self.send(chan, "No winners.")
					self.send(chan, "Pushed!")				
				elif len(res) > 0 and "dealer" not in res and res:
					self.send(chan, "Dealer lost!")
					if len(res) == 1:
						self.send(chan, "%s has won the round!" % (str(res)))
						self.send(chan, "%s's winning hand was: %s" % (user, self.bjk.winning_hands[0]))
				else:
					self.send(chan, "%s have won the round!" % (res))
					self.send(chan, "Winning hands were %s" % str(self.bjk.winning_hands))
				#else:
				#	self.send(chan, "No winners.")
			elif res == False:
				self.send(chan, "%s's cards: %s" % (user, str(self.bjk.players[user])))
			elif res == True:
				self.send(chan, "%s busted!" % user)
				#self.send(chan, "%s's cards were: %s" % (user, str(self.bjk.players[user]))
				self.send(chan , "%s was removed from game!" % user)
			else:
				self.send(chan, "%s won!" % user)
				self.send(chan, "%s winning hand: %s" % (user, self.bjk.winning_hands[0]))
				self.send(chan, "%s has been removed from game!" % user)
			pass

		if call == "deal":
			if len(self.bjk.players) < 2:
				self.send(chan, "No players in game..")
			else:
				res = self.bjk.deal()
				self.send(chan, "Shuffling deck...")
				self.send(chan, "Dealing cards..")
				if len(res) == 0:
					for player in self.bjk.players.keys():
						if player == "dealer":
							self.send(chan, "Dealer's cards: %s" % str(self.bjk.players["dealer"]))
						else:
							self.send(chan, "%s's cards: %s" % (player, str(self.bjk.players[player])))
				else:
					if res == "Has dealed":
						self.send(user, "The cards have already been dealed! Please wait for the next round!")
					else:
						self.send(chan, "%s has blackjack!" % res)

		if call == "double":
			self.bjk.double(user)
			pass

		if call == "join":
			res = self.bjk.addPlayerToGame(user)
			if res == True:
				self.send(chan, "%s joined the current game!" % user)
			else:
				self.send(user, "The game has already started. Please wait till next round to join!")


		if call == "shuffle":
			self.bjk.shuffle()
			self.send(chan, "Dealer shuffled deck..")

		if call == "hand":
			cards = self.bjk.getPlayerHand(user)
			self.send(chan, str("%s's cards : %s" % (user, cards)))

	def send(self, chan, msg):
		self.sendLine("PRIVMSG %s :%s" % (chan, msg))

