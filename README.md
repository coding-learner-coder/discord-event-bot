<<<<<<< HEAD
# Discord Event Bot

This repository contains a small Discord bot that announces events. To keep your bot token secret when publishing to GitHub or deploying to Railway, the token must be provided via an environment variable (or a local `.env` file which should NOT be committed).

Local setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\Activate.ps1 on Windows PowerShell
pip install -r requirements.txt
```

2. Create a `.env` file (do NOT commit it):

```
DISCORD_TOKEN=your_bot_token_here
```

3. Run locally:

```bash
python bot.py
```

Deploying to Railway

- In Railway (or any other host), set an environment variable named `DISCORD_TOKEN` with your bot token in the project settings. Do not add the token to source control.
- Optional: set `ENABLE_MESSAGE_CONTENT=true` if your bot uses message content-based prefix commands (also enable the intent in the Discord Developer Portal).

Security notes

- `.env` is listed in `.gitignore` so it will not be committed. Keep your token private.
- If you ever regenerate the token in the Developer Portal, update the Railway environment variable or your local `.env`.
# discord-event-bot

Small Discord bot to announce 3-hour events.

Setup (Windows):

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (uses the Python interpreter shown when you run the bot):

```powershell
& "C:/Users/world family/AppData/Local/Python/pythoncore-3.12-64/python.exe" -m pip install -r requirements.txt
```

3. Run the bot:

```powershell
& "C:/Users/world family/AppData/Local/Python/pythoncore-3.12-64/python.exe" bot.py
```

Troubleshooting:
- If VS Code still shows "Import 'discord' could not be resolved", set the Python interpreter in the bottom-right to the interpreter above, then reload the window.
- If using a virtualenv, set `python.analysis.extraPaths` in `.vscode/settings.json` to the venv `Lib\site-packages` path.
=======
# discord-event-bot
>>>>>>> a2169c126e1cef898c38339ca0714d7a7eec2f6c
