# Agent bouwen met middelbare scholieren in 6 sessies

## Doel van dit document

Dit document werkt het advies uit voor een lessenreeks waarin leerlingen in ongeveer zes sessies leren wat een AI-agent is en hoe zo’n agent “onder de motorkap” werkt.

Het uitgangspunt is niet dat leerlingen meteen een professioneel framework leren, maar dat ze begrijpen wat de bouwstenen zijn:

```text
LLM + instructie + tools + geheugen/state + beslisloop + controle
```

Pas nadat dit basisbegrip staat, kun je frameworks zoals Mastra, LangGraph of de OpenAI Agents SDK laten zien als professionele manieren om hetzelfde principe robuuster te bouwen.

---

# 1. Kernadvies

Voor middelbare scholieren is het verstandig om niet meteen met Mastra, LangGraph of een zwaar agent-framework te starten.

De beste didactische route is:

```text
1. Eerst begrijpen wat een agent is
2. Daarna een simpele AI-assistent maken
3. Daarna een tool toevoegen
4. Daarna een agent-loop bouwen
5. Daarna controle, memory en evaluatie toevoegen
6. Daarna een eigen mini-agent bouwen
```

De aanbevolen technische route is:

```text
Papier / schema / pseudocode
→ simpele Python
→ mini-agent-loop
→ tool calling
→ evaluator-agent
→ eventueel professioneel framework tonen
```

---

# 2. Waarom niet meteen een framework?

Frameworks zoals Mastra, LangGraph, CrewAI of OpenAI Agents SDK zijn krachtig, maar ze abstraheren veel weg.

Dat is handig voor gevorderde ontwikkelaars, maar minder geschikt als leerlingen eerst begrip moeten krijgen.

Bij een framework zien leerlingen vaak:

```text
We typen code
We starten iets
De agent doet iets magisch
```

Maar wat je wilt bereiken is:

```text
Leerlingen zien dat een agent eigenlijk een programma is
dat een taalmodel laat kiezen welke stap of tool nodig is.
```

Daarom is een mini-agent “from scratch” didactisch sterker.

---

# 3. Kernuitleg voor leerlingen

Een eenvoudige definitie:

```text
Een chatbot geeft antwoord.
Een agent kiest acties om een doel te bereiken.
```

Nog eenvoudiger:

```text
LLM = denkt in taal
Tool = doet iets concreets
Agent = regelt wanneer welke tool gebruikt wordt
```

Of als volledige zin:

> Een agent is geen magische AI. Een agent is een programma dat een taalmodel laat kiezen welke stap of tool nodig is om een doel te bereiken.

---

# 4. Bouwstenen van een agent

## 4.1 LLM

Het taalmodel. Dit is het deel dat taal begrijpt, redeneert en tekst genereert.

Voor leerlingen kun je zeggen:

```text
Het LLM is het brein dat taal begrijpt.
```

Maar het LLM kan niet vanzelf echte acties uitvoeren. Het kan bijvoorbeeld niet echt iets opslaan, een bestand openen, een berekening uitvoeren of een agenda aanpassen zonder dat een programma dat mogelijk maakt.

---

## 4.2 Prompt / instructie

De prompt vertelt de agent wat zijn rol, doel en grenzen zijn.

Voorbeeld:

```text
Jij bent een techniekcoach.
Leg technische begrippen uit aan een leerling van 13 jaar.
Gebruik korte zinnen en concrete voorbeelden.
```

De instructie bepaalt dus het gedrag van de agent.

---

## 4.3 Tools

Tools zijn functies die de agent mag gebruiken.

Voorbeelden:

```text
- rekenmachine
- woordenboek
- zoekfunctie
- planning maken
- bestand lezen
- antwoord controleren
- oefenvraag genereren
```

Een tool is dus niet “AI”. Een tool is gewone code.

Voorbeeld in simpele Python:

```python
def tel_op(a, b):
    return a + b
```

De agent kan dan beslissen:

```text
Ik moet rekenen, dus ik gebruik de tool tel_op.
```

---

## 4.4 Memory / state

Memory of state betekent dat de agent informatie bewaart tijdens het uitvoeren van een taak.

Voorbeelden:

```text
- Wat is het doel?
- Welke stappen zijn al uitgevoerd?
- Wat was het vorige antwoord?
- Welke fouten zijn gevonden?
- Is de taak klaar?
```

Voor leerlingen kun je zeggen:

