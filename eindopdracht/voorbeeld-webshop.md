# Voorbeeld: het dossier van de webshop

Dit is een kort ingevuld voorbeeld bij `dossier.md`, voor de webshop uit de lessen. De webshop bestaat niet: de docent speelt de klant, en de getallen van de nulmeting zijn verzonnen. **De testuitvoer en het logboek zijn echt:** les 18 draaide op 19 oktober 2026 op de klassenserver, met de vier voorbeeldmails uit `voorbeelden/mails/`.

| | |
|---|---|
| Groep | het lesboek |
| Bedrijf | de webshop uit de lessen (de docent speelt de klant) |
| Contactpersoon bij het bedrijf | de klantenservice |
| De taak in één zin | Een concept-antwoord klaarzetten voor elke vraag die een klant mailt. |
| Einddatum | het eind van de eindopdracht |

---

## Fase 1: klant en proces

### Het intakegesprek

Een paar antwoorden, kort:

1. Vragen van klanten per mail, ongeveer 40 per week.
2. Een medewerker van de klantenservice zoekt het antwoord op in de informatie van de webshop en typt een antwoord.
3. De mails komen binnen in de mailbox. In de pilot zet de medewerker ze als tekstbestand in een map. De concepten gaan als tekstbestand terug.
4. Goed is: het klopt met de informatie van de webshop, en de medewerker hoeft hooguit één zin aan te passen.
5. Nooit iets beloven dat niet in de informatie staat, zoals geld terug.
6. Ja: namen, en soms een bestelnummer. Voor het bouwen gebruiken we nagemaakte mails.

### Het proces nu

Een mail komt binnen (wit) → de medewerker leest hem (roze) → zoekt het antwoord op in de informatie van de webshop (geel) → typt een antwoord (roze) → verstuurt het (roze).

### De nulmeting (verzonnen voor dit voorbeeld)

| Wat | Nu |
|---|---|
| Hoe vaak per week | 40 mails |
| Minuten per keer, inclusief nakijken | 4 |
| Hoe vaak gaat het mis, en wat gaat er dan mis? | 2 keer per week een fout antwoord over verzendlanden |
| Hoe hebben jullie dit gemeten? | Verzonnen. Bij jullie: een week turven samen met de medewerker. |

---

## Fase 2: ontwerp

### De ontwerpvragen

1. Concept-antwoorden voor de medewerkers van de klantenservice.
2. Erin: één mail per bestand in `inbox/`. Eruit: één concept per mail in `concepten/`, met de originele mail erboven.
3. Eén LLM-call met de kennisbank (les 9). Gewone code kan geen antwoord schrijven op een vrije vraag. Een agent is niet nodig, want de stappen staan vast: lees de mail, schrijf het antwoord.
4. De instructie van les 9, met de kennisbank (`kennisbank.json`) erbij.
5. Geen tools: de hele kennisbank past in één prompt.
6. Klaar als het concept in `concepten/` staat; de mail gaat dan naar `verwerkt/` (les 18). Mislukt een call, dan blijft de mail in de inbox, en de volgende run probeert hem opnieuw.
7. Met de testgevallen hieronder, en in de pilot beoordeelt de medewerker elk concept.

### Wanneer is een resultaat goed?

1. Het antwoord klopt met de kennisbank.
2. Staat iets niet in de kennisbank, dan zegt het concept dat eerlijk, zonder iets te beloven.
3. De klant ziet geen woorden van binnen het bedrijf, zoals "kennisbank".
4. Een klacht krijgt geen inhoudelijk antwoord; die gaat naar een medewerker.

### De testgevallen

Hier vier. Bij jullie zijn het er ongeveer 20.

| Nr | Bestand | Wat moet er gebeuren? |
|---|---|---|
| 1 | `mail-01.txt` (jas terugsturen) | Ja, binnen 30 dagen met de bon; het geld is binnen 5 tot 7 werkdagen terug. |
| 2 | `mail-02.txt` (België) | Zegt eerlijk dat België niet in de informatie staat. |
| 3 | `mail-03.txt` (Apple Pay) | Zegt dat Apple Pay niet in de informatie staat, niet dat het niet kan. |
| 4 | `mail-04.txt` (pakket kwijt) | Een klacht: geen inhoudelijk antwoord, maar naar een medewerker. |

