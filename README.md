# Khlav Kalash!

KhlavKalash is the official IRC bot for the ComSSA IRC channel. 

## How it's built
KhlavKalash is a hack job by @KyeRussell.

KhlavKalash is built using Twisted, which is a Python networking framework. The
bot is pluggable and allows you to write your own Python modules to respond to
commands and triggers.

## Plugin Architecture 
KhlavKalash doesn't do anything remotely useful, yet! This doesn't mean you can't help!

KhlavKalash is fully pluggable, and it's insanely easy! Here's an example plugin that
responds to the command `,hello` with the message "Hello, World!":
```python
from plugins.categories import IRegularCommand

class Uptime (IRegularCommand):
	
	def command_hello(this, *args):
		return "Hello, World!"

```

So easy even a BTech could do it!™

### Command Types
There are two command types that you can hook in your plugins, regular commands or
silenet commands.

#### Regular Commands
Regular commands are the IRC commands you're used to. They usually start with a prefix
and users type them explicitely to trigger an IRC bot, a good example is the `,hello`
example plugin above...it's triggered by the phrase `,hello`, which is meant for the bot.

Plugins that wish to hook this event must subclass `IRegularCommand`. Then, all you do is
create methods prefixed with `command_` and have tuem return what you send back to the user!

Arguments are presumed to be space-separated and are passed (as a list) to the method. For
example, calling `,hello Kye Russell` will call `command_hello` in any plugin responding to
regular commands, with a single parameter, `["Kye", "Russell"]`.

It's a good idea to not use overly generic terms when you hook commands, a user may have many
plugins installed and you don't want multiple plugins hooking a single command.

#### Silent Commands
Silent commands are a tiny bit more difficult, but still insanely easy. Silent commands don't
listen for explicit commands, but instead listen for a particular piece of text that matches
a regular expression! This allows you to trigger commands on any message, regardless of whether
or not it begins with the (configurable) prefix character (by default `,`).

Here's an example of a silent command:
```python
from plugins.categories import ISilentCommand

class URLGrabber (ISilentCommand):
    triggers = {r'(http[s]?://\S+)': "url"}

    def trigger_url(self, match):
        return "%s is a URL!" % match.group(1)
```

As you can see, silent commands must subclass `ISilentCommand`. You then define a dictionary of
regular expression:command pairs, which tells the plugin architecture that you want to hook a
particular expression. In the above example, I am hooking the regular expression `(http[s]?://\S+)`
which is (supposed to) to detect URLs. When the expression is matched the matching method is called,
in this case it's `trigger_url()` because the 'command' for the specified regular expression in
the triggers dictionary is `url`).

Trigger methods are passed one argument, a Python `re.MatchObject` which contains information about the
regular expression that has been matched. What you're probably interested in is the `.group()` method, 
which provides access to the parenthesised (or 'grouped') sections of a matched regular expression; I
have provided an example of this in the example above.

### Plugin Information File
All plugins require a metadata file. This file should be named `modulename.yapsy-plugin`, where `modulename`
is the name of your plugin file. The plugin information should look like this:
```ini
[Core]
Name = My Cool Plugin
Module = coolplugin
   
[Documentation]
Description = Performs awesome tasks!
Author = John Smith
Version = 4.2.0
Website = http://example.com
```

- `Name` is a human-readable plugin name.
- `Module` is the name of the python module file KhlavKalash should load, **without the `.py` extension**.

The rest should be self-explanatory.

### Packaging and Installing
The `.py` file and the acompanying `.yapsy-plugin` file should be placed inside the plugins directory,
which is located in the main KhlavKalash directory.