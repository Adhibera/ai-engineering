"""
Les 11: routing.

Het LLM bepaalt wat voor bericht het is, en onze code kiest de route.
Elke route is een eigen workflow die je al kent: een vraag gaat naar de
kennisbank (les 9), een klacht naar een concept-mail die een mens
goedkeurt (les 8).

Starten:  uv run les11
"""

from ai_engineering.ai_call import MODEL, client
from ai_engineering.control import Beoordeling
from ai_engineering.feedback import schrijf_mail
from ai_engineering.retrieval import beantwoord_vraag


def main() -> None:
    bericht = input("Klantbericht: ")

    # Stap 1: het LLM bepaalt de soort, net als in les 6
    response = client.responses.parse(
        model=MODEL,
        instructions="Bepaal of het bericht van de klant een klacht, compliment of vraag is. Geef kort de reden.",
        input=bericht,
        text_format=Beoordeling,
    )
    beoordeling = response.output_parsed
    print("Soort:", beoordeling.soort)
    print("Reden:", beoordeling.reden)

    # Stap 2: onze code kiest de route, en elke route is een eigen workflow
    if beoordeling.soort == "vraag":
        print("AI:", beantwoord_vraag(bericht))  # les 9: retrieval
    elif beoordeling.soort == "klacht":
        schrijf_mail(bericht)  # les 8: feedback
    elif beoordeling.soort == "compliment":
        print("Bedankt voor je compliment!")  # hier is geen LLM nodig


if __name__ == "__main__":
    main()
