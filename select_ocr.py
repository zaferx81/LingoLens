import tkinter as tk
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

start_x = start_y = end_x = end_y = 0

def on_mouse_down(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    canvas.delete("rect")

def on_mouse_drag(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y
    canvas.delete("rect")
    canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red", width=2, tag="rect")

def on_mouse_up(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y
    root.destroy()

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-alpha", 0.3)
root.attributes("-topmost", True)
root.configure(bg="black")

canvas = tk.Canvas(root, cursor="cross", bg="gray")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

print("Ekranda OCR yapılacak alanı mouse ile seç...")

root.mainloop()

left = min(start_x, end_x)
top = min(start_y, end_y)
right = max(start_x, end_x)
bottom = max(start_y, end_y)

print(f"Seçilen alan: {left}, {top}, {right}, {bottom}")

img = ImageGrab.grab(bbox=(left, top, right, bottom))
text = pytesseract.image_to_string(img, lang="eng+tur")

print("\n--- OCR SONUCU ---\n")
print(text)

input("\nÇıkmak için Enter...")