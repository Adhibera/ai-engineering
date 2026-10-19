# Projectdossier: <naam van jullie project>

Dit is het dossier van jullie eindopdracht. Vul het per fase in. Het staat in jullie privé-repo, dus de docent ziet elke versie. Schrijf kort: een paar zinnen of een tabel is genoeg. Een ingevuld voorbeeld staat in `voorbeeld-webshop.md`.

Zet hier nooit persoonsgegevens in: geen namen, adressen of mails van klanten van het bedrijf.

| | |
|---|---|
| Groep | |
| Bedrijf | |
| Contactpersoon bij het bedrijf | (functie, geen privégegevens) |
| De taak in één zin | |
| Einddatum | |

---

## Fase 1: klant en proces

### Het intakegesprek

Datum, en wie erbij waren:

1. Welke taak kost jullie veel tijd en komt vaak terug? Hoe vaak per week?
2. Wie doet het nu, en hoe? Mogen we meekijken?
3. Waar komt het werk vandaan (mail, formulier, export), en waar gaat het resultaat heen?
4. Wanneer is een resultaat goed? Mogen we voorbeelden zien, nagemaakt of zonder herkenbare gegevens?
5. Wat mag nooit misgaan? Wat gebeurt er bij een fout?
6. Zitten er persoonsgegevens in? Wie beslist daar bij jullie over?
7. Wie is onze contactpersoon, hoeveel tijd heeft die, en wie beoordeelt de concepten in de pilot?
8. Wat moet er na de einddatum gebeuren?

### Het proces nu

Teken het proces zoals een medewerker het nu doet: wat komt erin, welke stappen, wat gaat eruit. Gebruik de kleuren van het lesboek (roze = mens, geel = data). Zet de tekening in de repo, bijvoorbeeld als `eindopdracht/proces.png`.

- Tekening:
- In woorden:

### De nulmeting

| Wat | Nu |
|---|---|
| Hoe vaak per week | |
| Minuten per keer, inclusief nakijken | |
| Hoe vaak gaat het mis, en wat gaat er dan mis? | |
| Hoe hebben jullie dit gemeten? | |

- [ ] Akkoord van de docent (datum):

---

## Fase 2: ontwerp

### De ontwerpvragen

1. Welke taak, en voor wie bij het bedrijf?
2. Wat gaat erin, en wat komt eruit?
3. Welke oplossing uit de keuzehulp (gewone code, één LLM-call, een workflow of een begrensde agent), en waarom niet een eenvoudigere?
4. Als er een LLM in zit: welke instructie krijgt het, en welke voorbeelden of gegevens?
5. Als er tools nodig zijn: welke, en wat doen ze?
6. Wanneer is een bestand klaar, en wat gebeurt er als het misgaat?
7. Hoe weten jullie en de klant dat het resultaat goed is?

### Wanneer is een resultaat goed?

De klant stelt dit vast, vóór jullie gaan bouwen. Een oud antwoord van het bedrijf is niet vanzelf goed.

1.
2.
3.

### De testgevallen

Ongeveer 20 gevallen van de klant. Daarvan gaan er 5 naar de docent, voor de eindtest. Die 5 staan hier niet.

| Nr | Bestand | Wat moet er gebeuren? |
|---|---|---|
| 1 | | |

- [ ] Akkoord van de docent (datum):

---

## Fase 3: lokaal bouwen

### Het testlog

Draai na elke verandering dezelfde testgevallen. Commit de verandering eerst, zodat de versie klopt. Begin elke run in een lege werkmap, met alleen de testgevallen in de inbox: net als les 18 slaat jullie programma een bestand over als het concept al bestaat. Noteer per run:

**Run (datum):** versie `…` (uit `git log --oneline -1`). Wat er veranderd is: … Duur van de run: …

| Nr | Wat moest er gebeuren? | Wat gebeurde er? | Oordeel (goed, deels, fout) |
|---|---|---|---|
| 1 | | | |

### De grenzen in de code

| Grens | Waarde | Waar in de code? |
|---|---|---|
| Hoeveel bestanden per run | | |
| Hoeveel LLM-calls per bestand | | |
| Hoe lang de uitvoer mag zijn | | |

---

## Fase 4: op de server

- Versie op de server (de regel na "Klaar." van `deploy.sh`):
- Uitgelogd om:
- Het logboek van een run die begon terwijl niemand ingelogd was (uit `journalctl --user -u inbox.service`):

```
(plak hier de regels)
```

---

## Fase 5: pilot, eindtest en overdracht

### Afspraken voor de pilot

| | |
|---|---|
| Wanneer brengen we de bestanden naar de server? | |
| Hoe komen de concepten bij de medewerker? (goedgekeurd door school en bedrijf) | |
| Wie kijkt of er bestanden blijven liggen of mislukken, en hoe vaak? | |
| Met echte gegevens: wanneer wissen we de kopieën op onze laptops? | |

### Het pilotlog

| Datum | Bestand | Bruikbaar zoals het is / na aanpassing / niet bruikbaar | Minuten nakijken | Opmerking |
|---|---|---|---|---|
| | | | | |

Het brengen en halen kost ook tijd. Tel die mee, ook als jullie het doen:

| Datum | Aantal bestanden | Minuten voor exporteren, uploaden, terughalen en afleveren | Wie |
|---|---|---|---|
| | | | |

### De eindtest

De docent geeft jullie de 5 apart gehouden gevallen. Draai ze één keer, met de versie van de pilot.

| Nr | Wat moest er gebeuren? | Wat gebeurde er? | Oordeel |
|---|---|---|---|
| E1 | | | |

### De vergelijking met de nulmeting

| | Nu (nulmeting) | Met het programma |
|---|---|---|
| Minuten per keer, inclusief nakijken, en met het programma ook het brengen en halen | | |
| Hoe vaak gaat het mis? | | |
| Kosten per week (OpenAI-dashboard, Usage van jullie project) | – | |

Wat bewijzen deze cijfers wel, en wat niet?

### De overdracht

Schrijf dit zo dat iemand anders het programma kan bedienen zonder jullie hulp.

- **Starten:**
- **Stoppen** (de timer, én een run die nog loopt):
- **Zien of een run mislukt is:**
- **Kosten:**
- **Grenzen:**
- **Bekende fouten:**
- **Wie controleert de concepten:**
- **Na de einddatum:**

- [ ] Met echte gegevens: kopieën op laptops gewist (datum):
