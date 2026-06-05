from langdetect import detect
from deep_translator import GoogleTranslator

class Traductor():

    def detectLang(message: str):
        return detect(message)

    def translate(source: str,target: str, message: str):
        return source,GoogleTranslator(source=source, target=target).translate(message)