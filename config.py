from dotenv import load_dotenv
import os

# .env faylni yuklaymiz
load_dotenv()


TOKEN= os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
raw_admins = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(i.strip()) for i in raw_admins.split(",") if i.strip().isdigit()]
 
TG_CHANNEL_URL = os.getenv("TG_CHANNEL_URL")
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL")
BOT_USERNAME = os.getenv("BOT_USERNAME")
USER_DATA_FILE = "users.json"
EVENT_DATA_FILE = "events.json"
EVENT_PARTICIPANTS_FILE = 'event_participants.json'