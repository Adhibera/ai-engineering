"""
Bouwt het lesboek documents/lesmateriaal.html uit sjabloon.html.

Het script tekent de schema's (op de plekken met {{schema:naam}}) en kleurt
de code- en terminalblokken. Pas de tekst aan in sjabloon.html en een schema
hieronder, en draai daarna dit script. Bewerk lesmateriaal.html niet met de
hand, want het script overschrijft dat bestand.

Starten:  uv run python documents/lesboek/bouw.py
"""

import html
import re
from pathlib import Path

HIER = Path(__file__).parent
SJABLOON = HIER / "sjabloon.html"
DOEL = HIER.parent / "lesmateriaal.html"

RX = {"llm": 12, "code": 4, "tool": 4, "mens": 24, "io": None}


class Schema:
    def __init__(self, naam, w, h, label):
        self.naam, self.w, self.h, self.label = naam, w, h, label
        self.vakken = {}
        self.lijnen = []
        self.dozen = []
        self.teksten = []

    def vak(self, naam, soort, x, y, w, h, regels, mono=False, stippel=False, links=False):
        self.vakken[naam] = (x, y, w, h)
        rx = RX[soort] if RX[soort] is not None else h / 2
        klasse = f"v-{soort}" + (" stippel" if stippel else "")
        d = [f'<rect class="{klasse}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>']
        if links:
            # Titel plus regels, links uitgelijnd (een lijst of een bestand)
            d.append(f'<text class="hoofd" x="{x + 12}" y="{y + 22}">{esc(regels[0])}</text>')
            for i, regel in enumerate(regels[1:], start=1):
                d.append(f'<text class="rij" x="{x + 12}" y="{y + 22 + 20 * i}">{esc(regel)}</text>')
        elif len(regels) == 1:
            k = "rij" if mono else "hoofd"
            if stippel:
                k += " zacht"
            d.append(f'<text class="{k}" x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle">{esc(regels[0])}</text>')
        else:
            d.append(f'<text class="hoofd" x="{x + w / 2}" y="{y + h / 2 - 3}" text-anchor="middle">{esc(regels[0])}</text>')
            d.append(f'<text class="sub" x="{x + w / 2}" y="{y + h / 2 + 15}" text-anchor="middle">{esc(regels[1])}</text>')
        self.dozen.append("\n".join(d))

    def p(self, naam, kant, t=0.5):
        x, y, w, h = self.vakken[naam]
        return {
            "l": (x, y + h * t), "r": (x + w, y + h * t),
            "t": (x + w * t, y), "b": (x + w * t, y + h),
        }[kant]

    def pijl(self, *punten, kop=True, stippel=False):
        pts = " ".join(f"{x},{y}" for x, y in punten)
        klasse = "pijl" + (" stippel" if stippel else "")
        einde = f' marker-end="url(#kop-{self.naam})"' if kop else ""
        self.lijnen.append(f'<polyline class="{klasse}" points="{pts}"{einde}/>')

    def tekst(self, x, y, s, anker="middle", klasse="lbl"):
        self.teksten.append(f'<text class="{klasse}" x="{x}" y="{y}" text-anchor="{anker}">{esc(s)}</text>')

    def svg(self):
        defs = (
            f'<defs><marker id="kop-{self.naam}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path class="kop" d="M0,0 L10,5 L0,10 z"/></marker></defs>'
        )
        delen = [defs, *self.lijnen, *self.dozen, *self.teksten]
        return (
            f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.label)}" '
            f'style="--min:{round(self.w * 0.78)}px">\n' + "\n".join(delen) + "\n</svg>"
        )


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- de schema's

