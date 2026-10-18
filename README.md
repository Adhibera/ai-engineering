# AI Engineering

## Lesboek

Open `documents/lesmateriaal.html` in je browser. Daarin staan per les de uitleg, een schema, opdrachten en een denkvraag.

## Installeren

Je hebt [uv](https://docs.astral.sh/uv/) nodig. Controleer dat met `uv --version`.

1. Installeer de packages: `uv sync`
2. Maak je eigen `.env`: `cp .env.example .env` (op Windows: `copy .env.example .env`) en zet je OpenAI API key erin.
3. Test het: `uv run les1`

### Werkt het niet?

| Je ziet | Wat er mis is |
|---|---|
| `uv: command not found`, of "uv wordt niet herkend" | `uv` is niet geïnstalleerd. Zie [docs.astral.sh/uv](https://docs.astral.sh/uv/). |
| `Missing credentials` of `Error code: 401` | Er is geen `.env`, hij staat niet in de projectmap, of de key klopt niet. |
| `Error code: 404` met `model_not_found` | De key mag het model uit `ai_call.py` (`MODEL`) niet gebruiken. Kies een model waar de key wel bij kan. |

## Starten

| Les | Starten | Code |
|---|---|---|
| 1. Je eerste AI call | `uv run les1` | `src/ai_engineering/ai_call.py` |
| 2. Chat zonder geheugen | `uv run les2` | `src/ai_engineering/chat.py` |
| 3. Memory | `uv run les3` | `src/ai_engineering/memory.py` |
| 4. Tools | `uv run les4` | `src/ai_engineering/tools.py` |
| 5. Structured output | `uv run les5` | `src/ai_engineering/structured_output.py` |
| 6. Control | `uv run les6` | `src/ai_engineering/control.py` |
| 7. Recovery | `uv run les7` | `src/ai_engineering/recovery.py` |
| 8. Feedback | `uv run les8` | `src/ai_engineering/feedback.py` |
| 9. Retrieval | `uv run les9` | `src/ai_engineering/retrieval.py` |
| 10. Prompt chaining | `uv run les10` | `src/ai_engineering/prompt_chaining.py` |
| 11. Routing | `uv run les11` | `src/ai_engineering/routing.py` |
| 12. Parallelization | `uv run les12` | `src/ai_engineering/parallelization.py` |
| 13. Agent-loop | `uv run les13` | `src/ai_engineering/agent_loop.py` |
| 14. Logging | `uv run les14` | `src/ai_engineering/logboek.py` |
| 15. Controleur | `uv run les15` | `src/ai_engineering/controleur.py` |
| 16. Framework | `uv run les16` | `src/ai_engineering/framework.py` |
| 17. Werken zonder gesprek | `uv run les17` | `src/ai_engineering/batch.py` |
| 18. Veilig opnieuw starten | `uv run les18` | `src/ai_engineering/herstart.py` |

## Het lesboek aanpassen

`documents/lesmateriaal.html` wordt gebouwd. Bewerk `documents/lesboek/sjabloon.html` (tekst) of `documents/lesboek/bouw.py` (schema's), en bouw daarna opnieuw:

```
uv run python documents/lesboek/bouw.py
```
