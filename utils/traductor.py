from langdetect import detect
from deep_translator import GoogleTranslator

class Traductor():

    def detectLang(message: str):
        return detect(message)

    def translate(message: str):
        source = detect(message)
        return source,GoogleTranslator(source, "es").translate(message)