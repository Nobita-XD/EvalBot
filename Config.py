from os import getenv

SESSION = getenv("SESSION", "session")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
AUTH = list(map(int, getenv("AUTH").split()))
