"""
Les 9: retrieval.

Een LLM weet niets over jouw bedrijf, zoals het retourbeleid van je webshop.
Daarom haalt je code die informatie eerst op uit een bron (hier een
kennisbank) en stuurt die mee met de vraag.

Starten:  uv run les9
"""

from pathlib import Path

from ai_engineering.ai_call import MODEL, client

# De kennisbank staat in een bestand naast deze code
KENNISBANK = Path(__file__).parent / "kennisbank.json"


def zoek_in_kennisbank(vraag: str) -> str:
    """Haal informatie op uit de kennisbank. We zoeken nog niet echt: we geven alles terug."""
    return KENNISBANK.read_text()


def main() -> None:
    vraag = input("Stel je vraag: ")

    # Stap 1: onze code haalt de informatie op
    informatie = zoek_in_kennisbank(vraag)

    # Stap 2: het LLM antwoordt met die informatie
    response = client.responses.create(
        model=MODEL,
        instructions="Je bent de klantenservice van een webshop. Antwoord kort en in het Nederlands, zonder Markdown. Gebruik alleen de informatie uit de kennisbank. Staat het antwoord er niet in, zeg dat dan.",
        input=f"Kennisbank:\n{informatie}\n\nVraag van de klant: {vraag}",
    )
    print("AI:", response.output_text)


if __name__ == "__main__":
    main()
