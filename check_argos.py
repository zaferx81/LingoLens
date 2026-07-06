import argostranslate.translate

langs = argostranslate.translate.get_installed_languages()

print("Kurulu diller:")
for lang in langs:
    print("-", lang.code, lang.name)

input("\nÇıkmak için Enter...")