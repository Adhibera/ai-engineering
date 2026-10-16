"""
Les 16: een framework.

Wat we in les 13 zelf bouwden, bestaat ook kant-en-klaar: een framework.
Dit is dezelfde webshop-agent, maar nu met de OpenAI Agents SDK.
Zoek voor elk stukje uit waar je eigen code van les 13 is gebleven.

Starten:  uv run les16
"""

from agents import Agent, MaxTurnsExceeded, Runner, function_tool

from ai_engineering.agent_loop import BESTELLINGEN, PAKKETTEN
from ai_engineering.ai_call import MODEL


# De beschrijving van de tool maakt de SDK zelf, uit de docstring en de type hints
@function_tool
def zoek_bestelling(bestelnummer: str) -> str:
    """Zoek een bestelling op met het bestelnummer."""
    print("(tool: zoek_bestelling", bestelnummer, ")")
    return BESTELLINGEN.get(bestelnummer, "bestelling niet gevonden")


@function_tool
def volg_pakket(trackcode: str) -> str:
    """Zoek op waar een pakket is met de trackcode."""
    print("(tool: volg_pakket", trackcode, ")")
    return PAKKETTEN.get(trackcode, "trackcode niet gevonden")


agent = Agent(
    name="Klantenservice",
    instructions="Je bent de klantenservice van een webshop. Antwoord kort en in het Nederlands, zonder Markdown. Gebruik de tools. Verzin niets.",
    model=MODEL,
    tools=[zoek_bestelling, volg_pakket],
)


def main() -> None:
    vraag = input("Stel je vraag: ")
    try:
        # Hierin zit de agent-loop van les 13. max_turns is ons MAX_STAPPEN.
        resultaat = Runner.run_sync(agent, vraag, max_turns=5)
        print("AI:", resultaat.final_output)
    except MaxTurnsExceeded:
        # Plan B, net als in les 13
        print("AI: Sorry, dat lukt me nu niet. Een medewerker neemt contact met je op.")


if __name__ == "__main__":
    main()
