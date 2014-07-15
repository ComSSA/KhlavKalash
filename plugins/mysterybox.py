from plugins.categories import IRegularCommand
import string
import random
from threading import Timer

class MinMax:
	def __init__(self, players, timer):
		self.numPlayers = players-1
		self.head = MinNode(timer, 0, players)
		self.doMove = self.head.max()

class MinNode:
	def __init__(self, timer, turn, players):
		self.costs = []
		self.bestPath = None
		self.timer = timer
		self.turn = turn
		self.players = players
		if (self.timer > 0):
			self.left = MinNode(self.timer-1,turn+1,players)
			self.right = MinNode(self.timer-2, turn+1,players)
			if (self.timer-2 < 0):
				self.right.costs = []
				for ii in range(self.players):
					if (self.turn%self.players == ii):
						self.right.costs.append(0)
					else: 
						self.right.costs.append(1)
		else:
			self.left = None
			self.right = None
			for ii in range(self.players):
				if (self.turn%self.players == ii):
					self.costs.append(0)
				else: 
					self.costs.append(1)
	def max(self):
		if(self.costs == []):
			self.right.max()
			self.left.max()
			self.bestPath = 0
			if (self.right.costs[self.turn%self.players] > self.left.costs[self.turn%self.players]):
				self.costs = self.right.costs
				self.bestPath = 2
			elif (self.right.costs[self.turn%self.players] < self.left.costs[self.turn%self.players]):
				self.costs = self.left.costs
				self.bestPath = 1
			else:
				for ii in range(self.players):
					self.costs.append(float(self.right.costs[ii]+self.left.costs[ii])/2.0)
					self.bestPath = random.randrange(1,3)
		return self.bestPath

class PlayList:
    def __init__(self):
        self.players = []
        
    def __str__(self):
        return str(self.players)
        
    def append(self,item):
        self.players.append(item)
        
    def find(self, user):
        ii = 0
        for player in self.players:
            if player.name == user:
                return (player, ii)
            ii = ii + 1
        return False
        
class Player:
    def __init__(self, name, lives):
        self.name = name
        self.lives = lives
        
class TheMysteryBox (IRegularCommand):
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.playerlist = PlayList()
        self.box = 0
        self.playerIndex = 0
        self.playing = False
        self.admin = ''
        self.ais  = 0
        
    def command_mysterybox(self, context, user, channel, args):
        self.context = context
        self.channel = channel
        if(len(args) == 0):
            if (not self.playing):
                return self.register(user)
        elif (args[0] == '2' or args[0] == '1'):
            if (self.playing and  self.playerlist.find(user) and self.playerIndex == self.playerlist.find(user)[1]):
                return self.move(int(float(args[0])),user)
        elif (args[0] == 'stop' and user == self.admin):
            return self.stop()
        elif (args[0] == 'start' and self.playing == False):
            return self.start(user)
        elif (args[0] == 'addcom' and self.playing == False):
            self.ais = self.ais + 1
            return self.register('@computer_' + str(self.ais))
            
    def register(self, name):
        if (self.playerlist.find(name) == False):
            self.playerlist.append(Player(name,2))
            return string.split(name,'!')[0] + ' has been registered'
        else:
            return string.split(name,'!')[0] + ' is already registered'
    def ai():
        if (self.playerlist.players[self.playerIndex].name[0] != '@'):
            return ''
        else:
            tree = MinMax(len(self.playerlist.players), self.box)
            return move(tree.doMove, self.playerlist.players[self.playerIndex].name[0])
            
    def start(self, admin):
        if (len(self.playerlist.players) < 2):
            return 'less than 2 people registered!'
        else:
            self.playing = True
            self.box = random.randrange(8,14)
            self.admin = admin
            self.playerIndex = random.randrange(0,len(self.playerlist.players))
            self.timeout = Timer(20.0,self.timeout_callback,[self.playerlist.players[self.playerIndex].name,self.context,self.channel])
            self.timeout.start()
            return string.split(str(self.playerlist.players[self.playerIndex].name),'!')[0] +' has the box with ' + str(self.box) + ' left on the clock'
            
    def stop(self):
        self.reset()
        return 'Admin has stopped the game'
        
    def move(self, move, user):
        self.timeout.cancel()
        if (move > self.box):
            returnstr = self.boom(user)
        elif (move == self.box):
            returnstr = self.boom(self.playerlist.players[(self.playerlist.find(user)[1]+1)%len(self.playerlist.players)].name)
        else:
            self.box = self.box - move
            self.playerIndex = (self.playerIndex+1)%len(self.playerlist.players)
            returnstr = string.split(user,'!')[0] + ' passed the box to ' + string.split(self.playerlist.players[self.playerIndex].name,'!')[0] + '. The box displays the number ' + str(self.box) + '!'
        if (self.playing): #restart the timeout
            self.timeout = Timer(20.0,self.timeout_callback,[self.playerlist.players[self.playerIndex].name,self.context,self.channel])
            self.timeout.start()
        return returnstr + ai()
        
    def timeout_callback(self, user, context, channel):
        context.msg(channel, self.boom(user))

    def boom(self, user):
        player = self.playerlist.find(user)[0]
        player.lives = player.lives-1
        returnstr = 'Boom! ' + string.split(user,'!')[0] + ' has been blown up! They have ' + str(player.lives) + ' lives left.'
        if (player.lives < 1):
            returnstr = returnstr + ' ' + string.split(player.name,'!')[0] + ' is now dead.'
            self.playerlist.players.remove(self.playerlist.find(user)[0])
        if (len(self.playerlist.players) == 1):
            returnstr = returnstr + '\n' + string.split(self.playerlist.players[0].name,'!')[0] + ' has won!'
            self.reset()
        else:
            self.box = self.box = random.randrange(8,14)
            self.playerIndex = random.randrange(0,len(self.playerlist.players))
            returnstr = returnstr + '\n' + string.split(str(self.playerlist.players[self.playerIndex].name),'!')[0] +' has the box with ' + str(self.box) + ' left on the clock'
            self.timeout = Timer(20.0,self.timeout_callback,[self.playerlist.players[self.playerIndex].name,self.context,self.channel])
            self.timeout.start()
        return returnstr