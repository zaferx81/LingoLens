import os
import threading
import keyboard
import pystray
from PIL import Image

from config import APP_NAME, APP_VERSION
from updater import check_for_updates
from settings_window import open_settings_window
from about_window import open_about_window


TRAY_ICON_PATH = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "logo",
    "LingoLens_Logo.png"
)


def quit_app(icon, item=None):
    icon.stop()
    keyboard.unhook_all()
    os._exit(0)


def show_status(icon, item=None):
    icon.notify(
        f"{APP_NAME} v{APP_VERSION}",
        "Çalışıyor | F6: Yazı Çevirisi | F7: OCR Çevirisi | F9: Çıkış"
    )


def open_settings(icon, item=None):
    threading.Thread(target=open_settings_window, daemon=True).start()


def open_about(icon, item=None):
    threading.Thread(target=open_about_window, daemon=True).start()


def check_update_from_tray(icon, item=None):
    found = check_for_updates()
    if not found:
        icon.notify(APP_NAME, "Yeni güncelleme bulunamadı.")


def start_tray_icon():
    if not os.path.exists(TRAY_ICON_PATH):
        return

    image = Image.open(TRAY_ICON_PATH)

    menu = pystray.Menu(
        pystray.MenuItem(f"{APP_NAME} v{APP_VERSION}", show_status, enabled=False),
        pystray.MenuItem("🟢 Durum: Çalışıyor", show_status),
        pystray.Menu.SEPARATOR,

        pystray.MenuItem("📝 F6  Yazı Çevirisi", show_status),
        pystray.MenuItem("📷 F7  OCR Çevirisi", show_status),
        pystray.Menu.SEPARATOR,

        pystray.MenuItem("⚙ Ayarlar", open_settings),
        pystray.MenuItem("🔄 Güncellemeleri Kontrol Et", check_update_from_tray),
        pystray.MenuItem("ℹ Hakkında", open_about),
        pystray.Menu.SEPARATOR,

        pystray.MenuItem("❌ Çıkış", quit_app)
    )

    icon = pystray.Icon(APP_NAME, image, APP_NAME, menu)

    def ready(icon):
        icon.visible = True
        icon.notify(
            f"{APP_NAME} çalışıyor",
            "F6: Yazı Çevirisi | F7: OCR Çevirisi"
        )

    icon.run(setup=ready)


def run_tray_in_thread():
    thread = threading.Thread(target=start_tray_icon, daemon=False)
    thread.start()