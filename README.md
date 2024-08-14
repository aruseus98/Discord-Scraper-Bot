# Discord Scraper Bot

A Python Discord bot that monitors web pages for new chapters and sends private notifications when a new link is detected.A Python Discord bot that monitors web pages for new chapters and sends private notifications when a new link is detected.  

## Prerequisites

* Python 3.8+  
* Docker  
* A Discord Bot token  
* A .env file with the necessary environment variables  

## Installation

1. Clone the repository:  
```
git clone https://github.com/your-username/discord-scraper-bot.git
cd discord-scraper-bot
```

2. Configure environment variables:  

Create a .env file at the root of the project and add your Discord token and user ID:  
```
DISCORD_TOKEN=your_discord_token
USER_ID=your_user_id
```

3. Add URLs to monitor:  

Add the URLs you want to monitor in the urls.txt file, one URL per line.  

# Using with Docker

1. Build the Docker image:  
```
docker build -t discord-scraper-bot .
```

2. Run the Docker container:  
```
docker run -d --name discord-scraper-bot --env-file .env discord-scraper-bot
```

The bot will connect to Discord, start monitoring the specified URLs, and send you notifications when a new update is found.  

## Project Structure

* bot.py: Main bot file
* scraper.py: Contains the scraping and update-checking functions
* urls.txt: File containing the URLs to monitor
* .env: Environment variables file (not included in the repository)

## Logs

Logs are recorded in the bot.log file.