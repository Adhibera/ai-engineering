"""
Les 5: structured output.

Een LLM geeft normaal gewone tekst terug. Met een Pydantic-model
vraag je om data in een vaste vorm: velden met een naam en een type.

Starten:  uv run les5
"""

from typing import Literal

from pydantic import BaseModel

from ai_engineering.ai_call import MODEL, client


# Welke velden we terug willen, en van welk type
class Taak(BaseModel):
    omschrijving: str
    klaar: bool
    prioriteit: Literal["laag", "middel", "hoog", "nvt"]  # alleen deze vier mogen


def main() -> None:
    zin = input("Beschrijf je taak: ")

    response = client.responses.parse(
        model=MODEL,
        instructions="Haal de taak uit de tekst van de gebruiker. Is de taak al klaar, kies dan nvt als prioriteit.",
        input=zin,
        text_format=Taak,
    )
    taak = response.output_parsed

    print("Omschrijving:", taak.omschrijving)
    print("Klaar:", taak.klaar)
    print("Prioriteit:", taak.prioriteit)


if __name__ == "__main__":
    main()