def augmented():
    s = Schema("aug", 680, 232, "Een LLM met drie hulpmiddelen: geheugen, tools en een kennisbank.")
    s.vak("in", "io", 20, 50, 100, 40, ["Vraag"])
    s.vak("llm", "llm", 270, 44, 140, 52, ["LLM", "denkt in taal"])
    s.vak("uit", "io", 560, 50, 100, 40, ["Antwoord"])
    s.vak("geh", "tool", 105, 165, 150, 52, ["Geheugen", "les 3"])
    s.vak("tools", "tool", 265, 165, 150, 52, ["Tools", "les 4"])
    s.vak("kb", "tool", 425, 165, 150, 52, ["Kennisbank", "les 9"])
    s.pijl(s.p("in", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "r"), s.p("uit", "l"))
    for naam in ("geh", "tools", "kb"):
        s.pijl(s.p("llm", "b"), s.p(naam, "t"), kop=False, stippel=True)
    return s


def les1():
    s = Schema("les1", 680, 186, "Je code stuurt instructies en je vraag naar het LLM en print het antwoord.")
    s.vak("in", "io", 20, 40, 110, 40, ["Jij typt"])
    s.vak("code", "code", 170, 34, 150, 52, ["vraag_ai()", "jouw code"])
    s.vak("llm", "llm", 470, 34, 160, 52, ["LLM", "bij OpenAI"])
    s.vak("uit", "io", 170, 132, 150, 40, ["AI: antwoord"])
    s.pijl(s.p("in", "r"), s.p("code", "l"))
    s.pijl((320, 48), (470, 48))
    s.tekst(395, 40, "instructies + vraag")
    s.pijl((470, 72), (320, 72))
    s.tekst(395, 90, "antwoord (tekst)")
    s.pijl(s.p("code", "b"), s.p("uit", "t"))
    s.tekst(253, 114, "print", anker="start")
    return s


def les2():
    s = Schema("les2", 680, 168, "Een while-lus: elke vraag gaat los naar het LLM, zonder de vorige vragen.")
    s.vak("in", "io", 20, 30, 120, 40, ["Jij typt"])
    s.vak("code", "code", 190, 24, 160, 52, ["vraag_ai(vraag)", "in een while-lus"])
    s.vak("llm", "llm", 420, 24, 170, 52, ["LLM", "ziet alleen deze vraag"])
    s.vak("uit", "io", 420, 110, 170, 40, ["AI: antwoord"])
    s.pijl(s.p("in", "r"), s.p("code", "l"))
    s.pijl(s.p("code", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "b"), s.p("uit", "t"))
    s.pijl(s.p("uit", "l"), (80, 130), s.p("in", "b"))
    s.tekst(250, 122, "volgende vraag")
    return s


def les3():
    s = Schema("les3", 680, 226, "Je code zet elke vraag en elk antwoord in een lijst en stuurt de hele lijst mee.")
    s.vak("in", "io", 20, 40, 110, 40, ["Jij typt"])
    s.vak("code", "code", 170, 34, 140, 52, ["append()", "vraag in de lijst"])
    s.vak("lijst", "tool", 360, 12, 300, 96, ["geschiedenis", 'user: "Ik heet Sam."', 'assistant: "Hoi Sam!"', 'user: "Hoe heet ik?"'], links=True)
    s.vak("llm", "llm", 430, 160, 160, 52, ["LLM", "leest de hele lijst"])
    s.vak("uit", "io", 160, 166, 170, 40, ["AI: Je heet Sam."])
    s.pijl(s.p("in", "r"), s.p("code", "l"))
    s.pijl((310, 60), (360, 60))
    s.pijl((470, 108), (470, 160))
    s.tekst(462, 139, "hele gesprek", anker="end")
    s.pijl((550, 160), (550, 108))
    s.tekst(558, 139, "antwoord erbij", anker="start")
    s.pijl(s.p("llm", "l"), s.p("uit", "r"))
    s.tekst(380, 178, "antwoord")
    return s


