import os
import json
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

CARPETA_MODELOS = os.getenv("CARPETA_MODELOS")
CONFIG_JSON = os.getenv("CONFIG_JSON")

with open(CONFIG_JSON, "r") as f:
    CONFIG = json.load(f)
