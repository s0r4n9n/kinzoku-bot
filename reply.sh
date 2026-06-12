#!/bin/sh
# Usage: ./reply.sh "ツイート本文"
[ -z "$1" ] && echo "usage: $0 \"tweet text\"" && exit 1
cd "$(dirname "$0")"
. ./.env; export GEMINI_API_KEY
python3 scripts/reply_api.py "$1"
