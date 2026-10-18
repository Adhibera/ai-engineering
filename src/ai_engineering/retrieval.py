"""
Les 9: retrieval.

Een LLM kent jouw bedrijf niet, zoals het retourbeleid van je webshop.
Daarom haalt je code die informatie eerst op uit een bron die jij beheert
(hier een kennisbank) en stuurt die mee met de vraag.

Starten:  uv run les9
"""

from pathlib import Path

from ai_engineering.ai_call import MODEL, client

# De kennisbank staat in een bestand naast deze code
KENNISBANK = Path(__file__).parent / "kennisbank.json"


def zoek_in_kennisbank(vraag: str) -> str:
    """Haal informatie op uit de kennisbank. We zoeken nog niet echt: we geven alles terug."""
    return KENNISBANK.read_text()


def beantwoord_vraag(vraag: str) -> str:
    """Beantwoord een vraag van een klant met informatie uit de kennisbank."""
    # Stap 1: onze code haalt de informatie op
    informatie = zoek_in_kennisbank(vraag)

    # Stap 2: het LLM antwoordt met die informatie
    response = client.responses.create(
        model=MODEL,
        instructions="Je bent de klantenservice van een webshop. Antwoord kort en in het Nederlands, zonder Markdown. Gebruik alleen de informatie uit de kennisbank. Staat het antwoord er niet in, zeg dat dan.",
        input=f"Kennisbank:\n{informatie}\n\nVraag van de klant: {vraag}",
    )
    return response.output_text


def main() -> None:
    vraag = input("Stel je vraag: ")
    print("AI:", beantwoord_vraag(vraag))


if __name__ == "__main__":
    main()