def les4():
    s = Schema("les4", 700, 216, "Het LLM vraagt om een tool, jouw code voert hem uit en stuurt het resultaat terug.")
    s.vak("in", "io", 10, 34, 90, 40, ["Vraag"])
    s.vak("llm1", "llm", 135, 28, 150, 52, ["LLM · stap 1", "kiest een tool"])
    s.vak("code", "code", 375, 28, 150, 52, ["Jouw code", "stap 2: voert uit"])
    s.vak("tool", "tool", 590, 28, 100, 52, ["Open-Meteo", "weer van nu"])
    s.vak("llm3", "llm", 375, 150, 150, 52, ["LLM · stap 3", "maakt het antwoord"])
    s.vak("uit", "io", 135, 156, 150, 40, ["Antwoord"])
    s.pijl(s.p("in", "r"), s.p("llm1", "l"))
    s.pijl(s.p("llm1", "r"), s.p("code", "l"))
    s.tekst(330, 46, "vraagt tool")
    s.pijl((525, 44), (590, 44))
    s.tekst(557, 36, "lat, lon")
    s.pijl((590, 66), (525, 66))
    s.tekst(557, 84, "13,5 °C")
    s.pijl(s.p("code", "b"), s.p("llm3", "t"))
    s.tekst(458, 119, "resultaat", anker="start")
    s.pijl(s.p("llm3", "l"), s.p("uit", "r"))
    return s


def les5():
    s = Schema("les5", 720, 214, "Het LLM vult een vast formulier in. Pydantic controleert de types en geeft een Python-object.")
    s.vak("model", "tool", 150, 8, 280, 96, ["class Taak", "omschrijving: str", "klaar: bool", "prioriteit: laag|middel|hoog|nvt"], links=True)
    s.vak("in", "io", 10, 156, 150, 40, ["Zin over een taak"])
    s.vak("llm", "llm", 215, 150, 150, 52, ["LLM", "vult het formulier in"])
    s.vak("pyd", "code", 430, 150, 140, 52, ["Pydantic", "checkt de types"])
    s.vak("uit", "io", 595, 156, 120, 40, ["Python-object"])
    s.pijl(s.p("model", "b", 0.5), s.p("llm", "t"))
    s.tekst(298, 131, "het formulier", anker="start")
    s.pijl(s.p("in", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "r"), s.p("pyd", "l"))
    s.tekst(397, 168, "JSON")
    s.pijl(s.p("pyd", "r"), s.p("uit", "l"))
    return s


def les6():
    s = Schema("les6", 710, 250, "Het LLM bepaalt de soort. Jouw code kiest met if/elif welke actie er volgt.")
    s.vak("in", "io", 10, 110, 90, 40, ["Bericht"])
    s.vak("llm", "llm", 130, 104, 140, 52, ["LLM", "bepaalt de soort"])
    s.vak("code", "code", 330, 104, 120, 52, ["if / elif", "jouw code"])
    s.vak("a", "code", 510, 24, 190, 52, ["klacht", "doorsturen naar afdeling"])
    s.vak("b", "code", 510, 104, 190, 52, ["compliment", "vaste tekst: Bedankt!"])
    s.vak("c", "llm", 510, 184, 190, 52, ["vraag", "antwoord met vraag_ai()"])
    s.pijl(s.p("in", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "r"), s.p("code", "l"))
    s.tekst(300, 122, "soort")
    s.pijl((450, 130), (480, 130), (480, 50), (510, 50))
    s.pijl((450, 130), (510, 130))
    s.pijl((450, 130), (480, 130), (480, 210), (510, 210))
    return s


def les7():
    s = Schema("les7", 720, 192, "Drie pogingen met steeds langer wachten. Lukt geen enkele poging, dan volgt plan B.")
    s.vak("in", "io", 10, 36, 70, 40, ["Vraag"])
    for i, x in enumerate((110, 280, 450), start=1):
        s.vak(f"p{i}", "llm", x, 30, 100, 52, [f"Poging {i}", "LLM-call"])
    s.vak("b", "code", 625, 30, 90, 52, ["Plan B", "sorry-tekst"])
    s.vak("uit", "io", 110, 140, 440, 36, ["Antwoord"])
    s.pijl(s.p("in", "r"), s.p("p1", "l"))
    for a, b, sec in (("p1", "p2", 1), ("p2", "p3", 2), ("p3", "b", 3)):
        x1, y = s.p(a, "r")
        x2, _ = s.p(b, "l")
        s.pijl((x1, y), (x2, y))
        s.tekst((x1 + x2) / 2, y - 8, "fout")
        s.tekst((x1 + x2) / 2, y + 18, f"wacht {sec} s")
    for i in (1, 2, 3):
        x, y = s.p(f"p{i}", "b")
        s.pijl((x, y), (x, 140), stippel=True)
        s.tekst(x + 6, 116, "gelukt", anker="start")
    return s


