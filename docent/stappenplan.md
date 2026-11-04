# Stappenplan voor de docent

Wat jij regelt, en wanneer: van de eerste les tot het einde van het schooljaar. Dezelfde stappen staan, met vinkjes en een rekenhulp, in `stappenplan.html`. De details staan in het [serverdraaiboek](serverdraaiboek.md), de [handleiding van de eindopdracht](eindopdracht-handleiding.md) en het [lesboek](../lesboek/lesboek.html).

**Voorbeeld: twee leerlingen.** Dan maak je twee leerlingprojecten (`leerling-01` en `leerling-02`) en één groep van twee (`groep1`). Met de limieten hieronder kost dat bij OpenAI hoogstens 2 × $5 + 1 × $10 = $20 per maand. Dat is een plafond, geen verwachting.

`groep0` is je testgroep op de server. Begin bij de leerlingen dus met `groep1`.

## 1. Vóór blok 1: per leerling

- [ ] **Een project per leerling.** Maak bij OpenAI `leerling-01`, `leerling-02`, enzovoort: een nummer, geen naam. Houd in je eigen klassenadministratie bij wie welk nummer heeft, niet in de repo. Dit kan al vroeg: zonder key kost een project niets. *Meer: draaiboek, "Een OpenAI-key per leerling".*
- [ ] **Een harde limiet.** Per project: Limits → Set spend limit, bijvoorbeeld $5 per maand, en **Enforce a hard limit** aan. Kijk op dezelfde pagina of `gpt-6.1-terra` mag.
- [ ] **Eén key per project, vlak voor het uitdelen.** Noem hem `laptop-leerling-01`. Vervaldatum: het einde van het schooljaar (31 juli). Geef hem met een eenmalige link uit een wachtwoordkluis (1 keer openen, na een dag verlopen); de leerling zet hem meteen in `.env`. Je hoeft niets te bewaren: kwijt is intrekken en een nieuwe maken (`laptop-leerling-01-2`). *Meer: draaiboek, "Uitdelen".*
- [ ] **Installeren in blok 1.** De leerling installeert git, uv en een editor (stappen voor Mac en Windows in het lesboek), clonet de repo (niet als ZIP downloaden: dan werkt `git pull` niet), typt `uv sync`, zet de key in `.env` en test met `uv run les1`. *Meer: lesboek, "Installeren".*
- [ ] **De Python-basis.** De lessen gaan uit van basiskennis Python ("Wat je al moet kunnen" in het lesboek). Regel die vóór les 1.

## 2. Vóór les 19: de server

- [ ] **Afspraken over de server.** Een quotum voor de schijf, of alleen controleren met `du`. En wie de mislukte runs controleert. *Meer: draaiboek, "Nog te doen".*
- [ ] **Een sleutel per leerling.** Elke leerling typt `ssh-keygen -t ed25519` en geeft jou het bestand `id_ed25519.pub`. Alleen het `.pub`-bestand.
- [ ] **Een gebruiker per groep.** Zet de sleutels in `sleutels-groep1.pub`, één regel per leerling, met de naam erachter. Dan: `scp sleutels-groep1.pub klasserver:` en `ssh klasserver 'sudo nieuwe-groep groep1 sleutels-groep1.pub && rm sleutels-groep1.pub'`. Controleer de vingerafdrukken. *Meer: draaiboek, "Een groep aanmaken".*
- [ ] **Een serverproject per groep.** Maak bij OpenAI `klasserver-groep1`, met een harde limiet en wat meer ruimte, bijvoorbeeld $10, zodat de pilot niet stilvalt. Noem de key `server-groep1`; hij verloopt aan het einde van het schooljaar. Geef hem met een eenmalige link aan de groep; die zet hem op de server in `.env`. *Meer: draaiboek, "Een OpenAI-key per groep".*
- [ ] **Het adres van de server.** Geef de leerlingen het IP-adres. Het staat niet in de repo, wel in de Hetzner Console.

## 3. Vóór de eindopdracht

- [ ] **Een klant per groep, en een reserveklant.** Een echte opdracht die past (en niet op de rode lijst staat). De reserveklant kan de school zelf zijn, bijvoorbeeld de mediatheek. *Meer: handleiding, "Een goede opdracht", "De rode lijst".*
- [ ] **De afspraak getekend.** De school tekent de afspraak met het bedrijf. *Meer: handleiding, "Een afspraaksjabloon voor school en bedrijf".*
- [ ] **Twee extra lessen.** Het intakegesprek oefenen, en de eigen repo, met inloggen bij GitHub vanaf de laptop. *Meer: handleiding, "Planning".*
- [ ] **Een privé-repo per groep.** De groep maakt hem en voegt jou toe. Op de server komt een deploy key die alleen mag lezen. *Meer: lesboek, "Jullie eigen repo".*

## 4. Tijdens de eindopdracht

- [ ] **Eind fase 1.** De afspraak is getekend; het proces en de nulmeting staan in het dossier. *Meer: handleiding, "Controlemomenten".*
- [ ] **Eind fase 2.** Het ontwerp en de testgevallen. Bewaar 5 testgevallen voor de eindtest.
- [ ] **Vóór echte gegevens: akkoord.** De privacyfunctionaris en het bedrijf beslissen, ook over de verwerkers: Hetzner en OpenAI. *Meer: handleiding, "Privacy".*
- [ ] **Vóór klantdata op de server: je eigen sleutel.** Zet een wachtwoordzin op je ssh-sleutel, met een ssh-agent. *Meer: draaiboek, "Nog te doen".*
- [ ] **De pilot.** Spreek af hoe de bestanden komen en gaan, en wie controleert. Geef de groep elke week de kosten van het serverproject: leerlingen kunnen het dashboard niet zien. *Meer: handleiding, "De pilot".*
- [ ] **Beoordelen.** Met de rubric uit het lesboek. De eindtest draait met je 5 bewaarde gevallen. *Meer: handleiding, "Beoordelen".*

## 5. Na de einddatum en aan het einde van het schooljaar

- [ ] **Per groep opruimen.** De timer uit en `~/werk` gewist. Met echte gegevens: de groep wist de kopieën op laptops. De groepskey ingetrokken, de deploy key uit de repo. Of de hele groep verwijderd. *Meer: handleiding, "Na de einddatum"; draaiboek, "Een groep verwijderen".*
- [ ] **OpenAI opruimen.** Trek de keys van de leerlingen in en archiveer alle projecten. De keys verlopen op 31 juli ook vanzelf. *Meer: draaiboek, "Einde van het schooljaar".*
- [ ] **De server.** Houd je hem niet voor volgend jaar, verwijder hem dan in de Hetzner Console. Pas dan stopt de rekening. *Meer: draaiboek, "Einde van het schooljaar".*

## Gaat er iets mis?

Een concept kan schade doen, er is een datalek, of de kosten lopen op: zet de groep stil met de **noodstop** uit het draaiboek. Bij de limiet stopt OpenAI vanzelf: elk verzoek krijgt dan fout `429` met `project_spend_limit_exceeded`.
