import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Mouse ile değil, şimdilik sabit alan okuyacağız.")
print("Not Defteri'ni ekranın sol üstüne yakın aç ve yazıyı görünür bırak.")

input("Hazır olunca Enter bas...")

# Sol, üst, sağ, alt koordinatlar
bbox = (100, 100, 900, 500)

img = ImageGrab.grab(bbox=bbox)

text = pytesseract.image_to_string(img, lang="eng+tur")

print("\n--- SEÇİLEN BÖLGE OCR SONUCU ---\n")
print(text)

input("\nÇıkmak için Enter...")