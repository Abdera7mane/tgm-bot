################################Remarques##############################

#Assurez-vous d'activer l'environnement virtuel/evn 
#Chaque fois que vous apportez des modifications, fermez le bot dans le terminal, puis redémarrez-le.  Il contiendra alors vos modifications. 

########################################################################



#bot lib
import hikari
import lightbulb

#var lib
#Les variables d'environnement sont plus sécurisées et doivent être utilisées lors du téléchargement de votre projet vers un système de contrôle de version tel que git. 
#définissez les variables d'environnement dans un nouveau .env. Le .env peut également être ajouté à votre .gitginore (si vous utilisez git), afin que vos informations d'identification ne soient pas exposées publiquement sur une plate-forme comme GitHub
from dotenv import load_dotenv
import os


# prend les variables d'environnement de .env. 
load_dotenv ()


variables_keys = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
    }
  

TOKEN = os.getenv('TOKEN')
databaseurl = os.getenv('databaseurl')

#db lib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db 

#établir une connexion avec Google Firebase .. 
cred = credentials.Certificate(variables_keys)
firebase_admin.initialize_app(cred, {'databaseURL': databaseurl})

#connectez vous au bot grace au token 
bot = lightbulb.BotApp(prefix="!", token=TOKEN , intents=hikari.Intents.ALL_UNPRIVILEGED)

#préparez la hiérarchie de votre base de données (dans notre cas, la suggestion apparaît en fonction du nom d'utilisateur)
#Obtenez une référence de base de données sur les sujet
ref = db.reference('subjects')


#preparez une première commande 
@bot.command
#nous pouvons ajouter des options à nos commandes
#nom de l'option, descriptioin
@lightbulb.option('resources', 'add the resources')
@lightbulb.option('suggestion', 'add your suggestion')
#nom de la commande, description de la commande 
@lightbulb.command('suggest', 'suggest a TGM subject')

#c'est une commande prefix .. lors de la création des commandes prefix (tapez ![nom de la commande]) 
#nous pouvons utiliser des commandes slash aussi (taper \[nom de la commande])
@lightbulb.implements(lightbulb.PrefixCommand)
async def suggestion(ctx: lightbulb.Context):
    #envoyer les donnée a la base de donnée
    users_ref = ref.child( ctx.user.username)
    users_ref.push({
            'resources' : ctx.options.resources,
            'title' : ctx.options.suggestion,
            'status' : 'PENDING',
})

    await ctx.respond("dear " + ctx.user.mention + " your suggestion has been successfully added to our database .. Thank you!")


bot.run()