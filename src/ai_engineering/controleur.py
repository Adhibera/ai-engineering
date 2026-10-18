"""
Les 15: de controleur.

In les 8 keurde een mens het concept. Nu doet een tweede LLM dat eerst:
de controleur. Keurt hij het af, dan gaat zijn feedback terug naar de
schrijver, net als de feedback van de mens in les 8. Daarna beslist de mens.

Starten:  uv run les15
"""

from pydantic import BaseModel

from ai_engineering.ai_call import MODEL, client, vraag_ai

# Hoe vaak de schrijver het mag proberen
MAX_RONDES = 3

# De regels waar de controleur op let
REGELS = """Je controleert een mail aan een klant. Keur de mail alleen goed als:
- er geen invulvelden in staan, zoals [naam] of [Bedrijfsnaam]
- de mail geen geld terug, korting of cadeau belooft
- de mail kort en vriendelijk is
Keur je de mail af, zeg dan kort wat er beter moet."""


class Controle(BaseModel):
    goedgekeurd: bool
    feedback: str


def controleer(mail: str) -> Controle:
    """De controleur: een tweede LLM-call die het concept beoordeelt."""
    response = client.responses.parse(
        model=MODEL,
        instructions=REGELS,
        input=mail,
        text_format=Controle,
    )
    return response.output_parsed


def schrijf_mail(klacht: str) -> None:
    """De schrijver maakt een concept, de controleur keurt, en een mens beslist."""
    opdracht = f"Schrijf een korte, vriendelijke mail aan een klant met deze klacht: {klacht}"
    gesprek = [{"role": "user", "content": opdracht}]

    for ronde in range(1, MAX_RONDES + 1):
        concept = vraag_ai(gesprek)
        print(f"\nConcept {ronde}:\n{concept}\n")

        # De controleur beoordeelt het concept
        controle = controleer(concept)
        print("Controleur:", controle.goedgekeurd, "-", controle.feedback)
        if controle.goedgekeurd:
            break

        # Afgekeurd: de feedback gaat terug naar de schrijver, net als in les 8
        gesprek.append({"role": "assistant", "content": concept})
        gesprek.append({"role": "user", "content": controle.feedback})

    # Ook het laatste concept kan afgekeurd zijn. Dat moet de mens weten.
    if not controle.goedgekeurd:
        print(f"\nLet op: ook na {MAX_RONDES} rondes keurt de controleur het af.")

    # De mens heeft het laatste woord
    akkoord = input("\nVersturen? (j/n): ")
    if akkoord == "j":
        print("Goedgekeurd. (Simulatie: er is geen echte mail verstuurd.)")
    else:
        print("Niet goedgekeurd. Er gaat geen mail naar de klant.")


def main() -> None:
    klacht = input("Klacht van de klant: ")
    schrijf_mail(klacht)


if __name__ == "__main__":
    main()
