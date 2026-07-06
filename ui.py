import tkinter as tk
import customtkinter as ctk
import pyperclip
import pyautogui
import subprocess
from PIL import ImageTk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

from config import APP_NAME
from languages import LANGUAGES, DEFAULT_SOURCE_LANGUAGE, DEFAULT_TARGET_LANGUAGE
from translator import translate
from ocr import read_image_area
from settings_manager import load_settings, save_settings
from smart_language import improve_turkish_translation
app_settings = load_settings()

F6_LAST_SOURCE_LANGUAGE = app_settings.get(
    "f6_source_language",
    DEFAULT_SOURCE_LANGUAGE
)

F6_LAST_TARGET_LANGUAGE = app_settings.get(
    "f6_target_language",
    DEFAULT_TARGET_LANGUAGE
)

F7_LAST_TARGET_LANGUAGE = app_settings.get(
    "f7_target_language",
    "Turkish"
)


def fix_turkish_input(text):
    text = text.strip().lower()

    sentence_fixes = {
        "merhaba arkadaşım nasılsın": "merhaba arkadaşım, nasılsın?",
        "merhaba arkadaşım, nasılsın": "merhaba arkadaşım, nasılsın?",
        "selam arkadaşım nasılsın": "merhaba arkadaşım, nasılsın?",
        "sa arkadaşım nasılsın": "merhaba arkadaşım, nasılsın?",
    }

    if text in sentence_fixes:
        return sentence_fixes[text]

    word_fixes = {
        "nasılsın": "nasılsın?",
        "naber": "nasılsın?",
        "nbr": "nasılsın?",
        "selam": "merhaba",
        "sa": "merhaba",
        "arkadasım": "arkadaşım",
        "arkadasim": "arkadaşım",
    }

    for wrong, correct in word_fixes.items():
        text = text.replace(wrong, correct)

    return text


def clean_ocr_text(text):
    if not text:
        return ""

    text = text.replace("|", "I")
    text = text.replace("  ", " ")

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        words = line.split()
        cleaned_words = []

        for word in words:
            clean_word = word.strip()

            if len(cleaned_words) >= 2:
                if clean_word == cleaned_words[-1] and clean_word == cleaned_words[-2]:
                    continue

            cleaned_words.append(clean_word)

        cleaned_line = " ".join(cleaned_words)

        if cleaned_line:
            cleaned_lines.append(cleaned_line)

    return "\n".join(cleaned_lines)
def smart_split_lines(text):
    """
    OCR bazen tüm metni tek satır okuyabiliyor.
    Bu fonksiyon oyun yazılarını daha doğal satırlara ayırmaya çalışır.
    """

    if not text:
        return []

    lines = []

    # Normal satırlar korunur
    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        lines.append(line)

    # Eğer zaten birden fazla satır varsa dokunma
    if len(lines) > 1:
        return lines

    text = lines[0]

    import re

    # Cümle sonlarını satır yap
    text = re.sub(r'([.!?])\s+', r'\1\n', text)

    # Saat
    text = re.sub(r'(\d{1,2}:\d{2})', r'\n\1', text)

    # Yüzde
    text = re.sub(r'(\d+%)', r'\n\1', text)

    # Derece
    text = re.sub(r'(\d+\s?[CFcf])', r'\n\1', text)

    # Madde işareti
    text = text.replace("•", "\n•")
    text = text.replace("►", "\n►")
    text = text.replace("»", "\n»")

    result = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            result.append(line)

    return result