```text
State is het notitieblok van de agent.
```

---

## 4.5 Agent-loop

De agent-loop is de kern van een agent.

In pseudocode:

```text
while taak_niet_klaar:
    vraag aan het LLM: wat is de volgende stap?

    als een tool nodig is:
        voer de tool uit
        geef het resultaat terug aan het LLM

    anders:
        geef het eindantwoord
        stop
```

Dit is de belangrijkste les uit de hele reeks.

Als leerlingen dit begrijpen, begrijpen ze veel beter wat frameworks later voor hen doen.

---

## 4.6 Controle / guardrails

Een agent moet niet alleen iets maken, maar ook controleren of het resultaat goed is.

Voorbeelden van controle:

```text
- Is het antwoord waar?
- Is de taal begrijpelijk?
- Is het niveau passend?
- Is de opdracht veilig?
- Is het resultaat volledig?
- Is de bron correct gebruikt?
```

Voor jouw onderwijscontext is dit zeer belangrijk, omdat een agent die lesmateriaal maakt ook fouten kan maken.

---

# 5. Overzicht van de 6 sessies

| Sessie | Thema | Leerlingen leren |
|---|---|---|
| 1 | Wat is een agent? | Verschil chatbot, assistant en agent |
| 2 | AI-assistent bouwen | Werken met rol, doel en instructie |
| 3 | Tools toevoegen | Verschil tussen denken en doen |
| 4 | Agent-loop bouwen | Hoe een agent stap voor stap werkt |
| 5 | Memory en controle | State, evaluator-agent en verbeteren |
| 6 | Mini-project | Eigen agent ontwerpen en presenteren |

---

# 6. Sessie 1 — Wat is een agent?

## Doel

Leerlingen begrijpen het verschil tussen een gewone chatbot en een agent.

## Kernvraag

```text
Wanneer is AI alleen een chatbot, en wanneer wordt het een agent?
```

## Uitleg

Een chatbot reageert vooral op wat je vraagt.

Een agent heeft een doel en kan meerdere stappen zetten om dat doel te bereiken.

Voorbeeld:

```text
Vraag aan chatbot:
"Maak een planning voor mijn huiswerk."

Chatbot:
Geeft een planning als tekst.

Agent:
- vraagt eventueel wanneer het huiswerk af moet zijn
- controleert hoeveel tijd er is
- verdeelt het werk
- kan een herinnering maken
- past de planning aan als er te weinig tijd is
```

## Activiteit

Laat leerlingen in groepjes voorbeelden bedenken van:

```text
1. Een chatbot
2. Een assistant
3. Een agent
```

Voorbeelden:

```text
Chatbot:
- legt een begrip uit
- beantwoordt een vraag

Assistant:
- helpt met huiswerk
- stelt oefenvragen

Agent:
- maakt een planning
- controleert werk
- zoekt informatie
- maakt een verbeterde versie
- voert meerdere stappen uit
```

## Product aan het einde van sessie 1

Leerlingen maken een eenvoudig schema:

```text
Doel van de agent:
Welke stappen moet hij zetten?
Welke tools zou hij nodig hebben?
Wanneer is hij klaar?
```

---

# 7. Sessie 2 — Bouw een gewone AI-assistent

## Doel

Leerlingen maken eerst een AI-assistent zonder tools.

Hierdoor zien ze dat een assistant nog geen echte agent is.

## Voorbeeldrol

```text
Jij bent een techniekcoach.
Je helpt leerlingen uit klas 2 vmbo basis/kader.
Je legt technische begrippen uit in korte zinnen.
Je gebruikt voorbeelden uit de praktijk.
Je stelt aan het einde één controlevraag.
```

## Voorbeeldopdracht

```text
Leg uit wat spanning, stroom en weerstand zijn.
Gebruik een voorbeeld met water.
```

## Leerdoel

Leerlingen begrijpen dat instructies invloed hebben op het gedrag van het taalmodel.

Ze ontdekken:

```text
- Een vage prompt geeft vaak een vaag antwoord.
- Een duidelijke rol maakt het antwoord beter.
- Een doelgroep noemen helpt.
- Een outputvorm noemen helpt.
```

## Reflectievragen

```text
Wat gebeurde er toen de prompt duidelijker werd?
Wat deed de AI goed?
Wat deed de AI nog niet?
Waarom is dit nog geen echte agent?
```

## Product aan het einde van sessie 2

