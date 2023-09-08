import os

from aiogram import Dispatcher
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')

dp = Dispatcher()
