# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "26342348"))
API_HASH = getenv("API_HASH", "aac8f8c983c97a08db79ece3eee2b9be")
BOT_TOKEN = getenv("BOT_TOKEN", "8307279773:AAEOcFdbSoF0Eciwzdw9xMmF0c1-P39Zh78")
OWNER_ID = list(map(int, getenv("OWNER_ID", "5763227969").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://Ansh089:Ansh089@cluster0.y8tpouc.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1003108906018")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1003108906018"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "500"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "upshrink.com")
AD_API = getenv("AD_API", "aac8f8c983c97a08db79ece3eee2b9be")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