Een goed geschreven systeeminstructie voor een AI-assistent.

---

# 8. Sessie 3 — Tools toevoegen

## Doel

Leerlingen begrijpen dat een agent tools nodig heeft om acties uit te voeren.

## Kernuitleg

Een LLM kan tekst maken, maar een tool doet iets concreets.

Voorbeeld:

```text
LLM:
"Ik denk dat ik moet rekenen."

Tool:
Voert de berekening echt uit.
```

## Simpele Python-tool

```python
def tel_op(a, b):
    return a + b
```

Of:

```python
def maak_planning(taak, minuten):
    return f"Werk {minuten} minuten aan: {taak}"
```

## Didactisch belangrijk

Laat leerlingen zien dat de tool gewone code is.

De AI is dus niet “alles”. De agent bestaat uit samenwerking tussen:

```text
taalmodel + programma + tools
```

## Mogelijke leerlingopdracht

Laat leerlingen drie tools ontwerpen voor een huiswerk-agent.

Voorbeeld:

```text
Tool 1: bereken hoeveel dagen er nog zijn
Tool 2: verdeel taken over dagen
Tool 3: controleer of de planning haalbaar is
```

## Product aan het einde van sessie 3

Een lijst met tools die hun agent nodig heeft, inclusief korte beschrijving:

```text
Naam tool:
Wat doet de tool?
Welke input heeft de tool nodig?
Welke output geeft de tool terug?
```

---

# 9. Sessie 4 — De agent-loop bouwen

## Doel

Leerlingen begrijpen het mechanisme van een echte agent-loop.

## Kernschema

```text
Gebruiker geeft doel
        ↓
Agent leest doel
        ↓
Agent kiest volgende stap
        ↓
Is een tool nodig?
   ↓ ja             ↓ nee
Tool uitvoeren     Eindantwoord geven
   ↓
Resultaat terug naar agent
   ↓
Nieuwe stap kiezen
```

## Pseudocode

```text
taak_klaar = False

while not taak_klaar:
    vraag aan de agent:
        Wat is de volgende stap?

    als de agent een tool wil gebruiken:
        voer de tool uit
        geef het resultaat terug

    anders:
        geef het eindantwoord
        taak_klaar = True
```

## Leerlingenopdracht

Laat leerlingen een agent-loop tekenen voor een eenvoudige taak.

Voorbeelden:

```text
- maak een quiz over elektriciteit
- plan mijn huiswerk
- verbeter een tekst
- maak een oefenvraag
- controleer een antwoord
```

## Product aan het einde van sessie 4

Een getekende of digitale flowchart van hun agent-loop.

---

# 10. Sessie 5 — Memory, controle en tweede agent

## Doel

Leerlingen begrijpen dat agents kunnen controleren, onthouden en verbeteren.

## Memory / state

Voorbeeld van state:

```json
{
  "doel": "Maak een oefenvraag over stroomkring",
  "niveau": "vmbo basis/kader leerjaar 2",
  "poging": 1,
  "status": "concept gemaakt",
  "feedback": "De vraag is nog te moeilijk"
}
```

## Tweede agent: evaluator-agent

Nu introduceer je twee rollen:

```text
Agent 1: maker
Agent 2: controleur
```

Voorbeeld:

```text
Maker-agent:
Maak een oefenvraag voor vmbo basis/kader.

Controle-agent:
Controleer of de vraag:
- begrijpelijk is
- op het juiste niveau is
- één duidelijke opdracht bevat
- een controleerbaar antwoord heeft
```

## Didactische waarde

Hier zien leerlingen dat agents niet alleen output genereren, maar ook kunnen:

```text
- controleren
- feedback geven
- opnieuw proberen
- verbeteren
```

Dit is belangrijk omdat AI-output niet automatisch goed is.

## Leerlingenopdracht

Laat leerlingen een oefenvraag laten maken en daarna laten controleren.

Voorbeeldonderwerp:

```text
Elektrische stroomkring
```

Voorbeeldcontrole:

```text
Is deze vraag geschikt voor klas 2 vmbo basis/kader?
Geef maximaal drie verbeterpunten.
```

## Product aan het einde van sessie 5

Een verbeterde versie van een AI-output met feedback van een tweede agent.

---

# 11. Sessie 6 — Mini-project: eigen agent bouwen

## Doel

Leerlingen ontwerpen en presenteren hun eigen mini-agent.

