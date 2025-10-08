import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LITE = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'users.db')}"

# bot config from env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
