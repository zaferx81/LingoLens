import time
import os
import keyboard

from config import APP_NAME, APP_VERSION
from settings_manager import load_settings
from updater import check_for_updates
from tray import run_tray_in_thread


def exit_app():
    print(f"{APP_NAME} kapatılıyor...")
    keyboard.unhook_all()
    os._exit(0)


def main():
    settings = load_settings()

    print(f"{APP_NAME} v{APP_VERSION} çalışıyor.")
    print("F6 = Yazı yaz, hedef dil seç, çevir ve panoya kopyala")
    print("F7 = Alan seç, OCR yap ve Türkçeye çevir")
    print("F9 = Çıkış")

    run_tray_in_thread()

    if settings.get("check_updates_on_start", True):
        check_for_updates()

    from ui import open_write_translate_window, select_area_and_ocr_translate

    keyboard.add_hotkey("f6", open_write_translate_window)
    keyboard.add_hotkey("f7", select_area_and_ocr_translate)
    keyboard.add_hotkey("f9", exit_app)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        exit_app()


if __name__ == "__main__":
    main()