"""
Les 7: recovery.

In het echt gaat er weleens iets mis: geen internet of een drukke server.
Een goed programma crasht dan niet. Het probeert het opnieuw,
en als het echt niet lukt, heeft het een plan B.

Starten:  uv run les7
"""

import random
import time

from ai_engineering.ai_call import vraag_ai

# Hoe vaak het misgaat: 0.5 is de helft van de keren. Zet op 1.0 om plan B te zien.
KANS_OP_FOUT = 0.5


def onbetrouwbare_vraag_ai(vraag: str) -> str:
    """Doet alsof de server soms niet bereikbaar is."""
    if random.random() < KANS_OP_FOUT:
        raise ConnectionError("de server is even niet bereikbaar")
    return vraag_ai(vraag)


def vraag_met_recovery(vraag: str) -> str:
    for poging in range(1, 4):  # maximaal 3 pogingen
        try:
            return onbetrouwbare_vraag_ai(vraag)
        except ConnectionError as fout:
            print("Poging", poging, "mislukt:", fout)
            time.sleep(poging)  # wacht steeds iets langer

    # Plan B: alle pogingen zijn mislukt
    return "Sorry, het lukt nu niet. Probeer het later nog eens."


def main() -> None:
    vraag = input("Stel je vraag: ")
    print("AI:", vraag_met_recovery(vraag))


if __name__ == "__main__":
    main()