def les8():
    s = Schema("les8", 700, 176, "Het LLM schrijft een concept. Een mens keurt het goed, of geeft feedback voor een nieuwe versie.")
    s.vak("in", "io", 10, 40, 100, 40, ["Klacht"])
    s.vak("llm", "llm", 150, 34, 150, 52, ["LLM", "schrijft een concept"])
    s.vak("mens", "mens", 380, 34, 150, 52, ["Mens", "Versturen? (j/n)"])
    s.vak("uit", "io", 580, 40, 110, 40, ["Verstuurd"])
    s.pijl(s.p("in", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "r"), s.p("mens", "l"))
    s.tekst(340, 52, "concept")
    s.pijl(s.p("mens", "r"), s.p("uit", "l"))
    s.tekst(555, 52, "j")
    s.pijl(s.p("mens", "b"), (455, 140), (225, 140), s.p("llm", "b"))
    s.tekst(340, 132, "n + feedback")
    s.tekst(340, 160, "komt in het gesprek (les 3)", klasse="lbl zacht")
    return s


def les9():
    s = Schema("les9", 700, 208, "Jouw code haalt eerst informatie uit de kennisbank en stuurt die samen met de vraag naar het LLM.")
    s.vak("in", "io", 10, 40, 100, 40, ["Vraag"])
    s.vak("code", "code", 150, 34, 160, 52, ["Stap 1: zoeken", "jouw code"])
    s.vak("kb", "tool", 150, 140, 160, 52, ["kennisbank.json", "3 vragen + antwoorden"])
    s.vak("llm", "llm", 400, 34, 160, 52, ["LLM · stap 2", "antwoordt met de info"])
    s.vak("uit", "io", 595, 40, 100, 40, ["Antwoord"])
    s.pijl(s.p("in", "r"), s.p("code", "l"))
    s.pijl((200, 86), (200, 140))
    s.tekst(192, 118, "zoek", anker="end")
    s.pijl((260, 140), (260, 86))
    s.tekst(268, 118, "info", anker="start")
    s.pijl(s.p("code", "r"), s.p("llm", "l"))
    s.tekst(355, 52, "info + vraag")
    s.pijl(s.p("llm", "r"), s.p("uit", "l"))
    return s


def les10():
    s = Schema("les10", 770, 180, "Drie LLM-calls na elkaar. Een gate na stap 1 stopt de keten als er geen probleem is.")
    s.vak("in", "io", 10, 40, 70, 40, ["Bericht"])
    s.vak("s1", "llm", 110, 34, 130, 52, ["Stap 1", "probleem?"])
    s.vak("gate", "code", 270, 34, 70, 52, ["Gate", "if"])
    s.vak("s2", "llm", 370, 34, 130, 52, ["Stap 2", "details eruit"])
    s.vak("s3", "llm", 530, 34, 130, 52, ["Stap 3", "schrijf antwoord"])
    s.vak("uit", "io", 690, 40, 70, 40, ["Concept"])
    s.vak("stop", "io", 265, 130, 80, 36, ["Stop"])
    s.pijl(s.p("in", "r"), s.p("s1", "l"))
    s.pijl(s.p("s1", "r"), s.p("gate", "l"))
    s.pijl(s.p("gate", "r"), s.p("s2", "l"))
    s.tekst(355, 52, "ja")
    s.pijl(s.p("s2", "r"), s.p("s3", "l"))
    s.pijl(s.p("s3", "r"), s.p("uit", "l"))
    s.pijl(s.p("gate", "b"), s.p("stop", "t"))
    s.tekst(311, 112, "nee", anker="start")
    return s


