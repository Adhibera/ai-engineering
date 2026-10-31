# AI Engineering

## Lesboek

Open `lesboek.html` in je browser. Daarin staan per les de uitleg, een schema, opdrachten en een denkvraag.

## Wat staat waar

| Map of bestand | Wat erin staat |
|---|---|
| `lesboek.html` | het lesboek |
| `src/ai_engineering/` | de code: één bestand per les, van `les01_ai_call.py` tot `les18_herstart.py` |
| `voorbeelden/` | voorbeeldmails voor les 17, 18 en 19 |
| `server/` | les 19: het programma op de klassenserver laten draaien |
| `eindopdracht/` | het dossier dat jullie invullen, en een ingevuld voorbeeld |
| `docent/` | voor de docent: handleidingen, de bron van het lesboek en achtergrond |

## Installeren

Je hebt [git](https://git-scm.com/) en [uv](https://docs.astral.sh/uv/) nodig. Controleer dat met `git --version` en `uv --version`.

1. Haal de code op: `git clone https://github.com/Adhibera/ai-engineering.git`, en ga de map in: `cd ai-engineering`. Open dezelfde map in je editor.
2. Installeer de packages: `uv sync`
3. Maak je eigen `.env`: `cp .env.example .env` (op Windows: `copy .env.example .env`) en zet de key erin die je van je docent krijgt. Die key is alleen voor jou: deel hem met niemand.
4. Test het: `uv run les1`

### Werkt het niet?

| Je ziet | Wat er mis is |
|---|---|
| `uv: command not found`, of "uv wordt niet herkend" | `uv` is niet geïnstalleerd. Zie [docs.astral.sh/uv](https://docs.astral.sh/uv/). |
| `Missing credentials` of `Error code: 401` | Er is geen `.env`, hij staat niet in de projectmap, of de key klopt niet. Is je key verlopen of ingetrokken? Vraag je docent om een nieuwe. |
| `Error code: 404` met `model_not_found` | De key mag het model uit `les01_ai_call.py` (`MODEL`) niet gebruiken. Vraag je docent welk model je moet gebruiken. |
| `Error code: 429` met `project_spend_limit_exceeded` | De limiet van je key is op. Opnieuw proberen helpt niet. Vraag je docent. |
| `Error code: 429` met "Rate limit reached" | Je stuurt te veel vragen kort na elkaar. Wacht even en probeer het opnieuw. |

## Starten

De bestanden hebben twee cijfers (`les01_ai_call.py`), zodat ze op volgorde staan. Het commando gebruikt het gewone nummer: `uv run les1`.

| Les | Starten | Code |
|---|---|---|
| 1. Je eerste AI call | `uv run les1` | `src/ai_engineering/les01_ai_call.py` |
| 2. Chat zonder geheugen | `uv run les2` | `src/ai_engineering/les02_chat.py` |
| 3. Memory | `uv run les3` | `src/ai_engineering/les03_memory.py` |
| 4. Tools | `uv run les4` | `src/ai_engineering/les04_tools.py` |
| 5. Structured output | `uv run les5` | `src/ai_engineering/les05_structured_output.py` |
| 6. Control | `uv run les6` | `src/ai_engineering/les06_control.py` |
| 7. Recovery | `uv run les7` | `src/ai_engineering/les07_recovery.py` |
| 8. Feedback | `uv run les8` | `src/ai_engineering/les08_feedback.py` |
| 9. Retrieval | `uv run les9` | `src/ai_engineering/les09_retrieval.py` |
| 10. Prompt chaining | `uv run les10` | `src/ai_engineering/les10_prompt_chaining.py` |
| 11. Routing | `uv run les11` | `src/ai_engineering/les11_routing.py` |
| 12. Parallelization | `uv run les12` | `src/ai_engineering/les12_parallelization.py` |
| 13. Agent-loop | `uv run les13` | `src/ai_engineering/les13_agent_loop.py` |
| 14. Logging | `uv run les14` | `src/ai_engineering/les14_logboek.py` |
| 15. Controleur | `uv run les15` | `src/ai_engineering/les15_controleur.py` |
| 16. Framework (optioneel) | `uv run les16` | `src/ai_engineering/les16_framework.py` |
| 17. Werken zonder gesprek | `uv run les17` | `src/ai_engineering/les17_batch.py` |
| 18. Veilig opnieuw starten | `uv run les18` | `src/ai_engineering/les18_herstart.py` |
| 19. Draaien op de server | op de server: `./server/deploy.sh` | `server/` |
| Eindopdracht | in jullie eigen privé-repo | `eindopdracht/` |

## Eindopdracht

De opdracht staat in het lesboek, in de sectie "Eindopdracht". Leerlingen vullen `eindopdracht/dossier.md` in; een ingevuld voorbeeld staat in `eindopdracht/voorbeeld-dossier-webshop.md`.

Voor de docent: `docent/eindopdracht-handleiding.md` (een goede opdracht kiezen, privacy, de pilot, een afspraaksjabloon en beoordelen) en `docent/serverdraaiboek.md` (de klassenserver). Alle stappen voor de docent op een rij, met vinkjes: `docent/stappenplan.html`.

## Het lesboek aanpassen

`lesboek.html` wordt gebouwd. Bewerk `docent/lesboek-bron/sjabloon.html` (tekst) of `docent/lesboek-bron/bouw.py` (schema's), en bouw daarna opnieuw:

```
uv run python docent/lesboek-bron/bouw.py
```
