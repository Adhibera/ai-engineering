"""
Les 6: control.

Het LLM beslist niet wat er gebeurt. Het LLM bepaalt alleen wat voor
bericht het is. Daarna beslist onze eigen code met if/elif wat er gebeurt.

Starten:  uv run les6
"""

from typing import Literal

from pydantic import BaseModel

from ai_engineering.ai_call import MODEL, client, vraag_ai


class Beoordeling(BaseModel):
    soort: Literal["klacht", "compliment", "vraag"]
    reden: str  # waarom koos het LLM dit? handig om te debuggen


def main() -> None:
    bericht = input("Klantbericht: ")

    # Stap 1: het LLM bepaalt de soort
    response = client.responses.parse(
        model=MODEL,
        instructions="Bepaal of het bericht van de klant een klacht, compliment of vraag is. Geef kort de reden.",
        input=bericht,
        text_format=Beoordeling,
    )
    beoordeling = response.output_parsed

    print("Soort:", beoordeling.soort)
    print("Reden:", beoordeling.reden)

    # Stap 2: onze eigen code beslist wat er gebeurt
    if beoordeling.soort == "klacht":
        print("Je bericht is doorgestuurd naar de klachtenafdeling.")
    elif beoordeling.soort == "compliment":
        print("Bedankt voor je compliment!")
    elif beoordeling.soort == "vraag":
        print("AI:", vraag_ai(bericht))


if __name__ == "__main__":
    main()
