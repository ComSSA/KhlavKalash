# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# used in bot functionality
import platform
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from socket import gethostname

# read config files
from ConfigParser import SafeConfigParser

# system imports
import time, sys

class MessageLogger:
    """
    A logging class.
    """
    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class KhlavKalash(irc.IRCClient):
    """The Khlav Kalash IRC bot."""

    def __init__(self, factory):
        self.factory = factory

        self.nickname = factory.nickname
        self.username = factory.username
        self.realname = factory.realname

        self.prefix = factory.prefix

        self.versionName = "KhlavKalash"
        self.versionNum = 1.0
        self.versionEnv = platform.system() + " " + platform.release()

        self.commands = ["uptime", "load"]
        self.silentCommands = {r'(http[s]?://\S+)': "url"}

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channels)


    def joined(self, channel):
        """Called when the bot joins the channel."""
        self.logger.log("[Joined %s]" % channel)


    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message."""

        # log the message
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))

        # Otherwise check to see if it is a command and if it's in the allowed list.
        commandRegex = r'%s(?P<command>\S+)\s*(?P<args>.*)' % self.prefix
        match = re.match(commandRegex, msg)

        if match:
            output = ""
            command = match.group("command").strip()
            allowed = [availableCommand for availableCommand in self.commands if availableCommand == command]

            if allowed:
                args = match.group("args")
                output = self.execute(command, args)

                self.msg(channel, output)
            else:
                self.logger.log("Invalid command %s executed by %s in %s" % (command, user, channel))

        # Check if silent command criteria has been met.
        for currentRegex in self.silentCommands:
            match = re.findall(currentRegex, msg)

            if match:
                command = self.silentCommands[currentRegex]
                output = self.execute(command, match)

                if output:
                    self.msg(channel, output)


    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))


    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    # Utility Methods
    def msg(self, channel, message):
        """Send a message to a specified channel and log it."""
        irc.IRCClient.msg(self, channel, message.encode("utf-8"))
        self.logger.log("<%s> %s" % (self.nickname, message.encode("utf-8")))


    # Command framework
    def execute(self, command, args):
        """Execute a bot command (just a method in this class)."""
        command_method = getattr(self, command)
        return command_method(args)

    # Commands
    def uptime(self, *args):
        return "Uptime for %s: " % gethostname() + subprocess.check_output(["uptime"])

    def url(self, *args):
        response = requests.get(args[0][0])
        soup = BeautifulSoup(response.text)

        if soup.title and soup.title.text:
            title = ' '.join(soup.title.string.replace('\n', '').split())
            
            if len(title) > 120:
                title = title[:117] + "..."

            return title





class KhlavKalashStand(protocol.ClientFactory):
    """A factory for KhlavKalash.

    Khlav kalash! Get your khlav kalash!
    """

    def buildProtocol(self, addr):
        p = KhlavKalash(self)
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create protocol and configure.
    f = KhlavKalashStand()

    conf = SafeConfigParser()
    conf.read('KhlavKalash.conf')

    f.nickname = conf.get('Bot', 'nickname')
    f.username = conf.get('Bot', 'username')
    f.realname = conf.get('Bot', 'realname')
    f.prefix = conf.get('Bot', 'prefix')
    f.channels = conf.get('Server', 'channels')
    f.filename = conf.get('Logging', 'filename')

    reactor.connectTCP(conf.get('Server', 'hostname'), 
        int(conf.get('Server', 'port')), f)

    # run bot
    reactor.run()