def show_result_window(original_text, translated_text):
    def copy_translation():
        pyperclip.copy(translated_text)
        status_label.configure(text="Çeviri panoya kopyalandı ✅")
        win.after(500, win.destroy)

    def close_window(event=None):
        win.destroy()
        return "break"

    win = ctk.CTk()
    win.title("LingoLens OCR Sonucu")
    win.attributes("-topmost", True)
    win.geometry("700x620+120+80")
    win.resizable(False, False)

    main_frame = ctk.CTkFrame(win, corner_radius=18)
    main_frame.pack(fill="both", expand=True, padx=16, pady=16)

    title = ctk.CTkLabel(main_frame, text="LingoLens", font=("Segoe UI", 26, "bold"))
    title.pack(pady=(18, 4))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="Ekrandan okunan metin ve çeviri",
        font=("Segoe UI", 11),
        text_color="#9CA3AF"
    )
    subtitle.pack(pady=(0, 16))

    src_label = ctk.CTkLabel(main_frame, text="Okunan Metin", font=("Segoe UI", 12, "bold"))
    src_label.pack(anchor="w", padx=18)

    src_box = ctk.CTkTextbox(main_frame, wrap="word", font=("Segoe UI", 12), height=145, corner_radius=12)
    src_box.pack(fill="both", padx=18, pady=(6, 14))
    src_box.insert("1.0", original_text)
    src_box.configure(state="disabled")

    tr_label = ctk.CTkLabel(main_frame, text="Çeviri", font=("Segoe UI", 12, "bold"))
    tr_label.pack(anchor="w", padx=18)

    tr_box = ctk.CTkTextbox(main_frame, wrap="word", font=("Segoe UI", 12), height=165, corner_radius=12)
    tr_box.pack(fill="both", padx=18, pady=(6, 14))
    tr_box.insert("1.0", translated_text)
    tr_box.configure(state="disabled")

    bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    bottom_frame.pack(fill="x", padx=18, pady=(0, 14))

    status_label = ctk.CTkLabel(
        bottom_frame,
        text="F7 sonucu hazır",
        font=("Segoe UI", 10),
        text_color="#9CA3AF"
    )
    status_label.pack(side="left")

    copy_btn = ctk.CTkButton(
        bottom_frame,
        text="Kopyala",
        command=copy_translation,
        width=95,
        height=34,
        corner_radius=10,
        font=("Segoe UI", 11, "bold")
    )
    copy_btn.pack(side="right", padx=(8, 0))

    close_btn = ctk.CTkButton(
        bottom_frame,
        text="Kapat",
        command=win.destroy,
        width=95,
        height=34,
        corner_radius=10,
        fg_color="#374151",
        hover_color="#4B5563",
        font=("Segoe UI", 11, "bold")
    )
    close_btn.pack(side="right")

    win.bind("<Escape>", close_window)
    win.mainloop()


