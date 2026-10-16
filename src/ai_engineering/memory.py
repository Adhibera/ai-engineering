"""
Les 2: memory.

Een LLM onthoudt niets. Wil je een gesprek voeren,
dan stuur je bij elke vraag de hele geschiedenis mee.

Starten:  uv run les2   (typ "stop" om te stoppen)
"""

from ai_engineering.ai_call import vraag_ai


def main() -> None:
    geschiedenis = []

    while True:
        vraag = input("Jij: ")
        if vraag == "stop":
            break

        geschiedenis.append({"role": "user", "content": vraag})
        antwoord = vraag_ai(geschiedenis)
        geschiedenis.append({"role": "assistant", "content": antwoord})

        print("AI:", antwoord)


if __name__ == "__main__":
    main()
