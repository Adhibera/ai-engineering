"""
Les 1.1: chat zonder geheugen.

Met een while-lus kun je steeds een nieuwe vraag stellen.
Maar let op: onthoudt de AI wat je eerder zei?

Starten:  uv run les1.1   (typ "stop" om te stoppen)
"""

from ai_engineering.ai_call import vraag_ai


def main() -> None:
    while True:
        vraag = input("Jij: ")
        if vraag == "stop":
            break

        antwoord = vraag_ai(vraag)
        print("AI:", antwoord)


if __name__ == "__main__":
    main()
