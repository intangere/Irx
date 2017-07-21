# Irx
Twisted IRC Library<br><br>
For nickserv authentication add this line to signedOn() in Iris.py:<br>
````
self.sendLine('PRIVMSG NICKSERV IDENTIFY %s' % irx.config.password)
````
