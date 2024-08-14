import os
import discord
import logging
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from scraper import scrape_page, check_for_updates_task  # Importation des fonctions depuis les autres fichiers

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer le logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Récupérer les variables d'environnement
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))

# Lire les URLs depuis le fichier urls.txt
with open("urls.txt", "r") as file:
    URLS = [line.strip() for line in file.readlines()]

# Initialiser le bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables globales
latest_links = {}

@bot.event
async def on_ready():
    logging.info(f'Bot connecté en tant que {bot.user}')
    
    # Initialiser avec le premier lien pour chaque URL lors du démarrage
    for url in URLS:
        latest_link = scrape_page(url)
        if latest_link:
            latest_links[url] = latest_link
            user = await bot.fetch_user(USER_ID)
            await user.send(f"Nouveau chapitre:\n{latest_link}")
            logging.info(f"Premier lien trouvé pour {url}: {latest_link}")
    
    # Démarrer la vérification périodique
    bot.loop.create_task(check_for_updates_task(bot, URLS, USER_ID, latest_links))

bot.run(DISCORD_TOKEN)
