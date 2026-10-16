"""
Les 1: je eerste AI call.

We sturen een vraag naar een taalmodel (LLM) van OpenAI en printen het antwoord.

Starten:  uv run ai-engineering
"""

from dotenv import load_dotenv
from openai import OpenAI

# Lees de API key uit het bestand .env
load_dotenv()

# De client praat met OpenAI. Hij vindt de key (OPENAI_API_KEY) zelf.
client = OpenAI()


def vraag_ai(vraag: str) -> str:
    """Stuur een vraag naar het LLM en geef het antwoord terug."""
    response = client.responses.create(
        model="gpt-6-astra",
        instructions="Je bent een behulpzame docent. Antwoord kort en in het Nederlands.",
        input=vraag,
    )
    return response.output_text


def main() -> None:
    vraag = input("Stel je vraag: ")
    antwoord = vraag_ai(vraag)
    print("AI:", antwoord)


if __name__ == "__main__":
    main()
