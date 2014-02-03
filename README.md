# Khlav Kalash!

KhlavKalash is the official IRC bot for the ComSSA IRC channel. 

## How it's built
KhlavKalash is a hack job by @KyeRussell.

KhlavKalash is built using Twisted, which is a Python networking framework. The
bot has a whitelist of functions which are just textual references to Python
methods. 

## Contributing
KhlavKalash doesn't do anything remotely useful, yet!

You can write your own method and drop it into the KhlavKalash class
to give the bot added functionality, for example:

```python
def hello(self, *args):
	return "Hello, World!"
```

Next you add your command to the whitelist (KhlavKalash.commands):
```python
self.commands = ["uptime", "hello"]
```

I'll make something a bit nicer later.