def les11():
    s = Schema("les11", 720, 260, "Een router bepaalt de soort. Elke soort gaat naar een eigen workflow uit een eerdere les.")
    s.vak("in", "io", 10, 110, 90, 40, ["Bericht"])
    s.vak("llm", "llm", 130, 104, 140, 52, ["LLM", "bepaalt de soort"])
    s.vak("code", "code", 320, 104, 110, 52, ["if / elif", "jouw code"])
    s.vak("a", "llm", 500, 24, 215, 52, ["vraag → les 9", "kennisbank + LLM"])
    s.vak("b", "mens", 500, 104, 215, 52, ["klacht → les 8", "concept, een mens keurt"])
    s.vak("c", "code", 500, 184, 215, 52, ["compliment", "vaste tekst, geen LLM"])
    s.pijl(s.p("in", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "r"), s.p("code", "l"))
    s.tekst(295, 122, "soort")
    s.pijl((430, 130), (465, 130), (465, 50), (500, 50))
    s.pijl((430, 130), (500, 130))
    s.pijl((430, 130), (465, 130), (465, 210), (500, 210))
    return s


def les12():
    s = Schema("les12", 715, 230, "Twee checks draaien tegelijk. Alleen als beide goedkeuren, mag het bericht door.")
    s.vak("in", "io", 10, 95, 80, 40, ["Bericht"])
    s.vak("a", "llm", 165, 30, 210, 52, ["Check onderwerp", "gaat het over de webshop?"])
    s.vak("b", "llm", 165, 148, 210, 52, ["Check veiligheid", "wil iemand de bot misleiden?"])
    s.vak("code", "code", 435, 89, 110, 52, ["Beide ✓?", "jouw code"])
    s.vak("ja", "io", 588, 38, 120, 36, ["Mag door"])
    s.vak("nee", "io", 588, 156, 120, 36, ["Tegengehouden"])
    s.pijl((90, 115), (125, 115), (125, 56), (165, 56))
    s.pijl((90, 115), (125, 115), (125, 174), (165, 174))
    s.tekst(133, 119, "tegelijk", anker="start")
    s.pijl((375, 56), (405, 56), (405, 105), (435, 105))
    s.pijl((375, 174), (405, 174), (405, 125), (435, 125))
    s.pijl((545, 105), (566, 105), (566, 56), (588, 56))
    s.tekst(574, 88, "ja", anker="start")
    s.pijl((545, 125), (566, 125), (566, 174), (588, 174))
    s.tekst(574, 148, "nee", anker="start")
    return s


def les12_tijd():
    s = Schema("les12t", 700, 182, "Tijdlijn: na elkaar tel je de wachttijd op, tegelijk wacht je alleen op de langzaamste check.")
    x0, per_s = 130, 90

    def balk(van, tot, y, h, tekst):
        s.dozen.append(
            f'<rect class="v-llm" x="{x0 + van * per_s}" y="{y}" width="{(tot - van) * per_s}" height="{h}" rx="5"/>'
            f'<text class="sub sterk" x="{x0 + van * per_s + 8}" y="{y + h / 2 + 4}">{esc(tekst)}</text>'
        )

    s.tekst(118, 43, "Na elkaar", anker="end", klasse="hoofd")
    balk(0, 2.4, 26, 26, "onderwerp")
    balk(2.4, 4.9, 26, 26, "veiligheid")
    s.tekst(x0 + 4.9 * per_s + 8, 43, "klaar na ± 5 s", anker="start", klasse="lbl")
    s.tekst(118, 107, "Tegelijk", anker="end", klasse="hoofd")
    balk(0, 2.4, 76, 24, "onderwerp")
    balk(0, 2.7, 104, 24, "veiligheid")
    s.tekst(x0 + 2.7 * per_s + 8, 121, "klaar na ± 3 s", anker="start", klasse="lbl")
    s.lijnen.append(f'<line class="as" x1="{x0}" y1="146" x2="{x0 + 6 * per_s}" y2="146"/>')
    for sec in range(7):
        x = x0 + sec * per_s
        s.lijnen.append(f'<line class="as" x1="{x}" y1="146" x2="{x}" y2="151"/>')
        s.tekst(x, 168, f"{sec} s", klasse="lbl zacht")
    return s


