# Catify Discord Bot

A simple Discord bot that sends cute cat images to your server, with customizable features and easy commands.

## Features
- Rotating status messages about cats
- Automatically posts cat images to a channel every few hours
- `!cat` command: Get a random cat image on demand
- `!setcatfreq <hours>`: Change how often cat images are posted automatically (1-24 hours)
- `!sync`: Set the current channel as the destination for automatic cat images
- `!help`: See all available commands

## Setup
1. **Install dependencies**
   ```sh
   pip install discord.py requests
   ```
2. **Edit `bot.py`**
   - Replace `<YOUR_BOT_TOKEN>` with your Discord bot token.
3. **Run the bot**
   ```sh
   python bot.py
   ```

## Usage
Invite the bot to your server and use these commands:
- `!cat` — Sends a random cat image
- `!setcatfreq <hours>` — Changes how often cat images are posted automatically
- `!sync` — Sets the current channel for automatic cat images
- `!help` — Shows all commands

## Notes
- The bot uses TheCatAPI for images.
- Make sure your bot has permission to send messages and embeds in the target channel.
- The default channel for automatic cat images is set in the code (`cat_channel_id`). Use `!sync` to change it.

## License
MIT
