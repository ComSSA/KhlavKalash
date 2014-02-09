from plugins.categories import ISilentCommand

import sqlite3
import os
import datetime

class SQLogger (ISilentCommand):
	triggers = {r'(.*)': 'log'}

	def __init__(self):
		self.conn = sqlite3.connect('plugins/sqlogger_data/sqlogger.db')
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS Events ( \
			EID INTEGER CONSTRAINT pk PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT, \
			Event TEXT, \
			Context TEXT, \
			Origin TEXT, \
			Body TEXT, \
			TS INTEGER \
			)")

		self.conn.commit()
	
	def trigger_log(self, user, channel, match):
		now = datetime.datetime.now()

		self.conn.execute("INSERT INTO EVENTS (Event, Context, Origin, Body, TS) \
			VALUES('PRIVMSG', ?, ?, ?, ?);", (channel, user, match.group(1), now,))
		
		self.conn.commit()
