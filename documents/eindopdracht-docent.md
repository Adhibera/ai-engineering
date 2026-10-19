# Eindopdracht: het deel voor de docent

Leerlingen lezen de opdracht in het lesboek, in de sectie "Eindopdracht", en vullen `eindopdracht/dossier.md` in. Dit deel is voor de docent: hoe je een opdracht kiest, wat niet mag, wat de school met het bedrijf afspreekt, hoe de pilot verloopt, en hoe je beoordeelt. Het hosten staat in `documents/serverdraaiboek.md`.

**Dit is geen juridisch advies.** Laat de privacyfunctionaris van de school dit deel en het afspraaksjabloon controleren voordat je ermee begint.

## In het kort

- Elke groep (advies: drie leerlingen) automatiseert één taak voor één bedrijf.
- Een medewerker van het bedrijf beoordeelt elk resultaat. Het programma verstuurt, betaalt of beslist niets zelf.
- De school sluit de afspraak met het bedrijf, niet de leerling.
- Het programma draait op de klassenserver, met de key van de groep, tot de einddatum.
- Bouwen gebeurt met nagemaakte voorbeelden. Echte gegevens alleen na akkoord van de school en het bedrijf.

---

## Een goede opdracht

Een opdracht is geschikt als:

1. de taak nu door een mens gedaan wordt;
2. hij vaak terugkomt: minstens 10 keer per week, zodat een pilot van twee weken minstens 20 concepten oplevert;
3. er tekst bij hoort, zodat een LLM iets toevoegt;
4. een medewerker elk resultaat kan nakijken;
5. hij te testen is met voorbeelden waarvan de klant zegt wat goed is;
6. de invoer als bestand of export kan komen (één invoer, één uitvoer);
7. je hem kunt bouwen met nagemaakte voorbeelden;
8. er een contactpersoon is met tijd: een intakegesprek, een gesprek over het ontwerp, en een medewerker voor de pilot.

**Voorbeelden:**
- vragen van klanten of offerteaanvragen: een concept-antwoord klaarzetten;
- productteksten schrijven uit een lijst met specificaties;
- meldingen of klachten indelen en samenvatten voor een medewerker;
- voor de school: vragen aan de administratie beantwoorden, of bij een vraag in de mediatheek boeken zoeken.

## De rode lijst

Dit is de grens van deze cursus. Zulke opdrachten doen we niet, ook niet als het bedrijf het wil:

- beslissingen over mensen: sollicitanten kiezen, leerlingen beoordelen, kredietwaardigheid;
- medisch, juridisch of financieel advies;
- bijzondere persoonsgegevens, zoals gezondheid of geloof, en strafrechtelijke gegevens (die vallen in de AVG onder een eigen regeling);
- iets dat zonder mens naar buiten gaat;
- een openbare chatbot op de website;
- betalen of bestellen;
- in de eerste ronde: toegang tot de mailbox of andere systemen van het bedrijf.

Werving en selectie, het beoordelen van leerresultaten en kredietwaardigheid staan in bijlage III van de AI-verordening (systemen met een hoog risico). Een medewerker die controleert, maakt dat niet vanzelf in orde. Bron: [AI Act Service Desk, bijlage III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3).

## Privacy

**Standaard werkt een groep met nagemaakte voorbeelden.** "Zonder namen" is nog niet anoniem: een adres, een ordernummer of een detail kan iemand ook herkenbaar maken.

**Voordat er echte gegevens komen,** beslist de privacyfunctionaris van de school, samen met het bedrijf. Een lijstje voor dat gesprek:

- Wie is verantwoordelijk voor de gegevens, en wie is verwerker?
- Op welke grondslag mogen de gegevens gebruikt worden?
- Welke verwerkersovereenkomsten zijn nodig? De gegevens gaan naar Hetzner (de server staat in Nürnberg) en naar OpenAI.
- Gaan gegevens buiten de EU? De OpenAI-projecten staan op "Global": er is geen garantie dat de gegevens in de EU blijven.
- Wie kan erbij? De groep, en de docent als beheerder (die kan ook de logboeken lezen).
- Wanneer wordt alles gewist? Wat de school en de groep beheren (de server, laptops, de repo), uiterlijk op de einddatum. Er zijn geen backups op de server. Wat OpenAI voor misbruikcontrole bewaart, valt daar niet onder; dat volgt de regels van OpenAI (zie hieronder).

