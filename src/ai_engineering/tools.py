"""
Les 4: tools.

Een LLM kan zelf niets opzoeken. Wel kan het vragen om een functie
(tool) aan te roepen. Jouw code voert die functie uit en stuurt het
resultaat terug naar het LLM.

Starten:  uv run les4
"""

import json

import requests

from ai_engineering.ai_call import INSTRUCTIES, MODEL, client


def huidige_temperatuur(latitude: float, longitude: float) -> float:
    """Haal de huidige temperatuur op bij Open-Meteo (gratis, geen key nodig)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m"}
    reactie = requests.get(url, params=params, timeout=10)  # wacht hoogstens 10 seconden
    reactie.raise_for_status()  # bij een fout van Open-Meteo stopt het hier, met een duidelijke melding
    return reactie.json()["current"]["temperature_2m"]


# De beschrijving van de tool, zodat het LLM weet wat het kan vragen
tools = [
    {
        "type": "function",
        "name": "huidige_temperatuur",
        "description": "Geef de huidige temperatuur in graden Celsius op een locatie.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False,
        },
        "strict": True,  # de argumenten van het LLM passen dan precies in deze parameters
    }
]


def main() -> None:
    vraag = input("Stel je vraag: ")
    gesprek = [{"role": "user", "content": vraag}]

    # Stap 1: het LLM kiest zelf of het de tool nodig heeft
    response = client.responses.create(
        model=MODEL, instructions=INSTRUCTIES, input=gesprek, tools=tools
    )
    # Bewaar alles wat het LLM terugstuurde, ook de tool-aanvraag
    gesprek += response.output

    # Stap 2: jouw code voert de tool uit
    tool_gebruikt = False
    for item in response.output:
        if item.type == "function_call":
            tool_gebruikt = True
            args = json.loads(item.arguments)
            print("(tool:", item.name, args, ")")
            resultaat = huidige_temperatuur(**args)
            gesprek.append({
                "type": "function_call_output",
                "call_id": item.call_id,  # koppelt het resultaat aan precies deze aanvraag
                "output": str(resultaat),
            })

    # Geen tool nodig? Dan is het eerste antwoord al goed, en is stap 3 niet nodig.
    if not tool_gebruikt:
        print("AI:", response.output_text)
        return

    # Stap 3: het LLM maakt een antwoord met het resultaat.
    # Met tool_choice="none" mag het geen nieuwe tool vragen: deze les doet één tool-ronde.
    response = client.responses.create(
        model=MODEL, instructions=INSTRUCTIES, input=gesprek, tools=tools, tool_choice="none"
    )
    print("AI:", response.output_text)


if __name__ == "__main__":
    main()
