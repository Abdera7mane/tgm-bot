import hikari
import os
from dotenv import load_dotenv

import lightbulb

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db 

from config import *

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {'databaseURL': dbUrl_config})

bot = lightbulb.BotApp(
    token=Token,
    default_enabled_guilds=(id)
)

ref = db.reference('/')

ref = db.reference('subjects')

@bot.command
@lightbulb.option('suggestion', 'write a suggestion', type=str)
@lightbulb.command('suggest', 'suggest a TGM subject')
@lightbulb.implements(lightbulb.SlashCommand)
async def suggestion(ctx):
    ref.push({
    'title' : ctx.options.suggestion,
    'status' : 'PENDING',
    'resources' : []
    })
    await ctx.respond("Your suggestion is in th db")


bot.run()