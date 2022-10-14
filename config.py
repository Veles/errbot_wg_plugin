from asyncio.constants import ACCEPT_RETRY_DELAY
import logging

from plugins.wg import Wg

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py
BACKEND = "Telegram" 
#BACKEND = "Text"  # Errbot will start in text mode (console only mode) and will answer commands from there.

BOT_DATA_DIR = "./err"
BOT_PLUGIN_INDEXES = "https://errbot.io/repos.json"
BOT_EXTRA_PLUGIN_DIR = "./plugins"
CORE_PLUGINS = ()
BOT_LOG_FILE = BOT_DATA_DIR + "/err.log"
BOT_LOG_LEVEL = logging.INFO
BOT_ASYNC = True

# Size of the thread pool for the asynchronous mode.
BOT_ASYNC_POOLSIZE = 10
BOT_ADMINS = (
    "85745624",  
#    "@CHANGE_ME",
)  # Don't leave this as "@CHANGE_ME" if you connect your errbot to a chat system!!
COMPACT_OUTPUT = True
BOT_IDENTITY = {
    ## Text mode
    #"username": "@errbot",  # The name for the bot
    ## Telegram mode (comment the others above if using this mode)
     "token": "5469197565:AAHrK65GL2MMuihxVFJqpa8b1p_D3B9s44c",
}

BOT_PREFIX = "/"
BOT_PREFIX_OPTIONAL_ON_CHAT = True

HIDE_RESTRICTED_COMMANDS = True
HIDE_RESTRICTED_ACCESS = True
ACCESS_CONTROLS = {
    ".*": {"allowusers": BOT_ADMINS, "denyusers": [], "allowrooms": [], "denyrooms": []},
    "wg*": {"allowusers": "*"},
    "help*": {"allowusers": "*"},
    "help": {"allowusers": "*"},
    "fix:": {"allowusers": "*"}
}

BOT_ALT_PREFIXES = ("@errbot", "@errbot ")
