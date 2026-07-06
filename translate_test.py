import argostranslate.translate

installed_languages = argostranslate.translate.get_installed_languages()

from_lang = next(filter(lambda x: x.code == "en", installed_languages))
to_lang = next(filter(lambda x: x.code == "tr", installed_languages))

translation = from_lang.get_translation(to_lang)

text = "Hello my friend"
translated = translation.translate(text)

print("Orijinal :", text)
print("Çeviri   :", translated)

input("\nÇıkmak için Enter...")