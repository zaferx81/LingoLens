import customtkinter as ctk

from settings_manager import load_settings, save_settings
from config import APP_NAME


def open_settings_window():
    settings = load_settings()

    win = ctk.CTk()
    win.title(f"{APP_NAME} Ayarlar")
    win.geometry("420x360")
    win.resizable(False, False)

    title = ctk.CTkLabel(
        win,
        text="LingoLens Ayarlar",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=(25, 10))

    check_updates = ctk.BooleanVar(value=settings.get("check_updates_on_start", True))
    remember_languages = ctk.BooleanVar(value=settings.get("remember_languages", True))
    show_notifications = ctk.BooleanVar(value=settings.get("show_notifications", True))
    dark_theme = ctk.BooleanVar(value=settings.get("dark_theme", True))

    ctk.CTkCheckBox(win, text="Açılışta güncelleme kontrol et", variable=check_updates).pack(anchor="w", padx=45, pady=8)
    ctk.CTkCheckBox(win, text="Son kullanılan dili hatırla", variable=remember_languages).pack(anchor="w", padx=45, pady=8)
    ctk.CTkCheckBox(win, text="Bildirimleri göster", variable=show_notifications).pack(anchor="w", padx=45, pady=8)
    ctk.CTkCheckBox(win, text="Karanlık tema", variable=dark_theme).pack(anchor="w", padx=45, pady=8)

    def save_and_close():
        settings["check_updates_on_start"] = check_updates.get()
        settings["remember_languages"] = remember_languages.get()
        settings["show_notifications"] = show_notifications.get()
        settings["dark_theme"] = dark_theme.get()
        save_settings(settings)
        win.destroy()

    ctk.CTkButton(
        win,
        text="Kaydet",
        width=140,
        command=save_and_close
    ).pack(pady=25)

    win.mainloop()