def les13():
    s = Schema("les13", 720, 248, "De agent-loop: het LLM kiest een tool, jouw code voert hem uit en het resultaat gaat terug, tot er geen tool meer nodig is.")
    s.vak("in", "io", 10, 50, 90, 40, ["Vraag"])
    s.vak("llm", "llm", 140, 44, 170, 52, ["LLM", "kiest de volgende stap"])
    s.vak("keuze", "code", 370, 44, 150, 52, ["Tool gekozen?", "jouw code checkt"])
    s.vak("uit", "io", 590, 50, 120, 40, ["Antwoord"])
    s.vak("voer", "code", 370, 170, 150, 52, ["Voer tool uit", "voer_tool_uit()"])
    s.vak("tools", "tool", 570, 158, 145, 76, ["tools", "zoek_bestelling", "volg_pakket"], links=True)
    s.pijl(s.p("in", "r"), s.p("llm", "l"))
    s.pijl(s.p("llm", "r"), s.p("keuze", "l"))
    s.pijl(s.p("keuze", "r"), s.p("uit", "l"))
    s.tekst(555, 62, "nee")
    s.pijl(s.p("keuze", "b"), s.p("voer", "t"))
    s.tekst(452, 137, "ja", anker="start")
    s.pijl((520, 188), (570, 188))
    s.pijl((570, 206), (520, 206))
    s.pijl(s.p("voer", "l"), (225, 196), s.p("llm", "b"))
    s.tekst(297, 188, "resultaat terug")
    s.tekst(297, 216, "ronde 1, 2, 3 … max. 5", klasse="lbl zacht")
    return s


def les14():
    s = Schema("les14", 720, 222, "De klant ziet alleen het antwoord. De stappen van de agent gaan naar het bestand agent.log.")
    s.vak("in", "io", 10, 40, 90, 40, ["Vraag"])
    s.vak("agent", "code", 140, 34, 160, 52, ["Agent-loop", "uit les 13"])
    s.vak("scherm", "io", 420, 30, 290, 40, ["Klant ziet alleen het antwoord"])
    s.vak("log", "tool", 420, 96, 290, 116, ["agent.log", "INFO Vraag: Waar blijft 1001?", "INFO Stap 1: tool zoek_bestelling", "INFO Stap 2: tool volg_pakket", "INFO Stap 3: klaar"], links=True)
    s.pijl(s.p("in", "r"), s.p("agent", "l"))
    s.pijl((300, 50), (420, 50))
    s.tekst(360, 42, "print")
    s.pijl((300, 72), (360, 72), (360, 154), (420, 154))
    s.tekst(352, 122, "logging", anker="end")
    return s


def les15():
    s = Schema("les15", 720, 182, "De schrijver maakt een concept, de controleur keurt het. Afgekeurd gaat terug met feedback; goedgekeurd gaat naar de mens.")
    s.vak("in", "io", 10, 40, 90, 40, ["Klacht"])
    s.vak("schr", "llm", 140, 34, 160, 52, ["Schrijver", "LLM: maakt concept"])
    s.vak("ctrl", "llm", 390, 34, 160, 52, ["Controleur", "LLM: checkt de regels"])
    s.vak("mens", "mens", 600, 34, 115, 52, ["Mens", "j of n"])
    s.pijl(s.p("in", "r"), s.p("schr", "l"))
    s.pijl(s.p("schr", "r"), s.p("ctrl", "l"))
    s.tekst(345, 52, "concept")
    s.pijl(s.p("ctrl", "r"), s.p("mens", "l"))
    s.tekst(575, 52, "goed")
    s.pijl((470, 86), (470, 140), (220, 140), (220, 86))
    s.tekst(345, 132, "afgekeurd + feedback")
    s.tekst(345, 160, "max. 3 rondes, daarna beslist de mens", klasse="lbl zacht")
    return s


