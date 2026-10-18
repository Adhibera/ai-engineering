"""
Les 13: de agent-loop.

In les 4 mocht het LLM één keer een tool kiezen. Een agent mag dat
steeds opnieuw: hij kiest een tool, bekijkt het resultaat en kiest dan
de volgende stap. Pas als hij geen tool meer nodig heeft, is hij klaar.

Starten:  uv run les13
"""

import json

from ai_engineering.ai_call import MODEL, client

# Maximaal aantal stappen, zodat de agent niet eindeloos doorgaat. Zet op 2 om plan B te zien.
MAX_STAPPEN = 5

# Nepdata. In het echt komt dit uit de database van de webshop en van de bezorger.
BESTELLINGEN = {
    "1001": "koptelefoon, onderweg, trackcode NL-7731",
    "1002": "waterkoker, bezorgd op 2 oktober",
}
PAKKETTEN = {"NL-7731": "ligt in het sorteercentrum in Utrecht, wordt morgen bezorgd"}


def zoek_bestelling(bestelnummer: str) -> str:
    return BESTELLINGEN.get(bestelnummer, "bestelling niet gevonden")


def volg_pakket(trackcode: str) -> str:
    return PAKKETTEN.get(trackcode, "trackcode niet gevonden")


# De beschrijving van de tools, zodat het LLM weet wat het kan vragen
tools = [
    {
        "type": "function",
        "name": "zoek_bestelling",
        "description": "Zoek een bestelling op met het bestelnummer.",
        "parameters": {
            "type": "object",
            "properties": {"bestelnummer": {"type": "string"}},
            "required": ["bestelnummer"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "volg_pakket",
        "description": "Zoek op waar een pakket is met de trackcode.",
        "parameters": {
            "type": "object",
            "properties": {"trackcode": {"type": "string"}},
            "required": ["trackcode"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def voer_tool_uit(naam: str, args: dict) -> str:
    """Onze code voert de tool uit die het LLM koos."""
    if naam == "zoek_bestelling":
        return zoek_bestelling(**args)
    elif naam == "volg_pakket":
        return volg_pakket(**args)
    else:
        # Staat een tool wel in tools, maar niet hier? Dan krijgt het LLM deze melding.
        return f"onbekende tool: {naam}"


def agent(vraag: str) -> str:
    gesprek = [{"role": "user", "content": vraag}]

    for stap in range(1, MAX_STAPPEN + 1):
        # Het LLM kiest de volgende stap: een tool, of het eindantwoord
        response = client.responses.create(
            model=MODEL,
            instructions="Je bent de klantenservice van een webshop. Antwoord kort en in het Nederlands, zonder Markdown. Gebruik de tools. Verzin niets.",
            input=gesprek,
            tools=tools,
        )
        # Bewaar alles wat het LLM terugstuurde, ook de tool-aanvragen
        gesprek += response.output

        # Onze code voert de gekozen tools uit en geeft het resultaat terug.
        # Twee tools in één ronde? Dan voert de for-lus ze na elkaar uit.
        tool_gebruikt = False
        for item in response.output:
            if item.type == "function_call":
                tool_gebruikt = True
                args = json.loads(item.arguments)
                print("(stap", stap, "tool:", item.name, args, ")")
                gesprek.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": voer_tool_uit(item.name, args),
                })

        # Geen tool nodig? Dan is de agent klaar.
        if not tool_gebruikt:
            return response.output_text

    # Plan B: de agent is na MAX_STAPPEN nog niet klaar
    return "Sorry, dat lukt me nu niet. Probeer het later nog eens."


def main() -> None:
    vraag = input("Stel je vraag: ")
    print("AI:", agent(vraag))


if __name__ == "__main__":
    main()
