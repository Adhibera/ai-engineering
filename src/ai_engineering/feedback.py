"""
Les 8: feedback (human-in-the-loop).

Bij belangrijke acties, zoals een mail naar een klant, beslist niet
het LLM maar een mens. Het LLM schrijft een concept. Is het niet goed,
dan geeft de mens feedback en schrijft het LLM een nieuwe versie.

Starten:  uv run les8
"""

from ai_engineering.ai_call import vraag_ai


def schrijf_mail(klacht: str) -> None:
    """Het LLM schrijft een concept-mail, en een mens beslist of die weg mag."""
    opdracht = f"Schrijf een korte, vriendelijke mail aan een klant met deze klacht: {klacht}"
    gesprek = [{"role": "user", "content": opdracht}]

    while True:
        concept = vraag_ai(gesprek)
        print("\nConcept:\n" + concept + "\n")

        # De mens beslist
        akkoord = input("Versturen? (j/n): ")
        if akkoord == "j":
            print("De mail is verstuurd.")
            break

        # Niet akkoord: de feedback gaat terug naar het LLM
        feedback = input("Wat moet er anders? ")
        gesprek.append({"role": "assistant", "content": concept})
        gesprek.append({"role": "user", "content": feedback})


def main() -> None:
    klacht = input("Klacht van de klant: ")
    schrijf_mail(klacht)


if __name__ == "__main__":
    main()
