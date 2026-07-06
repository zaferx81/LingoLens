import os
import webbrowser
import customtkinter as ctk
from PIL import Image

from config import APP_NAME, APP_VERSION
from updater import check_for_updates


LOGO_PATH = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "logo",
    "LingoLens_Logo.png"
)


def open_about_window():
    win = ctk.CTk()
    win.title(f"{APP_NAME} • Hakkında")
    win.geometry("430x620")
    win.resizable(False, False)

    if os.path.exists(LOGO_PATH):
        logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO_PATH),
            dark_image=Image.open(LOGO_PATH),
            size=(120, 120)
        )
        logo_label = ctk.CTkLabel(win, image=logo_img, text="")
        logo_label.pack(pady=(22, 8))

    ctk.CTkLabel(
        win,
        text="LingoLens",
        font=("Arial", 28, "bold")
    ).pack(pady=(4, 2))

    ctk.CTkLabel(
        win,
        text="Offline Screen Translator",
        font=("Arial", 15)
    ).pack(pady=(0, 4))

    ctk.CTkLabel(
        win,
        text=f"Version {APP_VERSION}",
        font=("Arial", 13)
    ).pack(pady=(0, 18))

    ctk.CTkFrame(win, height=2, width=330).pack(pady=(0, 18))

    ctk.CTkLabel(
        win,
        text="📝  F6   Yazı Çevirisi\n\n📷  F7   OCR Çevirisi\n\n🌍  Offline Çeviri",
        justify="left",
        font=("Arial", 15)
    ).pack(pady=(0, 18))

    ctk.CTkFrame(win, height=2, width=330).pack(pady=(0, 18))

    ctk.CTkLabel(
        win,
        text="👨‍💻  Geliştirici\n\nZafer Software\n\n© 2026 All Rights Reserved",
        justify="center",
        font=("Arial", 14)
    ).pack(pady=(0, 18))

    ctk.CTkFrame(win, height=2, width=330).pack(pady=(0, 14))

    def open_website():
        webbrowser.open("https://lingolens.app")

    def check_updates():
        check_for_updates()

    ctk.CTkButton(
        win,
        text="🌐 Web Sitesi",
        width=180,
        command=open_website
    ).pack(pady=5)

    ctk.CTkButton(
        win,
        text="🔄 Güncellemeler",
        width=180,
        command=check_updates
    ).pack(pady=5)

    ctk.CTkButton(
        win,
        text="Kapat",
        width=180,
        command=win.destroy
    ).pack(pady=(12, 20))

    win.mainloop()