**Wat OpenAI doet:** met `store=False` bewaart OpenAI een antwoord niet om het later op te halen (getest: zo'n antwoord geeft daarna een 404). Dat is geen nulbewaring. Voor misbruikcontrole kan OpenAI gegevens standaard tot 30 dagen bewaren, soms langer. Zero data retention kan alleen na goedkeuring door OpenAI. Bron: [OpenAI Docs, Your data](https://developers.openai.com/api/docs/guides/your-data). Hoe de projecten staan ingesteld, staat in het serverdraaiboek onder "Gegevens bij OpenAI".

**Wat de eisen in het lesboek al regelen:**
- `store=False` bij elke call, en bij de Agents SDK tracing uit;
- in het logboek en in foutmeldingen alleen de bestandsnaam, de status en de soort fout, nooit de tekst;
- bestandsnamen zonder persoonsgegevens, zoals `mail-001.txt`;
- met echte gegevens: kopieën op laptops wissen zodra de overdracht klaar is.

## De pilot

Spreek vóór de pilot af, met de groep en de medewerker:

- wanneer de medewerker de bestanden aanlevert, en hoe;
- wanneer de groep ze naar de server brengt (`scp` naar `~/werk/inbox`), en de concepten terughaalt;
- hoe de concepten bij de medewerker komen. Die route keuren de school en het bedrijf goed; een privémail van een leerling hoort daar niet bij;
- wie kijkt of er bestanden blijven liggen of mislukken, en hoe vaak (zie "Wat je ziet als het misgaat" in het serverdraaiboek).

**Stoppen** doe je als een concept schade kan doen (iets beloven, iemand beledigen, gegevens van een andere klant tonen), bij een datalek, als de kostengrens bereikt is, of als het bedrijf wil stoppen.
- De groep stopt de timer én een run die nog loopt:
  ```bash
  systemctl --user disable --now inbox.timer
  systemctl --user stop inbox.service
  ```
- De docent kan altijd de noodstop uit het serverdraaiboek gebruiken.

**Bij een incident** is de docent het aanspreekpunt, voor de groep en voor het bedrijf. Een datalek gaat volgens de procedure van de school.

## Een afspraaksjabloon voor school en bedrijf

Kopieer dit, vul het in, en laat het controleren door de school.

```
AFSPRAAK EINDOPDRACHT AI ENGINEERING

School:                       …    contactpersoon (docent): …
Bedrijf:                      …    contactpersoon: …
Groep leerlingen:             …

1. De taak
   In één zin: …
   Het programma maakt concepten. Een medewerker van het bedrijf beoordeelt elk
   concept en verstuurt het zelf. Het programma verstuurt, betaalt en beslist niets.

2. Periode
   Van … tot de einddatum: …

3. Wat het bedrijf levert
   - voorbeelden (nagemaakt, of zonder herkenbare gegevens): …
   - tijd van de contactpersoon: … gesprekken van … minuten
   - een medewerker die in de pilot de concepten beoordeelt: …

4. Gegevens
   [ ] alleen nagemaakte voorbeelden
   [ ] echte gegevens, na akkoord van de privacyfunctionaris op …
       welke gegevens: …
   Het programma draait op een server van de school bij Hetzner (Duitsland) en
   gebruikt OpenAI. Antwoorden worden niet opgeslagen om later op te halen
   (store=False), maar OpenAI kan gegevens voor misbruikcontrole bewaren,
   standaard tot 30 dagen en soms langer. Er is geen garantie dat de gegevens
   bij OpenAI in de EU blijven. Toegang op de server: de groep en de docent.

5. Route in de pilot
   De bestanden komen bij de groep via: …
   De concepten gaan terug via: …
   Momenten: …

6. Kosten
   De school betaalt het gebruik van OpenAI, met een harde limiet van … per maand.

7. Stoppen en incidenten
   De school stopt het programma bij schade, een datalek, de kostengrens, of als
   het bedrijf dat vraagt. Aanspreekpunt: de docent.

8. Na de einddatum
   [ ] de school zet het programma uit en wist de gegevens op de server; de groep
       wist de kopieën op laptops
   [ ] het bedrijf neemt het over, met een eigen OpenAI-key, een eigen server en
       het overdrachtsdocument van de groep
   De code: …

9. Leerlingenwerk
   Dit is een schoolopdracht. Er is geen garantie dat het programma foutloos werkt.
   De school beoordeelt de leerlingen; de mening van het bedrijf telt mee als input.

Handtekening school: …             Handtekening bedrijf: …
Datum: …
```

## Planning

Een begin voor tijdvak 2 tot en met 6. Pas het aan de lengte van de tijdvakken aan.

| Tijdvak | Fase |
|---|---|
| 2 | Klant en proces |
| 3 | Ontwerp, en beginnen met bouwen |
| 4 | Lokaal bouwen |
| 5 | Op de server, en de pilot begint |
| 6 | Pilot afronden, eindtest, presentatie en overdracht |

Twee harde momenten:
- **Halverwege tijdvak 2** is de afspraak met het bedrijf getekend. Lukt dat niet, dan stapt de groep over naar de reserveklant.
- **Uiterlijk drie weken voor het eind** draait het programma op de server, zodat de pilot van twee weken en de presentatie nog passen.

Plan er twee lessen bij:
- **Vóór fase 1:** het intakegesprek oefenen, met de docent als de webshop uit de lessen, zoals het rollenspel vóór les 13.
- **Vóór fase 3:** de eigen repo. De lessen leren `git clone` en `git pull`, maar niet `git commit` en `git push`. De stappen staan in het lesboek. Regel in deze les ook het inloggen bij GitHub vanaf de laptop: het wachtwoord van GitHub werkt niet voor `git push` via HTTPS. Dat kan met GitHub Desktop, met Git Credential Manager (zit bij Git voor Windows) of met de GitHub CLI (`gh auth login`). Dit is niet getest op laptops van leerlingen.

## Per groep klaarzetten

1. **De gebruiker en de key:** zie "Een groep aanmaken" en "Een OpenAI-key per groep" in het serverdraaiboek.
2. **De privé-repo:** de groep maakt hem zelf, en maakt de docent collaborator. Op de server komt een eigen sleutel als read-only deploy key in de repo. De stappen staan in het lesboek. Dit is op 19 oktober getest op `groep0` (zie "Wat er getest is" in het serverdraaiboek).
3. **De reserveklant:** regel vooraf één reserveklant, met dezelfde eisen. De school zelf kan dat zijn, bijvoorbeeld de administratie of de mediatheek.

## Controlemomenten

| Wanneer | Wat | Wie |
|---|---|---|
| Eind fase 1 | de afspraak getekend, en het proces en de nulmeting in het dossier | de docent, de school en het bedrijf |
| Eind fase 2 | het ontwerp en de testgevallen; 5 gevallen gaan naar de docent | de docent |
| Vóór echte gegevens | het akkoord van de privacyfunctionaris en het bedrijf | de school |
| De einddatum | uitzetten en wissen, of overdragen | de docent |

## Beoordelen

De rubric staat in het lesboek, bij de eindopdracht. Hij heeft vijf onderdelen, met elk drie niveaus: Beginnend, Voldoende en Goed.

- **Eerst de eisen.** Ontbreekt een eis, dan herstelt de groep die eerst, binnen een afgesproken termijn. Daarna beoordeel je.
- **Een cijfer:** 6 als alles Voldoende is, plus 0,8 voor elk onderdeel op Goed, en min 1 voor elk onderdeel dat na de hersteltermijn nog op Beginnend staat. Bijvoorbeeld: twee keer Goed en drie keer Voldoende geeft een 7,6. Heeft de school eigen regels in het PTA, dan gaan die voor.
- **Hosten** is een eis, maar levert geen punten op en kost geen punten. Mislukt het door een technisch probleem, dan telt het lokale programma.
- **De mening van de klant** telt mee als input, niet als cijfer.
- **De eindtest** draait de groep één keer, met de 5 gevallen die jij bewaard hebt.

## Na de einddatum

- [ ] De timer uit, en een lopende run gestopt (zie "De pilot").
- [ ] `~/werk` gewist op de server.
- [ ] Met echte gegevens: de groep bevestigt dat de kopieën op laptops gewist zijn.
- [ ] De OpenAI-key van de groep ingetrokken.
- [ ] De deploy key verwijderd uit de privé-repo (Settings → Deploy keys).
- [ ] Of de hele groep verwijderd: zie "Een groep verwijderen" in het serverdraaiboek.

Neemt het bedrijf het over, dan krijgt het de code, het overdrachtsdocument uit het dossier, en zet het een eigen OpenAI-key en een eigen server in. De key en de server van de school gaan niet mee.