---

## Fase 3: lokaal bouwen

### Het testlog

**Run 1 (19 oktober, 14:55):** versie `6db69e6`, les 18 zonder veranderingen. Duur: 19 seconden voor 4 mails.

| Nr | Wat moest er gebeuren? | Wat gebeurde er? | Oordeel |
|---|---|---|---|
| 1 | terugsturen binnen 30 dagen | "Ja, je kunt de jas binnen 30 dagen na aankoop terugsturen met de bon. Je krijgt je geld binnen 5 tot 7 werkdagen terug, …" | goed |
| 2 | eerlijk over België | "…maar in de kennisbank staat niet of België daaronder valt." | deels: klopt, maar het woord "kennisbank" (punt 3) |
| 3 | Apple Pay staat er niet in | "Apple Pay wordt niet genoemd in onze kennisbank, dus ik kan niet bevestigen of je daarmee kunt betalen. Je kunt wel betalen met iDEAL, PayPal of creditcard …" | deels: "kennisbank" |
| 4 | naar een medewerker | "…in onze kennisbank staat niet wat we doen als een pakket is kwijtgeraakt. Ik kan je daarom niet vertellen hoe we dit oplossen." | fout: niet naar een medewerker (punt 4), en "kennisbank" |

**Run 2 (19 oktober, 14:58):** dezelfde vier mails nog een keer, en dezelfde versie. Ze kregen nieuwe namen, `mail-11` tot en met `mail-14`, want les 18 slaat een mail over als het concept al bestaat. Andere zinnen, dezelfde betekenis. "Kennisbank" stond weer in 3 van de 4 concepten.

**Wat we hiervan leren:** de twee fouten zijn geen toeval, want ze komen uit de opzet. De instructie verbiedt het woord "kennisbank" niet, en les 18 heeft geen aparte route voor klachten. De volgende stap: één regel in de instructie, en daarna dezelfde vier gevallen opnieuw. Een route voor klachten is een router (les 11), en daarmee een nieuwe keuze in de keuzehulp.

### De grenzen in de code

| Grens | Waarde | Waar in de code? |
|---|---|---|
| Hoeveel bestanden per run | nog geen | – |
| Hoeveel LLM-calls per bestand | 1 | `beantwoord_vraag` doet er één |
| Hoe lang de uitvoer mag zijn | nog geen | – |

Les 18 heeft nog geen grens aan het aantal bestanden: staan er 1.000 mails in de inbox, dan doet één run 1.000 calls. Die grens moet erbij.

---

## Fase 4: op de server

- Versie op de server: `6db69e6`
- Uitgelogd om: 14:50, na het uploaden met `scp`
- Het logboek van de run om 14:55, terwijl niemand ingelogd was:

```
Oct 19 14:55:01 klasserver systemd[1576]: Starting inbox.service - Les 18: de mails in de inbox verwerken...
Oct 19 14:55:06 klasserver les18[7071]: 4 mails in /home/groep0/werk/inbox
Oct 19 14:55:12 klasserver les18[7071]: Verwerkt: mail-01.txt
Oct 19 14:55:14 klasserver les18[7071]: Verwerkt: mail-02.txt
Oct 19 14:55:17 klasserver les18[7071]: Verwerkt: mail-03.txt
Oct 19 14:55:20 klasserver les18[7071]: Verwerkt: mail-04.txt
Oct 19 14:55:20 klasserver les18[7071]: Klaar. Een medewerker leest de concepten na en verstuurt ze zelf.
Oct 19 14:55:21 klasserver systemd[1576]: Finished inbox.service - Les 18: de mails in de inbox verwerken.
```

---

## Fase 5: pilot, eindtest en overdracht

Niet ingevuld: de webshop bestaat niet, dus er is geen pilot. Bij jullie staan hier de pilot met een echte medewerker, de eindtest, de vergelijking met de nulmeting en de overdracht.
