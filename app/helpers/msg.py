
from core.config.lang import MESSAGES, VAL_ERR_MAP

def msg(section: str, key: str, lang: str = "en"):
    return MESSAGES.get(section, {}).get(key, {}).get(lang, "Unknown error")
