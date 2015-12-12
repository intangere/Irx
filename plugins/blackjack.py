from .blackjack import BlackJack

class blackjack():
	def __init__(self, *args):
		self.name = "blackjack"
		self.command = "blackack"
		self.description = "Blackjack for IRC"
		self.args = args[0]
	def run(self):
		call = self.args[0]
		user = self.args[1]
		chan = self.args[2]
		if call == "hit":
			self.bjk.hit(user)
			pass

		if call == "deal":
			self.bjk.deal()
			self.send(chan, "Dealer's cards: %s" % str(self.bjk.players["dealer"]))
			self.send(chan, "%s's cards: %s" % (user, str(self.bjk.players[user])))

		if call == "stand":
			self.bjk.stand(user)
			pass

		if call == "double":
			self.bjk.double(user)
			pass

		if call == "join":
			self.bjk.addPlayerToGame(user)
			self.send(chan, "%s joined the current game!" % user)

		if call == "shuffle":
			self.bjk.shuffle()
			self.send(chan, "Dealer shuffled deck..")

		if call == "cards":
			cards = self.getPlayerCards(user)
			send.send(chan, str("%s's cards : %s" % (user, cards)))