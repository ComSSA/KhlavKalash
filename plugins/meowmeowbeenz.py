from plugins.categories import IRegularCommand

import regex
import math

class PlayList:

    def __init__(self):
        self.players = []
        
    def __str__(self):
        return str(self.players)
        
    def append(self,item):
        self.players.append(item)
        
    def find(self, user):
        for player in self.players:
            if player.name == user:
                return player
        
    def sort(self):
        total = len(self.players)
        self.players = sorted(self.players, key=lambda player: player.totalrating)
        for player, ii in zip(self.players, range(1,total+1)):
            x = float(ii)/total
            player.beenz = int(math.ceil(pow(x/5,2) * 125-0.001))
            if player.beenz/5.0 > math.ceil(player.totalrating*5)/5.0:
                player.beenz = int(math.ceil(player.totalrating*5))
            if player.beenz < 1:
                player.beenz = 1
                
    def recalc_ratings(self):
        for ii in range(0,10):
            for player in self.players:
                player.calc_rating(self.players)
            self.sort()
            
class Player:

    def __init__(self, name, beenz, totalrating):
        self.name = name
        self.beenz = beenz
        self.totalrating = totalrating
        self.ratings = []
        
    def __str__ (self):
        return '' + self.name + ' has ' + str(self.beenz) + ' beenz'
        
    def __repr__(self):
        return repr((self.name, self.beenz, self.totalrating))
        
    def addrating(self, rating):
        self.ratings.append(rating)
        
    def findrater(self, name):
        for r in self.ratings:
            if r.rater.name == name:
                return r
        
    def calc_rating(self, players):
        totalweight = 0
        self.totalrating = 0
        for rater in self.ratings:
            totalweight = totalweight + rater.rater.beenz
        for rater in self.ratings:
            self.totalrating = self.totalrating + (rater.rater.beenz*rater.rating)/(float(totalweight)*5)
        if self.totalrating > 1.0:
            self.totalrating = 1.0
        return self.totalrating
        
class Rating:

    def __init__(self, rating, rater):
        self.rating = rating
        self.rater = rater
        
    def __repr__(self):
        return repr((self.rating, self.rater.name))
        
    def editrating(self, rating):
        self.rating = rating

class MeowMeowBeenz (IRegularCommand):
            
    def __init__(self):
        self.playerlist = PlayList()
        
    def command_mmb(self, user, channel, args):
        returnval = ''
        help = 'MeowMeowBeenz, rate everything! \n \",mmb <user> <rating>\" to rate | \",mmb\" to check your rating | \",mmb register\" to start playing | \",mmb help\" to view this message'
        user = user.split('!')[0]
        if len(args) == 0:
            returnval = self.func_self(user)
        elif len(args)  == 1: 
            if args[0] == 'list':
                returnval = self.func_list()
            elif args[0] == 'register':
                returnval = self.func_reg(user)
            elif args[0] == 'help':
                returnval = help
        elif len(args) == 2:
            if 0 < int(args[1]) < 6:
                returnval = self.func_rate(user,args)
            else:
                returnval = user + ', you can only rate people between 1 and 5 MeowMeowBeenz!'
        else:
            returnval = help
        return returnval
            
    def func_reg(self, user):
        player = self.playerlist.find(user)
        if player:
            returnval = user + ', don\'t be silly, you\'re already registered'
        else:
            player = Player(user,1,0.1)
            self.playerlist.append(player)
            self.playerlist.recalc_ratings()
            returnval = user + ' has been registered. RATE EVERYTHING!'
        return returnval
        
    def func_list(self):
        return str(self.playerlist)
        
    def func_self(self, user):
        player = self.playerlist.find(user)
        if player:
            player.calc_rating(self.playerlist)
            self.playerlist.recalc_ratings()
            returnval = str(player)
        else:
            returnval = user + ', you need to register first! Type \",mmb register\"'
        return returnval
        
    def func_rate(self, user, args):
        victim = self.playerlist.find(args[0])
        rater = self.playerlist.find(user)
        if not rater:
            returnval = user + ', you need to register first! Type \",mmb register\"'
        elif victim:
            if user == args[0]:
                returnval = user + ', don\'t be silly, you can\'t rate yourself.'
            else:
                rating = victim.findrater(user)
                if rating:
                    rating.editrating(int(float(args[1])))
                else:
                    victim.addrating(Rating(int(float(args[1])),rater))
                returnval = str(user) + ' rated ' + str(args[0])
        else:
            returnval = args[0] + ', is not registered. To the outlands!'
        self.playerlist.recalc_ratings()
        return returnval