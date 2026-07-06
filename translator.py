import argostranslate.translate


def get_installed_languages():
    return argostranslate.translate.get_installed_languages()


def _get_language(code):
    installed_languages = get_installed_languages()

    return next(
        (lang for lang in installed_languages if lang.code == code),
        None
    )


def _direct_translate(text, from_code, to_code):
    from_lang = _get_language(from_code)
    to_lang = _get_language(to_code)

    if from_lang is None:
        return None, f"Kaynak dil yüklü değil: {from_code}"

    if to_lang is None:
        return None, f"Hedef dil yüklü değil: {to_code}"

    translation = from_lang.get_translation(to_lang)

    if translation is None:
        return None, f"{from_code} → {to_code} çeviri paketi kurulu değil."

    return translation.translate(text), None


def translate(text, from_code, to_code):
    if not text:
        return ""

    if from_code == to_code:
        return text

    result, error = _direct_translate(text, from_code, to_code)

    if result is not None:
        return result

    if from_code != "en" and to_code != "en":
        first_result, first_error = _direct_translate(text, from_code, "en")

        if first_result is not None:
            second_result, second_error = _direct_translate(first_result, "en", to_code)

            if second_result is not None:
                return second_result

    return error