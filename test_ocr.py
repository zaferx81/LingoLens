import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("5 saniye içinde ekranda bir yazı aç...")
input("Hazır olunca Enter bas...")

img = ImageGrab.grab()

text = pytesseract.image_to_string(img, lang="eng+tur")

print("\n--- OCR SONUCU ---\n")
print(text)

input("\nÇıkmak için Enter...")