def open_write_translate_window():
    placeholder_text = "Buraya yazın..."

    def set_placeholder():
        input_box.delete("1.0", "end")
        input_box.insert("1.0", placeholder_text)
        input_box.configure(text_color="#6B7280")

    def clear_placeholder(event=None):
        current_text = input_box.get("1.0", "end").strip()
        if current_text == placeholder_text:
            input_box.delete("1.0", "end")
            input_box.configure(text_color="#F9FAFB")

    def translate_and_copy(event=None):
        global F6_LAST_SOURCE_LANGUAGE
        global F6_LAST_TARGET_LANGUAGE

        text = input_box.get("1.0", "end").strip()

        if text == placeholder_text:
            text = ""

        text = fix_turkish_input(text)

        if not text:
            status_label.configure(text="Önce bir metin yaz ✍️")
            return "break"

        source_name = source_combo.get()
        target_name = target_combo.get()

        from_code = LANGUAGES[source_name]
        to_code = LANGUAGES[target_name]

        global F6_LAST_SOURCE_LANGUAGE
        global F6_LAST_TARGET_LANGUAGE

        F6_LAST_SOURCE_LANGUAGE = source_name
        F6_LAST_TARGET_LANGUAGE = target_name

        app_settings["f6_source_language"] = source_name
        app_settings["f6_target_language"] = target_name

        save_settings(app_settings)

        result = translate(text, from_code, to_code)

        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Set-Clipboard -Value ([Console]::In.ReadToEnd())"
            ],
            input=result,
            text=True,
            check=False
        )
        
        print("Panoya kopyalandı:", result)
        win.after(700, win.destroy)
        return "break"

    def swap_languages():
        source_name = source_combo.get()
        target_name = target_combo.get()

        source_combo.set(target_name)
        target_combo.set(source_name)

        status_label.configure(text="Diller değiştirildi ⇄")

    def close_window(event=None):
        win.destroy()
        return "break"

    win = ctk.CTk()
    win.title("LingoLens")
    win.attributes("-topmost", True)
    win.geometry("520x360+150+150")
    win.resizable(False, False)

    main_frame = ctk.CTkFrame(win, corner_radius=18)
    main_frame.pack(fill="both", expand=True, padx=16, pady=16)

    title = ctk.CTkLabel(main_frame, text="LingoLens", font=("Segoe UI", 25, "bold"))
    title.pack(pady=(18, 2))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="Write • Translate • Copy",
        font=("Segoe UI", 11),
        text_color="#9CA3AF"
    )
    subtitle.pack(pady=(0, 16))

    lang_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    lang_frame.pack(pady=(0, 10))

    source_block = ctk.CTkFrame(lang_frame, fg_color="transparent")
    source_block.grid(row=0, column=0, padx=(0, 10))

    source_label = ctk.CTkLabel(source_block, text="Kaynak Dil", font=("Segoe UI", 10, "bold"))
    source_label.pack(anchor="w", pady=(0, 4))

    source_combo = ctk.CTkComboBox(
        source_block,
        values=list(LANGUAGES.keys()),
        width=180,
        height=34,
        corner_radius=8,
        state="readonly"
    )
    source_combo.set(DEFAULT_SOURCE_LANGUAGE)
    source_combo.pack()

    swap_btn = ctk.CTkButton(
        lang_frame,
        text="⇄",
        command=swap_languages,
        width=34,
        height=34,
        corner_radius=17,
        font=("Segoe UI", 18, "bold")
    )
    swap_btn.grid(row=0, column=1, padx=6, pady=(22, 0))

    target_block = ctk.CTkFrame(lang_frame, fg_color="transparent")
    target_block.grid(row=0, column=2, padx=(10, 0))

    target_label = ctk.CTkLabel(target_block, text="Hedef Dil", font=("Segoe UI", 10, "bold"))
    target_label.pack(anchor="w", pady=(0, 4))

    target_combo = ctk.CTkComboBox(
        target_block,
        values=list(LANGUAGES.keys()),
        width=180,
        height=34,
        corner_radius=8,
        state="readonly"
    )
    target_combo.set(F6_LAST_TARGET_LANGUAGE)
    target_combo.pack()

    input_box = ctk.CTkTextbox(main_frame, wrap="word", font=("Segoe UI", 13), height=95, corner_radius=12)
    input_box.pack(fill="x", padx=18, pady=(4, 12))

    set_placeholder()
    input_box.bind("<FocusIn>", clear_placeholder)

    translate_btn = ctk.CTkButton(
        main_frame,
        text="Çevir ve Kopyala",
        command=translate_and_copy,
        width=180,
        height=34,
        corner_radius=10,
        font=("Segoe UI", 12, "bold")
    )
    translate_btn.pack(pady=(0, 10))

    bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    bottom_frame.pack(fill="x", padx=18, pady=(0, 8))

    status_label = ctk.CTkLabel(
        bottom_frame,
        text="Enter = Çevir",
        font=("Segoe UI", 10),
        text_color="#9CA3AF"
    )
    status_label.pack(side="left")

    close_label = ctk.CTkLabel(
        bottom_frame,
        text="Esc = Kapat",
        font=("Segoe UI", 10),
        text_color="#9CA3AF"
    )
    close_label.pack(side="right")

    input_box.bind("<Return>", translate_and_copy)
    win.bind("<Escape>", close_window)

    input_box.focus()
    win.mainloop()


