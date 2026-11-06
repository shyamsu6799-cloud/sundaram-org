# SUNDARAM.ORG

A Hindi-first static learning website with a small, privacy-conscious Telegram study bot.

## Telegram study bot

The bot answers `/start` and `/help`, and searches public Wikipedia summaries for general-knowledge and educational questions. It is not an unrestricted people-search tool: it does not search for private contact details, account access, passwords, or personal records. Do not send sensitive personal information to it.

### Suggested Telegram identity

- Display name: **SUNDARAM Study Bot**
- Suggested username: **@SundaramShikshaBot** (must end in `bot`; username availability is determined by Telegram/BotFather)
- Once BotFather confirms and creates that username, its link will be: `https://t.me/SundaramShikshaBot`

I cannot reserve/check the username or create the bot without the owner completing BotFather setup. Never paste the bot token into this repository or a public chat.

### Run it

1. In Telegram, open the verified **@BotFather**, send `/newbot`, choose the display name and an available username ending in `bot`.
2. Copy the token privately. Treat it like a password; if exposed, revoke it with BotFather and create a new one.
3. Install Python 3.10+ and dependencies: `python -m pip install -r requirements.txt`.
4. Set the token as an environment variable (do not commit it):
   - macOS/Linux: `export TELEGRAM_BOT_TOKEN='your-token'`
   - Windows PowerShell: `$env:TELEGRAM_BOT_TOKEN='your-token'`
5. Run `python bot.py` on a computer or server that stays online. Keep the process running; GitHub Pages only hosts the static website and does not run bots.
6. In Telegram, open the bot link and send `/start`.

This starter uses Telegram's long-polling Bot API and Wikipedia's public MediaWiki API. It does not need a database or AI-provider key. Answers are short source summaries, not professional or authoritative advice. Deploy it only on a trusted host, keep the token secret, and add monitoring/rate limits before operating it at scale.
