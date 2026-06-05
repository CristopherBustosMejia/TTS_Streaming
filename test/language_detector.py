from deep_translator import GoogleTranslator
from langdetect import detect

def main():

    message = input()
    language = detect(message)
    print(f"Lenguaje detectado: {language}")
    traduction = GoogleTranslator(source=language,target="es").translate(message)

    print(f"Mensaje original: {message}")
    print(f"Mensaje traducido: {traduction}")

if __name__ == "__main__":
    main()