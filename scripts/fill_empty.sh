#!/bin/sh
# Re-generate empty replies in a pairs TSV: sh fill_empty.sh output/pairs_api.tsv
. ./.env; export GEMINI_API_KEY
f="$1"
: > "$f.tmp"
while IFS='	' read -r t r; do
  if [ -z "$r" ]; then
    r=$(python3 scripts/reply_api.py "$t" 2>/dev/null | tr -d '\n')
    sleep 7
  fi
  printf '%s\t%s\n' "$t" "$r" >> "$f.tmp"
done < "$f"
mv "$f.tmp" "$f"
awk -F'\t' '$2==""{n++} END{print (n+0)" still empty"}' "$f"
