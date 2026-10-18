# Serverdraaiboek: de klassenserver

Dit draaiboek is voor de docent. Het beschrijft hoe de klassenserver is ingericht, hoe je een groep aanmaakt, hoe je een groep stopzet, en wat je aan het eind van het schooljaar opruimt.

**Getest op 18 en 19 oktober 2026**, op de echte server: Hetzner Cloud, Ubuntu 24.04.4 LTS, systemd 255. De commando's hieronder zijn de commando's die toen werkten. **Les 19 zelf** (`server/deploy.sh` en de inbox-timer) **is nog niet op de server getest.**

Het IP-adres staat hier niet in, want deze repo is openbaar. Je vindt het in de Hetzner Console. Waar `<IP>` staat, vul je het zelf in.

---

## Wat er staat

| Onderdeel | Keuze |
|---|---|
| Account | een eigen Hetzner-account, met tweestapsverificatie |
| Project | `klasserver` |
| Server | `klasserver`: type CPX22 (2 vCPU's AMD, 4 GB, 80 GB), in Nürnberg. De goedkopere Cost-Optimized-servers waren op 18 oktober niet te krijgen. |
| Image | Ubuntu 24.04. Niet 26.04: het plan is op 24.04 gebouwd, en 26.04 gebruikt sudo-rs en de Rust-coreutils. 24.04 krijgt updates tot 2029. |
| Firewall | `alleen-ssh`: inkomend alleen TCP 22 en ICMP, uitgaand alles |
| SSH-sleutel | `laptop-docent` |
| Backups | uit |
| Gebruikers | `beheer` (sudo zonder wachtwoord), `groep0` (de testgroep van de docent), later `groep1`, `groep2`, … |
| Kosten | €19,49 voor de server en €0,50 voor het IPv4-adres: **€19,99 per maand, zonder btw** |

Hetzner rekent zolang de server bestaat, ook als hij uitstaat. Pas als je hem verwijdert, stopt de rekening.

## Inloggen

Op de laptop van de docent staat in `~/.ssh/config`:

```
Host klasserver
  HostName <IP>
  User beheer
  IdentityFile ~/.ssh/id_ed25519_adhibera
  IdentitiesOnly yes
```

- `ssh klasserver` logt je in als `beheer`.
- `ssh groep0@klasserver` logt je in als de testgroep, met dezelfde sleutel.
- Leerlingen loggen in met `ssh groepN@<IP>`, met hun eigen sleutel.

Wil je als beheerder iets van een groep zien, gebruik dan `sudo systemctl --user -M groepN@ …`. `sudo -u groepN systemctl --user …` werkt niet, want dan is er geen sessie.

---

## De server opnieuw inrichten

Dit heb je nodig bij een nieuwe server, bijvoorbeeld volgend schooljaar. Doe het in deze volgorde. Houd bij stap 3 een tweede verbinding open, zodat je jezelf niet buitensluit.

### 1. In de Hetzner Console

- Maak een project, voeg de publieke sleutel toe (Security → SSH keys), en maak de firewall `alleen-ssh`.
- Maak de server: Ubuntu 24.04, een EU-locatie, minstens 4 GB, met de sleutel en de firewall aangevinkt. Laat Cloud config leeg.
- Vink de sleutel echt aan. Zonder sleutel stuurt Hetzner een rootwachtwoord per mail.
- *Controle:* `ssh root@<IP>` werkt.

### 2. Bijwerken en de tijdzone (als root)

```bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get full-upgrade -y \
  -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold
timedatectl set-timezone Europe/Amsterdam
ls /var/run/reboot-required 2>/dev/null && echo "herstart nodig"
```

- Staat er "herstart nodig", doe dan `systemctl reboot`. De server was na ongeveer 20 seconden terug.
- `unattended-upgrades` en `git` stonden al op het image van Hetzner. De automatische updates stonden ook al aan (`/etc/apt/apt.conf.d/20auto-upgrades`).
- Zonder de tijdzone staat de server op UTC. Dan kloppen de tijden in het logboek niet met de klok in de klas.

### 3. De beheerder maken en SSH dichtzetten (als root)

Eerst de beheerder:

```bash
adduser --disabled-password --gecos "" beheer
usermod -aG sudo beheer
install -d -m 700 -o beheer -g beheer /home/beheer/.ssh
install -m 600 -o beheer -g beheer /root/.ssh/authorized_keys /home/beheer/.ssh/
printf 'beheer ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/90-beheer
chmod 440 /etc/sudoers.d/90-beheer && visudo -c
```

*Controle, in een nieuwe verbinding:* `ssh beheer@<IP> 'whoami; sudo -n whoami'` geeft `beheer` en daarna `root`. Pas dan SSH dichtzetten:

```bash
cat > /etc/ssh/sshd_config.d/10-klasserver.conf <<'EOF'
# Klasserver: alleen inloggen met een sleutel, niet als root
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
X11Forwarding no
EOF
sshd -t && systemctl restart ssh
sshd -T | grep -Ei '^(passwordauthentication|kbdinteractiveauthentication|permitrootlogin|x11forwarding) '
```

- Bij sshd telt de eerste waarde die hij leest. Daarom begint de naam met `10-`. Op het image van Hetzner was `sshd_config.d/` nog leeg; er stond geen `50-cloud-init.conf`.
- `systemctl restart ssh` was genoeg, ook al gebruikt Ubuntu 24.04 `ssh.socket`.
- *Controle:* als `beheer` inloggen werkt, `ssh root@<IP>` wordt geweigerd, en `ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password beheer@<IP>` geeft `Permission denied (publickey)`.
- Zet daarna de korte naam `klasserver` in `~/.ssh/config` (zie "Inloggen").

Sudo zonder wachtwoord is handig, maar wie de sleutel heeft, is meteen root. Zie daarom "Nog te doen": een wachtwoordzin op de sleutel.

### 4. uv voor iedereen

```bash
curl -LsSf https://astral.sh/uv/0.12.17/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
uv --version
```

- De versie staat vast, zodat je weet wat je krijgt. Bij een nieuwe server mag je een nieuwere versie kiezen.
- Ubuntu 24.04 heeft Python 3.12, en de repo vraagt 3.13. Die downloadt uv per groep zelf, in de thuismap, bij de eerste `uv sync`.

### 5. Het logboek

```bash
sudo mkdir -p /etc/systemd/journald.conf.d
printf '[Journal]\nStorage=persistent\nSystemMaxUse=1G\n' | sudo tee /etc/systemd/journald.conf.d/50-klasserver.conf
sudo systemctl restart systemd-journald
```

Het logboek blijft bewaard na een herstart, en wordt nooit groter dan 1 GB. Elke groep krijgt een eigen journal-bestand, en ziet met `journalctl --user` alleen de eigen regels.

### 6. 's Nachts herstarten na updates

```bash
printf '%s\n' \
  'Unattended-Upgrade::Automatic-Reboot "true";' \
  'Unattended-Upgrade::Automatic-Reboot-Time "03:17";' \
  | sudo tee /etc/apt/apt.conf.d/52-klasserver
apt-config dump | grep Automatic-Reboot
```

- De updates draaien elke dag tussen 06:00 en 07:00. Vraagt een update om een herstart, bijvoorbeeld na een nieuwe kernel, dan herstart de server de nacht daarna om 03:17.
- Na een herstart starten de timers van de groepen vanzelf weer (getest). Een run die om 03:17 bezig is, wordt afgebroken. Dankzij les 18 is dat veilig.
- Getest is alleen dat de instelling gelezen wordt. Een echte nachtelijke herstart is nog niet getest.

### 7. Het script `nieuwe-groep`

Zet het script uit bijlage A op je laptop in een bestand `nieuwe-groep`. Dan:

```bash
scp nieuwe-groep klasserver:/tmp/
ssh klasserver 'sudo install -m 755 -o root -g root /tmp/nieuwe-groep /usr/local/sbin/nieuwe-groep && rm /tmp/nieuwe-groep'
```

Maak daarna de testgroep `groep0` met je eigen publieke sleutel, zoals in "Een groep aanmaken". Met de testtimer uit bijlage B kun je de server controleren voordat er leerlingen op komen.

---

## Een groep aanmaken

1. Elke leerling maakt een sleutel met `ssh-keygen -t ed25519`, en geeft jou het bestand `~/.ssh/id_ed25519.pub`. Alleen het `.pub`-bestand: het bestand zonder `.pub` is geheim.
2. Maak per groep één bestand, bijvoorbeeld `sleutels-groep3.pub`, met één regel per leerling. Vervang het commentaar achter elke sleutel door de naam van de leerling:
   ```
   ssh-ed25519 AAAAC3Nza... sanne
   ssh-ed25519 AAAAC3Nza... daan
   ```
   Dan zie je later welke sleutel van wie is, en kun je één leerling weghalen.
3. Zet het bestand op de server, en maak de groep:
   ```bash
   scp sleutels-groep3.pub klasserver:
   ssh klasserver 'sudo nieuwe-groep groep3 sleutels-groep3.pub && rm sleutels-groep3.pub'
   ```
4. Het script toont de vingerafdruk van elke sleutel. Twijfel je of een sleutel echt van de leerling is, vergelijk hem dan met `ssh-keygen -lf ~/.ssh/id_ed25519.pub` op de laptop van de leerling.
5. De leerling logt in met `ssh groep3@<IP>`.

**Wat het script doet:** een gebruiker zonder wachtwoord, een thuismap die alleen de groep kan lezen (750), de sleutels in `~/.ssh/authorized_keys` (700 en 600), linger (de timers draaien ook als niemand ingelogd is), en de grenzen uit "Grenzen per groep".

**Wat het script weigert** (getest met een tijdelijke `groep9`). In al deze gevallen stopt het script voordat er iets verandert:

| Invoer | Melding |
|---|---|
| zonder `sudo` | Start dit script met sudo. |
| een naam die niet `groepN` is | De naam moet groepN zijn, bijvoorbeeld groep3. |
| een bestand dat niet bestaat | Het bestand … bestaat niet. |
| een privésleutel | Dit is een privésleutel. Die is nu niet meer geheim: laat de leerling een nieuwe maken. |
| een kapotte regel tussen goede sleutels | Van de 2 sleutels zijn er 1 geldig. |
| een bestand met alleen commentaar | Van de 0 sleutels zijn er 0 geldig. |
| een groep die al bestaat | `adduser` stopt, en de sleutels blijven zoals ze waren. |

De telling is nodig, omdat `ssh-keygen` een kapotte regel zonder melding overslaat. Zonder telling merkt een leerling het pas als inloggen mislukt.

### Sleutels later aanpassen

Komt er een leerling bij, of moet er een weg? Pas het bestand op je laptop aan, controleer het met `ssh-keygen -lf sleutels-groep3.pub`, en zet het opnieuw neer:

```bash
scp sleutels-groep3.pub klasserver:
ssh klasserver 'sudo install -m 600 -o groep3 -g groep3 sleutels-groep3.pub /home/groep3/.ssh/authorized_keys && rm sleutels-groep3.pub'
```

Een verbinding die al openstaat, blijft open. Een nieuwe verbinding met een weggehaalde sleutel lukt niet meer.

### Een groep verwijderen

```bash
g=groep3; u=$(id -u "$g")
sudo loginctl disable-linger "$g"
sudo loginctl terminate-user "$g"    # een foutmelding betekent: er draaide niets meer
sudo deluser --remove-home "$g"
sudo rm -r "/etc/systemd/system.control/user-$u.slice.d"
sudo systemctl daemon-reload
```

Daarmee zijn de thuismap, de timers, het werk en de grenzen weg. De OpenAI-key trek je apart in.

---

## Grenzen per groep

Het script zet de grenzen per groep met `systemctl set-property`. Ze gelden dus niet voor `beheer`.

| Grens | Waarde | Waarom | Getest |
|---|---|---|---|
| `MemoryMax` | 256M | Tien groepen en `groep0` samen gebruiken hoogstens ongeveer 2,75 GB van de 4 GB. | Een proces dat 400 MB vroeg, werd gestopt. Alleen dat proces, niet de server. |
| `MemorySwapMax` | 0 | Er is geen swap. Dit houdt het zo als er ooit swap bijkomt. | – |
| `TasksMax` | 128 | Tegen een programma dat eindeloos nieuwe processen start. | Alleen de instelling. |
| `CPUQuota` | 25% | Een kwart van één CPU per groep. | 10 seconden rekenen gaf 2,5 seconden CPU-tijd. |

`uv sync --locked` van de lesrepo, met het downloaden van Python 3.13, lukte binnen deze grenzen in 11 seconden.

- **Bekijken:** `systemctl show user-$(id -u groep3).slice -p MemoryMax -p MemorySwapMax -p TasksMax -p CPUQuotaPerSecUSec`. Verwacht: `268435456`, `0`, `128` en `250ms`.
- **Aanpassen**, bijvoorbeeld meer geheugen voor één groep: `sudo systemctl set-property user-$(id -u groep3).slice MemoryMax=512M`. De instelling blijft bewaard in `/etc/systemd/system.control/`.
- **Schijfruimte:** er zijn geen quota. Een groep gebruikt ongeveer 165 MB (Python 108 MB en de cache van uv), en ongeveer 230 MB met de `.venv` erbij. De schijf is 75 GB, en er was 70 GB vrij. Controleer met `sudo du -sh /home/*` en `df -h /`. Codex raadt quota aan (voor ruimte en voor het aantal bestanden) vóór er tien groepen komen, want controleren voorkomt geen volle schijf. Zie "Nog te doen".

## Overzicht

```bash
# De timers en de mislukte units van alle groepen
for g in $(getent passwd | cut -d: -f1 | grep '^groep'); do
  echo "== $g"
  sudo systemctl --user -M "$g@" list-timers --no-pager --no-legend
  sudo systemctl --user -M "$g@" --failed --no-pager --no-legend
done

sudo journalctl _UID=$(id -u groep3) -n 50 --no-pager   # het logboek van één groep
sudo du -sh /home/*; df -h /                            # de schijfruimte
ls /var/run/reboot-required                             # wacht er een herstart?
sudo journalctl --list-boots --no-pager | tail -3       # wanneer is de server herstart?
```

- `launchpadlib-cache-clean.timer` staat bij elke groep. Die timer hoort bij Ubuntu, niet bij de groep.
- Elke `-M`-opdracht zet een paar regels "Failed to release session: Access denied" in het logboek van die groep. De opdracht werkt wel. De groep kan die regels zien in `journalctl --user`.

## Noodstop

Gebruik dit als een groep iets doet wat niet mag, of als de kosten oplopen. Getest op `groep0`.

**1. Op de server.** Kopieer het hele blok; het duurt een paar seconden:

```bash
g=groep3
sudo usermod --expiredate 1 "$g"     # niemand van de groep kan nog inloggen, ook niet met een sleutel
sudo loginctl disable-linger "$g"    # niets start meer zonder login
sudo loginctl terminate-user "$g"    # alle processen en verbindingen van de groep stoppen
```

**2. Bij OpenAI.** Trek in het dashboard de key van de groep in. Het programma op de server is al gestopt, maar de key kan ook nog ergens anders staan, bijvoorbeeld op een laptop.

Waarom deze volgorde: kan de groep nog inloggen, dan kan ze de timer weer aanzetten. En met alleen linger uit draaien de timers nog steeds zolang iemand ingelogd is.

*Controle:*
- `ssh groep3@<IP>` geeft "Your account has expired; please contact your system administrator."
- `ps -u groep3 --no-headers | wc -l` geeft `0`.
- De timer loopt niet meer. In de test liep hij 3,5 minuut lang niet.

**Weer aanzetten:**

```bash
sudo usermod --expiredate "" groep3
sudo loginctl enable-linger groep3
```

- De timers van de groep lopen dan meteen weer, met de code die er stond (getest). Zorg dus eerst dat het probleem is opgelost.
- Met de ingetrokken key mislukt elke run. De groep zet een nieuwe key in `.env`.

**Eén leerling blokkeren:** haal de regel van die leerling uit het sleutelbestand (zie "Sleutels later aanpassen"). De rest van de groep kan dan doorwerken.

## Einde van het schooljaar

1. **Bewaar wat moet blijven.** De code staat in git. Het werk op de server, zoals de inbox, de concepten en de logboeken, wordt niet bewaard: er zijn geen backups. Klantdata bewaar je alleen als dat met het bedrijf is afgesproken.
2. **OpenAI:** trek per groep de key in, en archiveer de projecten.
3. **Hetzner:** verwijder de server in de console. Pas dan stopt de rekening. Kijk daarna bij Primary IPs of het IPv4-adres ook weg is; dat is niet getest. De firewall, de SSH-sleutel en het project kosten niets en mogen blijven.
4. **De laptop:** haal `Host klasserver` uit `~/.ssh/config`, en de oude sleutel van de server uit `known_hosts` met `ssh-keygen -R <IP>`.

Wil je de server houden voor volgend jaar, verwijder dan alleen de groepen (zie "Een groep verwijderen"). Een nieuwe server inrichten kan ook: zie "De server opnieuw inrichten".

---

## Goed om te weten

- **Groepen zien elkaars processen.** `ps` toont ook de programma's van andere groepen, met de commandoregel. Zet daarom geen geheim in een commandoregel. `.env` is wel afgeschermd, want de thuismap staat op 750. Met de mount-optie `hidepid` kun je processen verbergen, maar die heeft gevolgen voor systemd en logind. Dat is niet gedaan.
- **De beheerder kan alle prints lezen.** journald stuurt alles ook door naar `/var/log/syslog`. Dat kunnen alleen root en de groep `adm` lezen, de groepen niet. Maar print een groep klantdata, dan staat die daar ook. Spreek bij de eindopdracht af: geen klantdata printen.
- **De groep `users`.** `adduser` zet elke groep ook in de groep `users`. Dat is onschuldig, want de thuismappen staan op 750: alleen de eigenaar en de eigen groep kunnen erbij.
- **De timer is niet precies.** Een timer van elke 2 minuten liep om 22:28:12, 22:30:04 en 22:32:12. Hij kan tot een minuut later afgaan (`AccuracySec`).
- **Buitengesloten?** Root en `beheer` hebben geen wachtwoord, dus de webconsole van Hetzner helpt niet zomaar. Hetzner heeft in de console een rescue-systeem en een knop om het rootwachtwoord opnieuw in te stellen. Dat is niet getest.

## Nog te doen

**Vóór de groepen van leerlingen:**
- [ ] beslissen over quota voor de schijf, of alleen controleren met `du`
- [ ] les 19 testen op `groep0`: `server/deploy.sh`, de inbox-timer, en `scp` naar de inbox
- [ ] afspreken wie de mislukte runs controleert, en de mails die in de inbox blijven liggen

**Bij les 19:**
- [ ] per groep een OpenAI-project met een eigen key, en "Enforce a hard limit" aan. Een melding over de kosten houdt niets tegen. Volgens Codex kan een harde limiet door vertraging iets worden overschreden; dat is niet door Claude gecontroleerd.

**Vóór er klantdata op de server komt:**
- [ ] een wachtwoordzin op de sleutel van de docent (`ssh-keygen -p -f ~/.ssh/id_ed25519_adhibera`), met een ssh-agent. Nu heeft de sleutel geen wachtwoordzin. De schijf van de laptop is wel versleuteld.

## Wat er getest is (18 en 19 oktober 2026)

Met de testtimer uit bijlage B, als `groep0`, en een tijdelijke tweede groep `proef`:

| Test | Resultaat |
|---|---|
| Uitloggen | De timer liep door zonder sessie (linger). |
| Herstarten | Na de herstart liep de timer vanzelf weer. Het logboek van `groep0` had de runs van vóór en na de herstart. |
| Eigen logboek | `journalctl --user -u hallo` toonde de prints. |
| Scheiding | `proef` kon van `groep0` niet lezen: de thuismap, `/run/user/1001`, het logboek (ook het journal-bestand en `/var/log/syslog`) en `systemctl --user -M groep0@` werden geweigerd of waren leeg. |
| Geheugen | 400 MB vragen: het proces werd gestopt door de OOM-killer van de groep. |
| CPU | 10 seconden rekenen gaf 2,5 seconden CPU-tijd. |
| Python | `uv sync --locked` van de lesrepo, met Python 3.13, in 11 seconden. |
| Noodstop | Inloggen geweigerd, 0 processen, de timer liep niet meer. |
| Weer aanzetten | Inloggen werkte, en de timer liep weer. |
| `nieuwe-groep` | Zeven soorten foute invoer geweigerd, zonder dat er iets veranderde. Een goede groep klopte: de rechten, linger, de grenzen en inloggen. |
| 's Nachts herstarten | Alleen de instelling (`apt-config dump`). |

**Niet getest:** `TasksMax` echt bereiken, een echte nachtelijke herstart, les 19 op de server, en het rescue-systeem van Hetzner.

---

## Bijlage A: het script `nieuwe-groep`

Op de server staat het in `/usr/local/sbin/nieuwe-groep`.

```bash
#!/usr/bin/env bash
# Klasserver: maak een groep aan, met een gebruiker, sleutels, linger en grenzen.
# Gebruik: sudo nieuwe-groep groep3 sleutels-groep3.pub
set -euo pipefail

[[ $# -eq 2 ]] || { echo "Gebruik: sudo nieuwe-groep groepN sleutels.pub"; exit 1; }
[[ $EUID -eq 0 ]] || { echo "Start dit script met sudo."; exit 1; }
naam="$1"; sleutels="$2"
[[ "$naam" =~ ^groep[0-9]+$ ]] || { echo "De naam moet groepN zijn, bijvoorbeeld groep3."; exit 1; }
[[ -f "$sleutels" ]] || { echo "Het bestand $sleutels bestaat niet."; exit 1; }

# Controleer de sleutels voordat er iets verandert
if grep -q "PRIVATE KEY" "$sleutels"; then
  echo "Dit is een privésleutel. Die is nu niet meer geheim: laat de leerling een nieuwe maken."
  exit 1
fi
regels=$(grep -cvE '^[[:space:]]*(#|$)' "$sleutels" || true)
geldig=$(ssh-keygen -l -f "$sleutels" 2>/dev/null | wc -l || true)
[[ "$regels" -gt 0 && "$regels" -eq "$geldig" ]] || { echo "Van de $regels sleutels zijn er $geldig geldig."; exit 1; }
ssh-keygen -l -f "$sleutels"

adduser --disabled-password --gecos "" "$naam"
install -d -m 700 -o "$naam" -g "$naam" "/home/$naam/.ssh"
install -m 600 -o "$naam" -g "$naam" "$sleutels" "/home/$naam/.ssh/authorized_keys"
loginctl enable-linger "$naam"
systemctl set-property "user-$(id -u "$naam").slice" \
  MemoryMax=256M MemorySwapMax=0 TasksMax=128 CPUQuota=25%
echo "Klaar: $naam (UID $(id -u "$naam"))"
```

## Bijlage B: de testtimer

Hiermee controleer je een nieuwe server, los van les 19. Log in als de groep, en zet in `~/.config/systemd/user/` twee bestanden.

`hallo.service`:

```ini
[Unit]
Description=Testtimer: schrijf de tijd naar hallo.txt

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'date "+%%F %%T" >> %h/hallo.txt && echo "hallo van %u"'
```

`hallo.timer`:

```ini
[Unit]
Description=Start hallo.service elke 2 minuten

[Timer]
OnCalendar=*:0/2

[Install]
WantedBy=timers.target
```

Aanzetten en bekijken:

```bash
systemd-analyze --user verify ~/.config/systemd/user/hallo.service ~/.config/systemd/user/hallo.timer
systemctl --user daemon-reload
systemctl --user enable --now hallo.timer
systemctl --user list-timers hallo.timer
journalctl --user -u hallo
```

Log uit, wacht een paar minuten, en kijk of `~/hallo.txt` gegroeid is. Doe hetzelfde na `sudo systemctl reboot`.

Opruimen:

```bash
systemctl --user disable --now hallo.timer
rm ~/.config/systemd/user/hallo.service ~/.config/systemd/user/hallo.timer ~/hallo.txt
systemctl --user daemon-reload
```
