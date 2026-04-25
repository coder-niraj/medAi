from core.config.lang import MESSAGES


def msg(section: str, key: str, lang: str = "en"):
    return MESSAGES.get(section, {}).get(key, {}).get(lang, "Unknown error")
