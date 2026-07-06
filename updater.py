import json
import urllib.request
from tkinter import messagebox
from config import APP_VERSION, UPDATE_CHECK_URL


def is_newer_version(current, latest):
    current_parts = [int(x) for x in current.split(".")]
    latest_parts = [int(x) for x in latest.split(".")]
    return latest_parts > current_parts


def check_for_updates():
    try:
        with urllib.request.urlopen(UPDATE_CHECK_URL, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        latest_version = data.get("version")
        notes = data.get("notes", "")
        download_url = data.get("download_url", "")

        if latest_version and is_newer_version(APP_VERSION, latest_version):
            messagebox.showinfo(
                "Yeni Güncelleme Bulundu",
                f"LingoLens yeni sürümü hazır!\n\n"
                f"Mevcut sürüm: {APP_VERSION}\n"
                f"Yeni sürüm: {latest_version}\n\n"
                f"Yenilikler:\n{notes}\n\n"
                f"İndirme adresi:\n{download_url}"
            )
            return True

        return False

    except Exception:
        return False