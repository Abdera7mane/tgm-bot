from tokenize import Token
import hikari
import os
from dotenv import load_dotenv

load_dotenv()
intents = hikari.Intents.GUILD_VOICE_STATES | hikari.Intents.GUILD_SCHEDULED_EVENTS
intents ^= 

bot = hikari.GatewayBot(token=os.getenv("TOKEN"), intents=hikari.Intents.all())

bot.run()