## Mogelijke projecten

```text
- Huiswerkplanner-agent
- Quiz-agent
- Techniekcoach-agent
- Examen-oefenvraag-agent
- Feedback-agent voor teksten
- Woordjes-oefen-agent
- Planning-agent voor een project
- Veiligheidscontrole-agent voor praktijkopdrachten
```

## Verplichte onderdelen

Elke groep moet kunnen uitleggen:

```text
1. Wat is het doel van onze agent?
2. Voor wie is de agent bedoeld?
3. Welke instructie krijgt de agent?
4. Welke tools heeft de agent?
5. Wat moet de agent onthouden?
6. Hoe weet de agent dat hij klaar is?
7. Hoe controleren we of het resultaat goed is?
```

## Presentatievorm

Laat leerlingen presenteren met dit format:

```text
Naam agent:
Doel:
Gebruiker:
Tools:
Agent-loop:
Controle:
Demo of voorbeeld:
Wat kan beter?
```

## Product aan het einde van sessie 6

Een werkend prototype of een goed uitgewerkt ontwerp van een agent.

---

# 12. Voorbeeldproject: examen-oefenvraag-agent

Dit project sluit goed aan bij jouw onderwijscontext.

## Doel

Van een examenvraag een begrijpelijke oefenvraag maken voor een leerling.

## Agentrollen

```text
Agent 1: omzetter
Agent 2: controleur
Agent 3: verbeteraar
```

## Workflow

```text
1. Lees de oorspronkelijke examenvraag
2. Bepaal het onderwerp
3. Bepaal het niveau
4. Maak een eenvoudige oefenvraag
5. Maak een antwoordmodel
6. Controleer of vraag en antwoord kloppen
7. Verbeter indien nodig
8. Sla het eindresultaat op
```

## Voorbeeldstatus

```json
{
  "vraagnummer": 3,
  "onderwerp": "elektrische stroomkring",
  "niveau": "vmbo basis/kader",
  "status": "gecontroleerd",
  "feedback": "Vraag is duidelijk, antwoordmodel ontbreekt nog",
  "volgende_stap": "antwoordmodel toevoegen"
}
```

## Waarom dit project sterk is

Leerlingen zien hierin bijna alle belangrijke agentconcepten:

```text
- doelgericht werken
- meerdere stappen
- tools
- controle
- feedback
- verbeteren
- status bijhouden
```

---

# 13. Welke technologie gebruiken?

## Advies voor de eerste lessen

Gebruik zo min mogelijk technische ruis.

Aanbevolen:

```text
- papier of whiteboard voor schema’s
- simpele Python-bestanden
- eventueel Jupyter Notebook
- eenvoudige functies als tools
```

## Waarom Python?

Python is geschikt omdat:

```text
- de syntax relatief leesbaar is
- functies goed zichtbaar zijn
- pseudocode makkelijk naar Python te vertalen is
- leerlingen snel resultaat zien
```

## Waarom niet meteen TypeScript?

TypeScript is zeer geschikt voor moderne webapps en frameworks zoals Mastra, maar voor startende leerlingen kan het extra complexiteit toevoegen:

```text
- Node.js
- npm
- package.json
- types
- async/await
- projectstructuur
```

Dat is waardevol, maar niet als eerste stap wanneer het hoofddoel begrip van agents is.

---

# 14. Wanneer Mastra, LangGraph of OpenAI Agents SDK tonen?

## Mastra

Tonen als voorbeeld van:

```text
Zo kun je agents professioneler bouwen in TypeScript.
```

Mastra is interessant als leerlingen of docenten later richting webapps, Node.js en moderne AI-applicaties willen.

## LangGraph

Tonen als voorbeeld van:

```text
Zo kun je complexe agent-workflows bouwen met state, stappen en routes.
```

LangGraph past goed bij workflows waarin een agent meerdere stappen moet doorlopen en soms moet teruggaan of verbeteren.

## OpenAI Agents SDK

Tonen als voorbeeld van:

```text
Zo kun je met een professionele SDK agents bouwen met tools, handoffs, guardrails en tracing.
```

Dit kan goed als afsluiting:

```text
Wat wij zelf hebben gebouwd, bestaat ook als professioneel framework.
```

---

# 15. Didactische principes

## 15.1 Maak de magie zichtbaar

Leerlingen moeten niet alleen zien dat het werkt, maar ook waarom het werkt.

Dus niet alleen:

