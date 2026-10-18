"""
Les 14: logging.

Een agent kiest zelf zijn stappen. Achteraf wil je kunnen nalezen wat
hij deed, maar de klant hoeft dat niet te zien. Daarom schrijft de agent
zijn stappen in een logboek: het bestand agent.log.

Starten:  uv run les14   (en open daarna agent.log)
"""

import json
import logging

from ai_engineering.agent_loop import tools, voer_tool_uit
from ai_engineering.ai_call import MODEL, client

# Alles vanaf INFO gaat naar agent.log. Zet op logging.WARNING om alleen problemen te zien.
logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Zet op 2 om een WARNING in het logboek te zien
MAX_STAPPEN = 5


def agent(vraag: str) -> str:
    logging.info(f"Vraag: {vraag}")
    gesprek = [{"role": "user", "content": vraag}]

    for stap in range(1, MAX_STAPPEN + 1):
        response = client.responses.create(
            model=MODEL,
            instructions="Je bent de klantenservice van een webshop. Antwoord kort en in het Nederlands, zonder Markdown. Gebruik de tools. Verzin niets.",
            input=gesprek,
            tools=tools,
        )
        gesprek += response.output

        tool_gebruikt = False
        for item in response.output:
            if item.type == "function_call":
                tool_gebruikt = True
                args = json.loads(item.arguments)
                resultaat = voer_tool_uit(item.name, args)
                # Niet meer print: de stap gaat naar het logboek
                logging.info(f"Stap {stap}: tool {item.name} {args} gaf: {resultaat}")
                gesprek.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": resultaat,
                })

        if not tool_gebruikt:
            logging.info(f"Stap {stap}: klaar. Antwoord: {response.output_text}")
            return response.output_text

    logging.warning(f"Na {MAX_STAPPEN} stappen nog niet klaar, plan B")
    return "Sorry, dat lukt me nu niet. Probeer het later nog eens."


def main() -> None:
    vraag = input("Stel je vraag: ")
    print("AI:", agent(vraag))


if __name__ == "__main__":
    main()
