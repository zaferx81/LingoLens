def improve_turkish_translation(text):
    if not text:
        return ""

    text = text.strip()

    rules = {
        "Merhaba arkadaşımım": "Merhaba arkadaşım",
        "merhaba arkadaşımım": "merhaba arkadaşım",
        "Merhaba arkadaşımım,": "Merhaba arkadaşım,",
        "merhaba arkadaşımım,": "merhaba arkadaşım,",

        "Merhaba arkadaş,": "Merhaba arkadaşım,",
        "merhaba arkadaş,": "merhaba arkadaşım,",
        "Merhaba arkadaş ": "Merhaba arkadaşım ",
        "merhaba arkadaş ": "merhaba arkadaşım ",

        "İyi hissediyor musunuz?": "İyi misin?",
        "iyi hissediyor musunuz?": "iyi misin?",
        "İyi hissediyor musun?": "İyi misin?",
        "iyi hissediyor musun?": "iyi misin?",

        "Bugün nasılsın?": "bugün nasılsın?",

        "Daha sonra görüşürüz.": "Görüşürüz.",
        "daha sonra görüşürüz.": "görüşürüz.",
        "Size teşekkür ederim.": "Teşekkür ederim.",
        "size teşekkür ederim.": "teşekkür ederim.",
        "Kendine dikkat et.": "Kendine iyi bak.",
        "kendine dikkat et.": "kendine iyi bak.",
    }

    for wrong, correct in rules.items():
        text = text.replace(wrong, correct)

    while "arkadaşımım" in text:
        text = text.replace("arkadaşımım", "arkadaşım")

    text = text.replace("  ", " ")

    return text