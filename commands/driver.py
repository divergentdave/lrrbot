import irc
from lrrbot import bot
import storage
import utils

def driver_name():
    return storage.data["show"]["driver"]

@bot.command("driver")
@utils.throttle()
def current_driver(lrrbot, conn, event, respond_to):
	"""
	Command: !game

	Post the game currently being played.
	"""
	driver = lrrbot.get_driver(conn, event, respond_to)
	if driver is None:
		message = "No one is driving the bus"
	else:
		message = "Currently driving: %s" % storage.data["show"]["driver"]
	if lrrbot.driver_override is not None:
		message += " (overridden)"
	conn.privmsg(respond_to, message)

@bot.command("driver override (.*?)")
@utils.mod_only
def override_driver(lrrbot, conn, event, respond_to, driver):
	"""
	Command: !game override NAME
	
	eg: !game override Prayer Warriors: A.O.F.G.
	
	Override what game is being played (eg when the current game isn't in the Twitch database)

	--command
	Command: !game override off
	
	Disable override, go back to getting current game from Twitch stream settings.
	Should the crew start regularly playing a game called "off", I'm sure we'll figure something out.
	"""
	if driver == "" or driver.lower() == "off":
		lrrbot.driver_override = None
		operation = "disabled"
	else:
		lrrbot.driver_override = game
		operation = "enabled"
	lrrbot.get_driver.reset_throttle()
	current_driver.reset_throttle()
	driver = lrrbot.get_driver()
	message = "Override %s. " % operation
	if game is None:
		message += "Not currently playing any game"
	else:
		message += "New driver: %s" % driver
	conn.privmsg(respond_to, message)

@bot.command("driver refresh")
@utils.mod_only
def refresh_driver(lrrbot, conn, event, respond_to):
	"""
	Command: !game refresh

	Force a refresh of the current Twitch game (normally this is updated at most once every 15 minutes)
	"""
	lrrbot.get_driver.reset_throttle()
	current_diver.reset_throttle()
	# current_game(lrrbot, conn, event, respond_to)