```text
De agent geeft antwoord.
```

Maar juist:

```text
De agent koos deze tool.
De tool gaf dit resultaat.
De agent gebruikte dat resultaat voor de volgende stap.
```

## 15.2 Eerst schema, dan code

Begin elke technische stap met een schema.

Voorbeeld:

```text
Input → beslissing → tool → observatie → nieuwe beslissing → output
```

Daarna pas code.

## 15.3 Werk met kleine successen

Gebruik eenvoudige opdrachten.

Niet meteen:

```text
Bouw een volledige autonome schoolagent.
```

Maar:

```text
Bouw een agent die een quizvraag maakt en controleert.
```

## 15.4 Laat fouten bewust gebeuren

Agents maken fouten. Dat is leerzaam.

Laat leerlingen onderzoeken:

```text
- Wat ging mis?
- Waarom ging het mis?
- Welke instructie ontbrak?
- Welke controle hadden we nodig?
- Welke tool had kunnen helpen?
```

---

# 16. Beoordelingsrubric

| Onderdeel | Beginnend | Voldoende | Goed |
|---|---|---|---|
| Begrip agent | Kan voorbeeld noemen | Kan verschil chatbot/agent uitleggen | Kan bouwstenen benoemen en toepassen |
| Prompt/instructie | Prompt is vaag | Prompt heeft rol en doel | Prompt heeft rol, doelgroep, grenzen en outputvorm |
| Tools | Tool is onduidelijk | Tool heeft duidelijke functie | Tool past logisch bij agentdoel |
| Agent-loop | Stappen ontbreken | Basisloop klopt | Loop bevat toolgebruik, observatie en stopvoorwaarde |
| Controle | Geen controle | Simpele controle | Duidelijke kwaliteitscriteria en verbetering |
| Presentatie | Uitleg is beperkt | Agent wordt begrijpelijk uitgelegd | Werking onder de motorkap wordt helder uitgelegd |

---

# 17. Minimale technische variant

Als je weinig tijd of technische middelen hebt, kun je de hele lessenreeks ook grotendeels zonder echte API bouwen.

Gebruik dan:

```text
- ChatGPT als LLM
- leerlingen als “programma”
- kaartjes als tools
- whiteboard als memory/state
```

Voorbeeld:

```text
Een leerling speelt de gebruiker.
Een leerling speelt het LLM.
Een leerling speelt de tool.
Een leerling speelt de controle-agent.
Het whiteboard is het geheugen.
```

Dit maakt het concept heel zichtbaar.

Daarna kun je dezelfde structuur vertalen naar code.

---

# 18. Praktische eindboodschap

Voor leerlingen is het belangrijkste niet dat ze een bepaald framework beheersen.

Het belangrijkste is dat ze begrijpen:

```text
Een agent is een systeem.
Het LLM is maar één onderdeel.
Tools voeren echte acties uit.
State houdt bij wat er gebeurt.
De loop bepaalt de volgende stap.
Controle bepaalt of het resultaat goed genoeg is.
```

Als dit begrip staat, kunnen ze later makkelijker overstappen naar:

```text
- Mastra
- LangGraph
- OpenAI Agents SDK
- CrewAI
- Pydantic AI
- LlamaIndex
- n8n / Flowise / Dify
```

Maar de basis blijft hetzelfde.

---

# 19. Samenvatting in één schema

```text
Gebruiker geeft doel
        ↓
Agent leest doel + instructie
        ↓
Agent kijkt naar state/geheugen
        ↓
Agent kiest volgende stap
        ↓
Tool nodig?
   ↓ ja                         ↓ nee
Tool uitvoeren              Eindantwoord maken
   ↓
Observatie/resultaat
   ↓
State bijwerken
   ↓
Controle nodig?
   ↓
Verbeteren of afronden
```

---

# 20. Mijn concrete advies

Voor jouw lessenreeks zou ik kiezen voor:

```text
Vanilla Python mini-agent
→ simpele tools
→ zichtbare agent-loop
→ evaluator-agent
→ mini-project
→ pas daarna frameworks tonen
```

Dus niet starten met Mastra als hoofdroute.

Gebruik Mastra, LangGraph of OpenAI Agents SDK pas als vergelijking:

```text
Wat wij zelf simpel hebben gebouwd,
doen frameworks op een professionele manier.
```

Dat geeft leerlingen begrip in plaats van alleen frameworkervaring.