def les16():
    s = Schema("les16", 720, 316, "Links de onderdelen van les 13, rechts waar ze in de SDK zitten. Gestippeld: dat zie je niet meer.")
    s.tekst(20, 28, "Les 13 · zelf gebouwd (111 regels)", anker="start", klasse="hoofd")
    s.tekst(420, 28, "Les 16 · met de SDK (52 regels)", anker="start", klasse="hoofd")
    rijen = [
        ("tools = [ … ]  (26 regels)", "@function_tool + docstring", False),
        ("voer_tool_uit()", "zit in de SDK", True),
        ("for stap in range(…)", "Runner.run_sync(max_turns=5)", False),
        ("plan B na de lus", "except MaxTurnsExceeded", False),
        ("logging naar agent.log", "tracing in het dashboard", False),
    ]
    for i, (links, rechts, weg) in enumerate(rijen):
        y = 46 + i * 52
        s.vak(f"l{i}", "code", 20, y, 300, 40, [links], mono=True)
        s.vak(f"r{i}", "code", 420, y, 280, 40, [rechts], mono=True, stippel=weg)
        s.pijl(s.p(f"l{i}", "r"), s.p(f"r{i}", "l"), stippel=weg)
    return s


SCHEMAS = {f.__name__: f for f in (
    augmented, les1, les2, les3, les4, les5, les6, les7, les8, les9,
    les10, les11, les12, les12_tijd, les13, les14, les15, les16,
)}


# ---------------------------------------------------------------- code kleuren

PY = re.compile(
    r'(?P<com>#[^\n]*)'
    r'|(?P<str>[fF]?"""[\s\S]*?"""|[fF]?"[^"\n]*"|\'[^\'\n]*\')'
    r'|(?P<dec>@\w+)'
    r'|(?P<kw>\b(?:def|return|for|in|if|elif|else|while|break|class|import|from|try|except|as|async|await|not|and|or|True|False|None)\b)'
)


def kleur_python(code):
    uit, pos = [], 0
    for m in PY.finditer(code):
        uit.append(esc(code[pos:m.start()]))
        uit.append(f'<span class="{m.lastgroup}">{esc(m.group())}</span>')
        pos = m.end()
    uit.append(esc(code[pos:]))
    return "".join(uit)


def kleur_terminal(tekst):
    regels = []
    for regel in tekst.split("\n"):
        if regel.startswith("$ "):
            regels.append(f'<span class="prompt">$</span> <span class="cmd">{esc(regel[2:])}</span>')
            continue
        r = esc(regel)
        r = re.sub(r"⟦(.*?)⟧", r'<kbd>\1</kbd>', r)
        r = re.sub(r"^(AI:)", r'<span class="ai">\1</span>', r)
        r = re.sub(r"^(\(.*\))$", r'<span class="dim">\1</span>', r)
        r = re.sub(r"\b(INFO)\b", r'<span class="info">\1</span>', r)
        r = re.sub(r"\b(WARNING)\b", r'<span class="warn">\1</span>', r)
        regels.append(r)
    return "\n".join(regels)


def bouw():
    pagina = SJABLOON.read_text()

    def schema(m):
        return SCHEMAS[m.group(1)]().svg()

    pagina = re.sub(r"\{\{schema:(\w+)\}\}", schema, pagina)
    pagina = re.sub(
        r'<pre class="py">\n?([\s\S]*?)</pre>',
        lambda m: f'<pre class="py"><code>{kleur_python(m.group(1).rstrip())}</code></pre>',
        pagina,
    )
    pagina = re.sub(
        r'<pre class="term">\n?([\s\S]*?)</pre>',
        lambda m: f'<pre class="term"><code>{kleur_terminal(m.group(1).rstrip())}</code></pre>',
        pagina,
    )
    DOEL.write_text(pagina)
    print("geschreven:", DOEL, len(pagina), "tekens")


if __name__ == "__main__":
    bouw()