def choose_f7_target_language():
    global F7_LAST_TARGET_LANGUAGE

    selected = {"target": F7_LAST_TARGET_LANGUAGE}

    def start():
        global F7_LAST_TARGET_LANGUAGE

        selected["target"] = target_combo.get()
        F7_LAST_TARGET_LANGUAGE = selected["target"]

        app_settings["f7_target_language"] = F7_LAST_TARGET_LANGUAGE
        save_settings(app_settings)

        win.destroy()

    def close_window(event=None):
        win.destroy()
        return "break"
    
    win = ctk.CTk()
    win.title("LingoLens OCR")
    win.attributes("-topmost", True)
    win.geometry("380x250+200+180")
    win.resizable(False, False)

    main_frame = ctk.CTkFrame(win, corner_radius=18)
    main_frame.pack(fill="both", expand=True, padx=16, pady=16)

    title = ctk.CTkLabel(main_frame, text="LingoLens OCR", font=("Segoe UI", 24, "bold"))
    title.pack(pady=(20, 4))

    subtitle = ctk.CTkLabel(
        main_frame,
        text="Ekrandan yazıyı seç ve çevir",
        font=("Segoe UI", 11),
        text_color="#9CA3AF"
    )
    subtitle.pack(pady=(0, 18))

    label = ctk.CTkLabel(main_frame, text="Hedef Dil", font=("Segoe UI", 11, "bold"))
    label.pack(pady=(0, 5))

    target_combo = ctk.CTkComboBox(
        main_frame,
        values=list(LANGUAGES.keys()),
        width=220,
        height=34,
        corner_radius=8,
        state="readonly"
    )
    target_combo.set(F7_LAST_TARGET_LANGUAGE)
    target_combo.pack(pady=(0, 18))

    start_btn = ctk.CTkButton(
        main_frame,
        text="OCR Başlat",
        command=start,
        width=180,
        height=36,
        corner_radius=10,
        font=("Segoe UI", 12, "bold")
    )
    start_btn.pack()

    info_label = ctk.CTkLabel(
        main_frame,
        text="ESC = Kapat",
        font=("Segoe UI", 10),
        text_color="#9CA3AF"
    )
    info_label.pack(pady=(16, 0))

    win.bind("<Escape>", close_window)
    win.mainloop()

    return selected["target"]


def select_area_and_ocr_translate():
    target_name = choose_f7_target_language()
    target_code = LANGUAGES[target_name]
    
    import time
    time.sleep(0.3)

    frozen_image = pyautogui.screenshot()

    start_x = start_y = end_x = end_y = 0

    def on_mouse_down(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y
        canvas.delete("rect")

    def on_mouse_drag(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x, event.y
        canvas.delete("rect")
        canvas.create_rectangle(
            start_x,
            start_y,
            end_x,
            end_y,
            outline="red",
            width=3,
            tag="rect"
        )

    def on_mouse_up(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x, event.y
        root.destroy()

    def cancel_selection(event=None):
        root.destroy()
        return "break"

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)

    screen_image = ImageTk.PhotoImage(frozen_image)

    canvas = tk.Canvas(root, cursor="cross", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.create_image(0, 0, image=screen_image, anchor="nw")

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)
    root.bind("<Escape>", cancel_selection)

    print("Donmuş ekrandan alan seç...")
    root.mainloop()

    left = min(start_x, end_x)
    top = min(start_y, end_y)
    right = max(start_x, end_x)
    bottom = max(start_y, end_y)

    if right - left < 5 or bottom - top < 5:
        return

    original_text = read_image_area(
        frozen_image,
        left,
        top,
        right,
        bottom
    )

    original_text = clean_ocr_text(original_text)

    if original_text:
        original_lines = smart_split_lines(original_text)
        translated_lines = []

        for line in original_lines:
            line = line.strip()

            if not line:
                continue

            translated_line = translate(line, "en", target_code)
            translated_line = clean_ocr_text(translated_line)

            if target_name == "Turkish":
                translated_line = improve_turkish_translation(translated_line)

            translated_lines.append(f"({translated_line})")

        translated_text = "\n".join(translated_lines)

    else:
        original_text = "Metin okunamadı."
        translated_text = "Metin okunamadı."

    print("\n--- OCR SONUCU ---")
    print(original_text)

    print("\n--- ÇEVİRİ ---")
    print(translated_text)

    print("------------------\n")

    show_result_window(original_text, translated_text)