"""
Les 18: veilig opnieuw uitvoeren.

Les 17 deed bij elke start alles opnieuw, en overschreef concepten die een
medewerker misschien al had aangepast. Nu gaat een mail pas naar de map
verwerkt als zijn concept klaarstaat. Crasht het programma, dan start je
het gewoon opnieuw: het doet alleen wat nog in de inbox staat.

Starten:  uv run les18
"""

from pathlib import Path

from ai_engineering.retrieval import beantwoord_vraag

# De mappen staan in de map waar je het programma start
INBOX = Path("inbox")
CONCEPTEN = Path("concepten")
VERWERKT = Path("verwerkt")


def verwerk(bestand: Path) -> None:
    """Maak een concept voor één mail, en zet de mail daarna in de map verwerkt."""
    concept_bestand = CONCEPTEN / bestand.name

    # Staat er al een concept? Niet overschrijven: misschien heeft de medewerker het al aangepast
    if not concept_bestand.exists():
        mail = bestand.read_text(encoding="utf-8")
        antwoord = beantwoord_vraag(mail)  # les 9: retrieval
        concept = f"Mail van de klant:\n{mail}\nConcept-antwoord:\n{antwoord}\n"
        concept_bestand.write_text(concept, encoding="utf-8")

    # Pas als het concept er staat, gaat de mail uit de inbox
    bestand.replace(VERWERKT / bestand.name)


def main() -> None:
    CONCEPTEN.mkdir(exist_ok=True)
    VERWERKT.mkdir(exist_ok=True)
    mails = sorted(INBOX.glob("*.txt"))
    print(len(mails), "mails in", INBOX.resolve())

    for bestand in mails:
        verwerk(bestand)
        print("Verwerkt:", bestand.name)

    print("Klaar. Een medewerker leest de concepten na en verstuurt ze zelf.")


if __name__ == "__main__":
    main()
