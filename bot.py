import os
import discord
import logging
import asyncio
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer le logging
logging.basicConfig(
    filename='bot.log',  # Le fichier où les logs seront écrits
    level=logging.INFO,  # Niveau de logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format des logs
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Récupérer les variables d'environnement
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
URLS = os.getenv("URLS").split(',')  # Récupérer les URLs comme une liste

# Lire les URLs depuis le fichier urls.txt
with open("urls.txt", "r") as file:
    URLS = [line.strip() for line in file.readlines()]
    
# Initialiser le bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionnaire pour stocker le lien le plus récent par URL
latest_links = {}

# Fonction pour scraper la page
def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a réussi
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        ul_element = soup.find('ul', class_='row-content-chapter')
        if ul_element:
            # Trouver le premier lien dans cet élément <ul>
            first_link = ul_element.find('a')
            if first_link:
                return first_link.get('href')
        return None
    except Exception as e:
        logging.error(f"Erreur lors du scraping de {url}: {str(e)}")
        return None

# Fonction pour vérifier les mises à jour
async def check_for_updates():
    global latest_links

    while True:
        found_new_entry = False
        for url in URLS:
            current_link = scrape_page(url)
            if current_link:
                if url not in latest_links:
                    # Si c'est la première fois qu'on voit cette URL, on initialise latest_links
                    latest_links[url] = current_link
                    user = await bot.fetch_user(USER_ID)
                    await user.send(f"Nouveau chapitre:\n{current_link}")
                    logging.info(f"Nouveau lien trouvé pour {url}: {current_link}")
                    found_new_entry = True
                elif current_link != latest_links[url]:
                    # Si un nouveau lien est détecté
                    user = await bot.fetch_user(USER_ID)
                    await user.send(f"Nouveau chapitre:\n{current_link}")
                    # Mettre à jour le lien le plus récent
                    latest_links[url] = current_link
                    logging.info(f"Nouveau lien trouvé pour {url}: {current_link}")
                    found_new_entry = True

        if not found_new_entry:
            logging.info("Aucune nouvelle entrée trouvée pour les URLs surveillées.")
        
        logging.info("Vérification terminée. Attente de 2 minutes avant la prochaine vérification.")
        await asyncio.sleep(120)  # Attendre 2 minutes avant la prochaine vérification

@bot.event
async def on_ready():
    logging.info(f'Bot connecté en tant que {bot.user}')
    
    # Initialiser avec le premier lien pour chaque URL lors du démarrage
    global latest_links
    
    for url in URLS:
        latest_link = scrape_page(url)
        if latest_link:
            latest_links[url] = latest_link
            user = await bot.fetch_user(USER_ID)
            await user.send(f"Nouveau chapitre:\n{latest_link}")
            logging.info(f"Premier lien trouvé pour {url}: {latest_link}")
    
    # Démarrer la vérification périodique
    bot.loop.create_task(check_for_updates())

bot.run(DISCORD_TOKEN)
