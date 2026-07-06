import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "check_updates_on_start": True,
    "remember_languages": True,
    "show_notifications": True,
    "dark_theme": True,

    "f6_source_language": "Turkish",
    "f6_target_language": "English",
    "f7_target_language": "Turkish"
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        # Yeni sürümlerde eksik ayarlar otomatik eklensin
        changed = False

        for key, value in DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = value
                changed = True

        if changed:
            save_settings(settings)

        return settings

    except Exception:
        save_settings(DEFAULT_SETTINGS.copy())
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)