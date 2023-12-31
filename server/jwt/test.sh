#!/usr/bin/env bash

# source env
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "$DIR/../../.env"

# get
# curl -X 'GET' \
#   -H "Authorization: Bearer $SERVER_JWT_TOKEN"   \
#   'http://192.168.1.45:3001/texts?text_id=gte.1&text=like.b*' \
#   -H 'accept: application/json'

# delete
# curl -X 'DELETE' \
#   -H "Authorization: Bearer $SERVER_JWT_TOKEN"   \
#   "http://192.168.1.45:$SERVER_PORT/texts?text_id=eq.1" \
#   -H 'accept: application/json'

# post
curl -X 'POST' \
  -H "Authorization: Bearer $SERVER_JWT_TOKEN"   \
  "http://192.168.1.45:$SERVER_PORT/texts" \
  -H 'Content-Type: application/json' \
  -d '{ "text": "value1" }'