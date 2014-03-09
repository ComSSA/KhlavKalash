#!/usr/bin/env python

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# used in bot functionality
import platform
import re
import os

# read config files
from ConfigParser import SafeConfigParser

# Plugin Architecture 
from yapsy.PluginManager import PluginManagerSingleton
from plugins.categories import IRegularCommand, ISilentCommand
import logging
import sys


class KhlavKalash(irc.IRCClient):
    """The Khlav Kalash IRC bot."""

    def __init__(self, factory):
        self.factory = factory

        # configure  bot settings
        self.nickname = factory.nickname
        self.username = factory.username
        self.realname = factory.realname

        self.prefix = factory.prefix

        self.versionName = "KhlavKalash"
        self.versionNum = 2.0
        self.versionEnv = platform.system() + " " + platform.release()

        # give plugin manager to bot instance.
        self.pm = PluginManagerSingleton.get()
        self.pm.bot = self

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channels)

    def joined(self, channel):
        """Called when the bot joins the channel."""

    def privmsg(self, user, channel, msg):
        """Called when the bot receives a message."""
        # prepare output list
        output = []

        # check to see if it is a command and if it's in the allowed list.
        commandRegex = r'%s(?P<command>\S+)\s*(?P<args>.*)' % self.prefix
        match = re.match(commandRegex, msg)

        if match:
            command = match.group("command").strip()
            args = match.group("args").split()

            # pass the command to all plugins to see if we get a response
            for plugin in self.pm.getPluginsOfCategory("Regular"):
                result = plugin.plugin_object.run(command, user, channel, args)
                if result:
                    output.append(result)

        # check for silent commands
        for plugin in self.pm.getPluginsOfCategory("Silent"):
            output += plugin.plugin_object.run(user, channel, msg)

        # print all collected output
        for current_output in output:
                self.msg(channel, current_output)

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""

    # Utility Methods
    def msg(self, channel, message):
        """Send a message to a specified channel and log it."""
        irc.IRCClient.msg(self, channel, message.encode("utf-8"))

    # Command framework
    def execute(self, command, args):
        """Execute a bot command (just a method in this class)."""
        command_method = getattr(self, command)
        return command_method(args)

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

    # Get config file location
    if len(sys.argv) < 2:
        conf_path = 'KhlavKalash.conf'
    else:
        conf_path = sys.argv[1]

    # Check if config exists.
    if not os.path.isfile(conf_path):
        print "Configuration file '%s' not found, please create it." % conf_path
        sys.exit(1)

    # load the configuration file
    conf = SafeConfigParser()
    conf.read(conf_path)

    # activate debugging mode if necessary.
    if (conf.getboolean("Bot", "debug")):
        logging.basicConfig(level=logging.DEBUG)


    # initialise plugin manager and load plugins
    pm = PluginManagerSingleton.get()
    pm.setPluginPlaces(["plugins"])
    pm.setCategoriesFilter({
        "Regular" : IRegularCommand,
        "Silent"  : ISilentCommand,
    })

    pm.collectPlugins()

    # create protocol and configure.
    f = KhlavKalashStand()

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
