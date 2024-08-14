import logging
import requests
from bs4 import BeautifulSoup
import asyncio

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
async def check_for_updates_task(bot, urls, user_id, latest_links):
    while True:
        found_new_entry = False
        for url in urls:
            current_link = scrape_page(url)
            if current_link:
                if url not in latest_links:
                    latest_links[url] = current_link
                    user = await bot.fetch_user(user_id)
                    await user.send(f"Nouveau chapitre:\n{current_link}")
                    logging.info(f"Nouveau lien trouvé pour {url}: {current_link}")
                    found_new_entry = True
                elif current_link != latest_links[url]:
                    user = await bot.fetch_user(user_id)
                    await user.send(f"Nouveau chapitre:\n{current_link}")
                    latest_links[url] = current_link
                    logging.info(f"Nouveau lien trouvé pour {url}: {current_link}")
                    found_new_entry = True

        if not found_new_entry:
            logging.info("Aucune nouvelle entrée trouvée pour les URLs surveillées.")
        
        logging.info("Vérification terminée. Attente de 2 minutes avant la prochaine vérification.")
        await asyncio.sleep(120)
