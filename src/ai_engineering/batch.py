"""
Les 17: werken zonder gesprek.

Tot nu toe wachtte elk programma op jou, met input(). Een bedrijf wil dat
het werk ook gebeurt als er niemand achter de computer zit. Dit programma
verwerkt alle mails uit de map inbox achter elkaar (een batch), zet voor
elke mail een concept in de map concepten, en stopt. Een medewerker leest
de concepten later na.

Starten:  uv run les17   (en open daarna de map concepten)
"""

from pathlib import Path

from ai_engineering.retrieval import beantwoord_vraag

# De mappen staan in de map waar je het programma start
INBOX = Path("inbox")
CONCEPTEN = Path("concepten")


def main() -> None:
    CONCEPTEN.mkdir(exist_ok=True)
    mails = sorted(INBOX.glob("*.txt"))
    print(len(mails), "mails in", INBOX.resolve())

    for bestand in mails:
        # Geen input(): de mail komt uit een bestand (utf-8, zodat ë en € ook op Windows goed gaan)
        mail = bestand.read_text(encoding="utf-8")
        antwoord = beantwoord_vraag(mail)  # les 9: retrieval

        # Geen antwoord op het scherm: het concept gaat naar een bestand, voor de medewerker
        concept = f"Mail van de klant:\n{mail}\nConcept-antwoord:\n{antwoord}\n"
        (CONCEPTEN / bestand.name).write_text(concept, encoding="utf-8")
        print("Concept klaar:", bestand.name)

    print("Klaar. Een medewerker leest de concepten na en verstuurt ze zelf.")


if __name__ == "__main__":
    main()
