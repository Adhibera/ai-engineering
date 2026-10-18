#!/usr/bin/env bash
# Les 19: zet de code klaar op de server en zet de timer aan.
#
# Gebruik:  ./server/deploy.sh           de nieuwste versie
#           ./server/deploy.sh a1b2c3d   een vorige versie terugzetten (zie git log --oneline)
set -euo pipefail  # stop bij de eerste fout
cd "$(dirname "$0")/.."
versie="${1:-origin/main}"

# Stap 1: haal de versies op, en controleer dat de gekozen versie alles heeft wat de server nodig heeft
git fetch --quiet
for bestand in server/deploy.sh server/inbox.service server/inbox.timer pyproject.toml uv.lock; do
    git cat-file -e "$versie:$bestand" 2>/dev/null || { echo "Versie $versie mist $bestand. Er is niets veranderd."; exit 1; }
done

# Stap 2: zet de timer uit (ook na een herstart van de server), en wacht tot een lopende run klaar is
if [ -f ~/.config/systemd/user/inbox.timer ]; then
    systemctl --user disable --now inbox.timer
fi
while [ "$(systemctl --user is-active inbox.service)" = activating ]; do sleep 1; done

# Stap 3: de code en de packages (--locked: precies de versies uit uv.lock)
git checkout --quiet "$versie"
uv sync --locked --quiet

# Stap 4: de map voor het werk, de service en de timer, en de timer weer aan
mkdir -p ~/werk/inbox ~/.config/systemd/user
cp server/inbox.service server/inbox.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now inbox.timer

echo "Klaar. Versie: $(git log --oneline -1)"
