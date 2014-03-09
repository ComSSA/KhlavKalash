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
        return False
    def sort(self):
        total = len(self.players)
        self.players = sorted(self.players, key=lambda player: player.totalrating)
        for player, ii in zip(self.players, range(1,total+1)):
            x = float(ii)/total
            player.beenz = int(math.ceil(pow(x/5,2) * 125-0.001))
    def recalc_ratings(self):
        for ii in range(0,2):
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
        return False
    def calc_rating(self, players):
        totalweight = 1
        self.totalrating = 0.00001
        for rater in self.ratings:
            totalweight = totalweight + rater.rater.beenz
        for rater in self.ratings:
            self.totalrating = self.totalrating + (rater.rater.beenz*rater.rating)/(float(totalweight)*5)
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
        user = user.split('!')[0]
        if len(args) < 1:
            return self.func_self(user)
        elif len(args) < 2 and args[0] == 'list': #for the debugs
            return self.func_list()
        elif len(args) < 3:
            return self.func_rate(user,args)

    def func_list(self):
        return str(self.playerlist)
        
    def func_self(self, user):
        player = self.playerlist.find(user)
        if player:
            player.calc_rating(self.playerlist)
        else:
            player = Player(user,1,0.1)
            self.playerlist.append(player)
        self.playerlist.recalc_ratings()
        return str(player)
        
    def func_rate(self, user, args):
        victim = self.playerlist.find(args[0])
        rater = self.playerlist.find(user)
        if not rater:
            rater = Player(user,1,0.1)
            self.playerlist.append(rater)
        if victim:
            rating = victim.findrater(user)
            if rating:
                rating.editrating(int(float(args[1])))
            else:
                victim.addrating(Rating(int(float(args[1])),rater))
        else:
            victim = Player(args[0],1,0.1)
            self.playerlist.append(victim)
            victim.addrating(Rating(int(float(args[1])),rater))
        self.playerlist.recalc_ratings()
        return str(user) + ' rated ' + str(args[0])