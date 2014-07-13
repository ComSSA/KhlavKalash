from plugins.categories import IRegularCommand
import string
import random
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
        self.playerlist = PlayList()
        self.box = 0
        self.playerIndex = 0
        self.playing = False
        self.admin = ''
        
    def command_mysterybox(self, user, channel, args):
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
            
    def register(self, name):
        if (self.playerlist.find(name) == False):
            self.playerlist.append(Player(name,2))
            return string.split(name,'!')[0] + ' has been registered'
        else:
            return string.split(name,'!')[0] + ' is already registered'
            
    def start(self, admin):
        if (len(self.playerlist.players) < 2):
            return 'less than 2 people registered!'
        else:
            self.playing = True
            self.box = random.randrange(8,14)
            self.admin = admin
            self.playerIndex = random.randrange(0,len(self.playerlist.players))
            return string.split(str(self.playerlist.players[self.playerIndex].name),'!')[0] +' has the box with ' + str(self.box) + ' left on the clock'
            
    def stop(self):
        self.playerlist = PlayList()
        self.box = 0
        self.playerIndex = 0
        self.playing = False
        self.admin = ''
        return 'Admin has stopped the game'
        
    def move(self, move, user):
        if (move > self.box):
            return self.boom(user)
        elif (move == self.box):
            return self.boom(self.playerlist.players[(self.playerlist.find(user)[1]+1)%len(self.playerlist.players)].name)
        else:
            self.box = self.box - move
            self.playerIndex = (self.playerIndex+1)%len(self.playerlist.players)
            return string.split(user,'!')[0] + ' passed the box to ' + string.split(self.playerlist.players[self.playerIndex].name,'!')[0] + '. The box displays the number ' + str(self.box) + '!'
            
    def boom(self, user):
        player = self.playerlist.find(user)[0]
        player.lives = player.lives-1
        returnstr = 'Boom! ' + string.split(user,'!')[0] + ' has been blown up! They have ' + str(player.lives) + ' lives left.'
        if (player.lives < 1):
            returnstr = returnstr + ' ' + string.split(player.name,'!')[0] + ' is now dead.'
            self.playerlist.players.remove(self.playerlist.find(user)[0])
        if (len(self.playerlist.players) == 1):
            returnstr = returnstr + '\n' + string.split(self.playerlist.players[0],'!')[0] + ' has won!'
            self.playerlist = PlayList()
            self.box = 0
            self.playerIndex = 0
            self.playing = False
            self.admin = ''
        else:
            self.box = self.box = random.randrange(8,14)
            self.playerIndex = random.randrange(0,len(self.playerlist.players))
            returnstr = returnstr + '\n' + string.split(str(self.playerlist.players[self.playerIndex].name),'!')[0] +' has the box with ' + str(self.box) + ' left on the clock'
        return returnstr