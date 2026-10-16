"""
Les 10: prompt chaining.

Een grote taak splits je op in kleine stappen. Elke stap is een eigen
LLM-call die verder werkt met de uitkomst van de vorige stap. Tussen de
stappen controleert je code of het zin heeft om door te gaan: een gate.

Starten:  uv run les10
"""

from pydantic import BaseModel

from ai_engineering.ai_call import MODEL, client


class Controle(BaseModel):
    probleem_met_bestelling: bool
    reden: str  # waarom koos het LLM dit? handig om te debuggen


class Details(BaseModel):
    product: str
    probleem: str


def main() -> None:
    bericht = input("Klantbericht: ")

    # Stap 1: meldt de klant een probleem met een bestelling?
    response = client.responses.parse(
        model=MODEL,
        instructions="Bepaal of de klant een probleem meldt met een bestelling bij onze webshop. Geef kort de reden.",
        input=bericht,
        text_format=Controle,
    )
    controle = response.output_parsed
    print("Stap 1, probleem met bestelling:", controle.probleem_met_bestelling)
    print("Stap 1, reden:", controle.reden)

    # Gate: is er geen probleem met een bestelling, dan stopt de keten hier
    if not controle.probleem_met_bestelling:
        print("Geen probleem met een bestelling. De keten stopt.")
        return

    # Stap 2: haal de details uit het bericht
    response = client.responses.parse(
        model=MODEL,
        instructions="Haal het product en het probleem uit het bericht van de klant.",
        input=bericht,
        text_format=Details,
    )
    details = response.output_parsed
    print("Stap 2, product:", details.product)
    print("Stap 2, probleem:", details.probleem)

    # Stap 3: schrijf een antwoord met de details uit stap 2
    response = client.responses.create(
        model=MODEL,
        instructions="Je bent de klantenservice van een webshop. Schrijf een kort, vriendelijk antwoord aan de klant, in het Nederlands en zonder Markdown.",
        input=f"Product: {details.product}\nProbleem: {details.probleem}",
    )
    print("\nConcept-antwoord:\n" + response.output_text)


if __name__ == "__main__":
    main()
