import json
import os
import tempfile
import time
import urllib.request
import customtkinter as ctk
from tkinter import messagebox

from config import APP_VERSION, UPDATE_CHECK_URL


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def is_newer_version(current, latest):
    current_parts = [int(x) for x in current.split(".")]
    latest_parts = [int(x) for x in latest.split(".")]
    return latest_parts > current_parts


def get_update_info():
    try:
        separator = "&" if "?" in UPDATE_CHECK_URL else "?"
        check_url = f"{UPDATE_CHECK_URL}{separator}t={int(time.time())}"

        request = urllib.request.Request(
            check_url,
            headers={
                "User-Agent": "LingoLens-Updater"
            }
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        return data, None

    except Exception as e:
        return None, e


def download_update(download_url, latest_version):
    win = ctk.CTk()
    win.title("LingoLens Güncelleme")
    win.geometry("500x300")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    main_frame = ctk.CTkFrame(
        win,
        corner_radius=18
    )
    main_frame.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=18
    )

    title_label = ctk.CTkLabel(
        main_frame,
        text="LingoLens",
        font=("Segoe UI", 26, "bold")
    )
    title_label.pack(pady=(20, 4))

    subtitle_label = ctk.CTkLabel(
        main_frame,
        text="Güncelleme indiriliyor",
        font=("Segoe UI", 14),
        text_color="#9CA3AF"
    )
    subtitle_label.pack(pady=(0, 14))

    version_label = ctk.CTkLabel(
        main_frame,
        text=f"Yeni sürüm: {latest_version}",
        font=("Segoe UI", 12, "bold")
    )
    version_label.pack(pady=(0, 16))

    progress = ctk.CTkProgressBar(
        main_frame,
        width=400,
        height=18,
        corner_radius=9
    )
    progress.set(0)
    progress.pack(pady=(0, 10))

    percent_label = ctk.CTkLabel(
        main_frame,
        text="%0",
        font=("Segoe UI", 14, "bold")
    )
    percent_label.pack()

    status_label = ctk.CTkLabel(
        main_frame,
        text="Güncelleme dosyaları hazırlanıyor...",
        font=("Segoe UI", 11),
        text_color="#9CA3AF"
    )
    status_label.pack(pady=(8, 0))

    win.update()

    try:
        temp_dir = tempfile.gettempdir()

        installer_path = os.path.join(
            temp_dir,
            "LingoLens_Setup_Update.exe"
        )

        request = urllib.request.Request(
            download_url,
            headers={
                "User-Agent": "LingoLens-Updater"
            }
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            total_size = response.headers.get("Content-Length")

            if total_size:
                total_size = int(total_size)

            downloaded = 0
            block_size = 1024 * 256

            with open(installer_path, "wb") as file:
                while True:
                    chunk = response.read(block_size)

                    if not chunk:
                        break

                    file.write(chunk)
                    downloaded += len(chunk)

                    if total_size:
                        ratio = downloaded / total_size

                        if ratio > 1:
                            ratio = 1

                        progress.set(ratio)

                        percent = int(ratio * 100)

                        percent_label.configure(
                            text=f"%{percent}"
                        )

                    else:
                        percent_label.configure(
                            text=f"{downloaded // (1024 * 1024)} MB"
                        )

                    status_label.configure(
                        text="Güncelleme dosyaları indiriliyor..."
                    )

                    win.update()

        progress.set(1)
        percent_label.configure(text="%100")

        subtitle_label.configure(
            text="İndirme tamamlandı"
        )

        status_label.configure(
            text="Kurulum başlatılıyor..."
        )

        win.update()

        os.startfile(installer_path)

        win.after(800, win.destroy)
        win.update()

        os._exit(0)

    except Exception as e:
        win.destroy()

        messagebox.showerror(
            "Güncelleme Hatası",
            "Güncelleme indirilemedi.\n\n"
            f"Hata:\n{e}"
        )


def show_update_window(
    latest_version,
    notes,
    download_url
):
    win = ctk.CTk()
    win.title("LingoLens Güncelleme")
    win.geometry("540x430")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    result = {
        "update": False
    }

    main_frame = ctk.CTkFrame(
        win,
        corner_radius=18
    )
    main_frame.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=18
    )

    title = ctk.CTkLabel(
        main_frame,
        text="LingoLens",
        font=("Segoe UI", 28, "bold")
    )
    title.pack(pady=(22, 2))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="Yeni Güncelleme Bulundu",
        font=("Segoe UI", 15, "bold"),
        text_color="#3B82F6"
    )
    subtitle.pack(pady=(0, 18))

    version_frame = ctk.CTkFrame(
        main_frame,
        corner_radius=12
    )
    version_frame.pack(
        padx=24,
        pady=(0, 16),
        fill="x"
    )

    current_label = ctk.CTkLabel(
        version_frame,
        text=f"Mevcut sürüm\n{APP_VERSION}",
        font=("Segoe UI", 11),
        justify="center"
    )
    current_label.grid(
        row=0,
        column=0,
        padx=30,
        pady=14
    )

    arrow_label = ctk.CTkLabel(
        version_frame,
        text="→",
        font=("Segoe UI", 22, "bold"),
        text_color="#3B82F6"
    )
    arrow_label.grid(
        row=0,
        column=1,
        padx=10
    )

    new_label = ctk.CTkLabel(
        version_frame,
        text=f"Yeni sürüm\n{latest_version}",
        font=("Segoe UI", 11, "bold"),
        justify="center"
    )
    new_label.grid(
        row=0,
        column=2,
        padx=30,
        pady=14
    )

    version_frame.grid_columnconfigure(
        (0, 1, 2),
        weight=1
    )

    notes_title = ctk.CTkLabel(
        main_frame,
        text="Yenilikler",
        font=("Segoe UI", 12, "bold")
    )
    notes_title.pack(pady=(0, 6))

    notes_box = ctk.CTkTextbox(
        main_frame,
        width=450,
        height=100,
        corner_radius=10,
        wrap="word",
        font=("Segoe UI", 11)
    )
    notes_box.pack(
        padx=22,
        pady=(0, 18)
    )

    notes_box.insert(
        "1.0",
        notes
    )

    notes_box.configure(
        state="disabled"
    )

    button_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    button_frame.pack(pady=(0, 18))

    def update_now():
        result["update"] = True
        win.destroy()

    def later():
        result["update"] = False
        win.destroy()

    update_button = ctk.CTkButton(
        button_frame,
        text="Güncelle",
        width=160,
        height=42,
        corner_radius=10,
        font=("Segoe UI", 12, "bold"),
        command=update_now
    )
    update_button.grid(
        row=0,
        column=0,
        padx=8
    )

    later_button = ctk.CTkButton(
        button_frame,
        text="Daha Sonra",
        width=160,
        height=42,
        corner_radius=10,
        fg_color="#374151",
        hover_color="#4B5563",
        font=("Segoe UI", 12),
        command=later
    )
    later_button.grid(
        row=0,
        column=1,
        padx=8
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        later
    )

    win.mainloop()

    if result["update"]:
        download_update(
            download_url,
            latest_version
        )

    return result["update"]


def check_for_updates():
    data, error = get_update_info()

    if error:
        print(
            "Güncelleme kontrol hatası:",
            repr(error)
        )
        return False

    latest_version = data.get(
        "version"
    )

    notes = data.get(
        "notes",
        ""
    )

    download_url = data.get(
        "download_url",
        ""
    )

    if not latest_version:
        return False

    if not is_newer_version(
        APP_VERSION,
        latest_version
    ):
        return False

    if not download_url:
        messagebox.showerror(
            "Güncelleme Hatası",
            "Güncelleme dosyasının indirme adresi bulunamadı."
        )
        return False

    show_update_window(
        latest_version,
        notes,
        download_url
    )

    return True