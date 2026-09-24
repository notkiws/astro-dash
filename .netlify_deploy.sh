#!/bin/bash
# Wait for the Netlify login ticket to be authorised, then create the site and deploy dist/.
LOG=/tmp/nl_deploy.log
: > "$LOG"
cd /home/hermes/space-hero || exit 1
echo "== waiting for authorisation (up to 15 min) ==" >> "$LOG"
timeout 900 netlify login >> "$LOG" 2>&1
if ! netlify status >> "$LOG" 2>&1; then echo "LOGIN_FAILED" >> "$LOG"; exit 1; fi
echo "== logged in ==" >> "$LOG"
netlify status >> "$LOG" 2>&1

echo "== create site ==" >> "$LOG"
SITE_ID=$(netlify api createSite --data '{"name":"astro-dash-notkiws"}' 2>>"$LOG" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('id',''))" 2>>"$LOG")
if [ -z "$SITE_ID" ]; then
  SITE_ID=$(netlify api listSites 2>>"$LOG" | python3 -c "import sys,json;d=json.load(sys.stdin);print(next((s['id'] for s in d if s.get('name','').startswith('astro-dash')),''))" 2>>"$LOG")
fi
echo "site id: $SITE_ID" >> "$LOG"
[ -z "$SITE_ID" ] && { echo "NO_SITE" >> "$LOG"; exit 1; }

echo "== deploy ==" >> "$LOG"
netlify deploy --prod --dir=dist --site "$SITE_ID" >> "$LOG" 2>&1
echo "== done ==" >> "$LOG"
grep -Eo 'https://[a-z0-9.-]+\.netlify\.app' "$LOG" | sort -u
