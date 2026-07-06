import pytesseract
import pyautogui

from config import TESSERACT_PATH, OCR_LANGS

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def get_ocr_lang():
    if isinstance(OCR_LANGS, dict):
        return "+".join(OCR_LANGS.values())

    return OCR_LANGS


def read_screen_area(left, top, right, bottom):
    width = right - left
    height = bottom - top

    img = pyautogui.screenshot(region=(left, top, width, height))
    text = pytesseract.image_to_string(img, lang=get_ocr_lang()).strip()

    return text


def read_image_area(image, left, top, right, bottom):
    crop = image.crop((left, top, right, bottom))
    text = pytesseract.image_to_string(crop, lang=get_ocr_lang()).strip()

    return text